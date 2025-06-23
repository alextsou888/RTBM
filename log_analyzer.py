import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import json
import re
import subprocess
import shutil

# 語系資料
LANG_TEXT = {
    "zh": {
        "title": "Log 分析工具 - BUB_NUM_CHARGE_CYCLE",
        "select_label": "選擇 Log 資料夾:",
        "button": "選擇資料夾並分析",
    },
    "en": {
        "title": "Log Analyzer - BUB_NUM_CHARGE_CYCLE",
        "select_label": "Select Log Folder:",
        "button": "Browse and Analyze",
    }
}

current_lang = "zh"
current_theme = "light"


def analyze_log_folder(folder_path, result_display):
    folder = Path(folder_path)
    output_file = folder / "search_results.json"

    log_files = list(folder.glob("*.log")) + list(folder.glob("*.txt"))
    if not log_files:
        messagebox.showerror("錯誤", "找不到任何 .log 或 .txt 檔案")
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

    result_display.delete(1.0, tk.END)
    result_display.insert(tk.END, f"分析檔案: {largest_file.name}\n\n")

    result_display.insert(tk.END, f"[錯誤行數]: {len(error_lines)}\n", "bold")
    for line in error_lines:
        result_display.insert(tk.END, f"{line}\n", "error")

    result_display.insert(tk.END, f"\n[含 4 days uptime 行數]: {len(uptime_lines)}\n", "bold")
    for line in uptime_lines:
        result_display.insert(tk.END, f"{line}\n", "uptime")

    result_display.insert(tk.END, f"\n[BUB 數值]: {bub_values}\n", "bold")
    result_display.insert(tk.END, f"[是否遞增]: {'✅ 是' if is_increasing else '❌ 否'}\n", "bold")
    if not is_increasing:
        result_display.insert(tk.END, f"[遞增錯誤]: {violations}\n")

    result_display.insert(tk.END, f"\n✅ JSON 已儲存：{output_file}\n")

    try:
        subprocess.Popen(["notepad++", str(output_file)])
    except FileNotFoundError:
        try:
            subprocess.Popen(["notepad", str(output_file)])
        except FileNotFoundError:
            messagebox.showwarning("警告", "⚠ 找不到 Notepad++ 或記事本，請手動開啟 JSON 檔案")


def browse_folder(entry, result_display):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry.delete(0, tk.END)
        entry.insert(0, folder_selected)
        analyze_log_folder(folder_selected, result_display)


def create_gui():
    global current_lang, current_theme

    root = tk.Tk()
    root.title(LANG_TEXT[current_lang]["title"])
    root.geometry("900x650")

    def switch_language(lang):
        global current_lang
        current_lang = lang
        label.config(text=LANG_TEXT[lang]["select_label"])
        browse_button.config(text=LANG_TEXT[lang]["button"])
        root.title(LANG_TEXT[lang]["title"])

    def toggle_theme():
        global current_theme
        if current_theme == "light":
            current_theme = "dark"
            root.config(bg="#2b2b2b")
            label.config(bg="#2b2b2b", fg="lightblue")
            result_box.config(bg="#1e1e1e", fg="white", insertbackground="white")
        else:
            current_theme = "light"
            root.config(bg="SystemButtonFace")
            label.config(bg="SystemButtonFace", fg="blue")
            result_box.config(bg="white", fg="black", insertbackground="black")

    # UI 元件
    top_frame = tk.Frame(root)
    top_frame.pack(pady=5)

    label = tk.Label(top_frame, text=LANG_TEXT[current_lang]["select_label"], fg="blue", font=("Arial", 10, "bold"))
    label.pack(side=tk.LEFT)

    path_entry = tk.Entry(top_frame, width=70)
    path_entry.pack(side=tk.LEFT, padx=5)

    browse_button = tk.Button(top_frame, text=LANG_TEXT[current_lang]["button"],
                              command=lambda: browse_folder(path_entry, result_box))
    browse_button.pack(side=tk.LEFT)

    result_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=30)
    result_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 標籤樣式
    result_box.tag_config("error", foreground="red")
    result_box.tag_config("uptime", foreground="blue")
    result_box.tag_config("bold", font=("Arial", 10, "bold"))

    # 語系與主題切換按鈕
    lang_frame = tk.Frame(root)
    lang_frame.pack(pady=5)

    tk.Button(lang_frame, text="繁中", command=lambda: switch_language("zh")).pack(side=tk.LEFT, padx=5)
    tk.Button(lang_frame, text="English", command=lambda: switch_language("en")).pack(side=tk.LEFT, padx=5)
    tk.Button(lang_frame, text="🌙 切換主題", command=toggle_theme).pack(side=tk.LEFT, padx=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()