@echo off
git rev-parse --is-inside-work-tree >nul 2>&1
if %errorlevel%==0 (
    echo ?前目?是 Git ??，???行操作...

    echo 正在??程拉取最新代?并合并...
    git pull origin main || echo 拉取失?

    set /p commit_msg=??入本次提交信息:

    echo 正在提交代?...
    git add .
    git commit -m "%commit_msg%" || echo 提交失?

    echo 正在推送到?程??...
    git push origin main || echo 推送失?
) else (
    echo ?前目?不是 Git ??！
    echo ???操作：
    echo 1) 初始化一?新的 Git ??
    echo 2) ?入正确的 Git ??目?路?
    echo 3) 退出

    set /p choice=??入???字:

    if "%choice%"=="1" (
        git init
        echo Git ??已初始化。
    ) else if "%choice%"=="2" (
        set /p repo_path=??入 Git ??目?路?:
        if exist "%repo_path%\.git" (
            cd /d "%repo_path%"
            echo 已切?到 %repo_path%
        ) else (
            echo 目?不是有效的 Git ??
        )
    ) else (
        echo 退出
        exit /b 1
    )
)

pause

