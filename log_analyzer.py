# log_analyzer.py

import json
import re
from pathlib import Path
import sys

def analyze_log_folder(folder_path="logs"):
    folder = Path(folder_path)
    output_file = folder / "search_results.json"

    log_files = list(folder.glob("*.log")) + list(folder.glob("*.txt"))
    if not log_files:
        print("❌ 找不到 .log 或 .txt 檔案")
        return

    largest_file = max(log_files, key=lambda f: f.stat().st_size)
    error_lines = []
    uptime_lines = []
    bub_values = []

    with largest_file.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            stripped_line = line.strip()
            if "[ERROR][testbody] [ERROR]" in stripped_line:
                error_lines.append(stripped_line)
            if "[SSH][CMD] uptime" in stripped_line and "4 days" in stripped_line:
                uptime_lines.append(stripped_line)
            match = re.search(r'"did_value"\s*:\s*\{[^}]*?"BUB_NUM_CHARGE_CYCLE"\s*:\s*(\d+)', stripped_line)
            if match:
                bub_values.append(int(match.group(1)))

    is_increasing = True
    violations = []
    last_value = -1
    for val in bub_values:
        if val < last_value:
            is_increasing = False
            violations.append({"current": val, "previous": last_value})
        last_value = val

    result = {
        "檔案": largest_file.name,
        "錯誤行數": len(error_lines),
        "BUB_NUM_CHARGE_CYCLE": {
            "數值": bub_values,
            "是否遞增": "是" if is_increasing else "否",
            "遞增錯誤": violations
        },
        "含 4 days uptime 行數": len(uptime_lines)
    }

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ 分析完成：{largest_file.name}")
    print(f"📄 結果已儲存：{output_file}")

if __name__ == "__main__":
    # 支援命令列參數可指定資料夾，預設 logs/
    path = sys.argv[1] if len(sys.argv) > 1 else "logs"
    analyze_log_folder(path)

