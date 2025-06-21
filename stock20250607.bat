@echo off

echo 停止 train1.exe (如果有執行中)...
taskkill /IM train1.exe /F >nul 2>&1

echo 刪除舊的 dist\train1.exe...
del /F /Q dist\train1.exe >nul 2>&1

echo 升級 pyinstaller 和 altgraph...
pip uninstall -y pyinstaller altgraph
pip install pyinstaller==6.6.0

echo 執行 pyinstaller 打包...
pyinstaller --noconsole --onefile --icon=app.ico train1.py

echo 完成！
pause