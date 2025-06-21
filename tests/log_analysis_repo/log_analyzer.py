import json
import re
from pathlib import Path

LOG_DIR = "logs"

def analyze_logs():
    folder = Path(LOG_DIR)
    log_files = list(folder.glob("*.log")) + list(folder.glob("*.txt"))
    if not log_files:
        print("找不到任何 .log 或 .txt 檔案")
        return
    largest_file = max(log_files, key=lambda f: f.stat().st_size)
    error_lines = []
    uptime_lines = []
    bub_values = []
    with largest_file.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if "[ERROR][testbody] [ERROR]" in line:
                error_lines.append(line)
            if "[SSH][CMD] uptime" in line and "4 days" in line:
                uptime_lines.append(line)
            match = re.search(r'"did_value"\s*:\s*\{[^}]*?"BUB_NUM_CHARGE_CYCLE"\s*:\s*(\d+)', line)
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
    output_file = folder / "search_results.json"
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"分析完成，結果儲存至 {output_file}")

if __name__ == "__main__":
    analyze_logs()
