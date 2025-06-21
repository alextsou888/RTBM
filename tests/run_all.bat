@echo off
REM 先檢查 Python 是否存在
where python >nul 2>&1
IF ERRORLEVEL 1 (
    echo 找不到 Python，請先安裝 Python 並設定環境變數。
    pause
    exit /b 1
)

REM 建立 logs 資料夾（若不存在）
if not exist logs (
    mkdir logs
)

echo 正在下載 Log 檔...
python download_logs.py
if ERRORLEVEL 1 (
    echo 下載 Log 失敗，請檢查 download_logs.py。
    pause
    exit /b 1
)

echo 下載完成，開始分析 Log 檔...
python log_analyzer.py
if ERRORLEVEL 1 (
    echo 分析 Log 失敗，請檢查 log_analyzer.py。
    pause
    exit /b 1
)

echo 分析完成，結果存於 logs\search_results.json
pause
