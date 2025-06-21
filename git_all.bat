@echo off
git rev-parse --is-inside-work-tree >nul 2>&1
if %errorlevel%==0 (
    echo ?�e��?�O Git ??�A???��ާ@...

    echo ���b??�{�Ԩ��̷s�N?�}�X�}...
    git pull origin main || echo �Ԩ���?

    set /p commit_msg=??�J��������H��:

    echo ���b����N?...
    git add .
    git commit -m "%commit_msg%" || echo ���楢?

    echo ���b���e��?�{??...
    git push origin main || echo ���e��?
) else (
    echo ?�e��?���O Git ??�I
    echo ???�ާ@�G
    echo 1) ��l�Ƥ@?�s�� Git ??
    echo 2) ?�J���̪� Git ??��?��?
    echo 3) �h�X

    set /p choice=??�J???�r:

    if "%choice%"=="1" (
        git init
        echo Git ??�w��l�ơC
    ) else if "%choice%"=="2" (
        set /p repo_path=??�J Git ??��?��?:
        if exist "%repo_path%\.git" (
            cd /d "%repo_path%"
            echo �w��?�� %repo_path%
        ) else (
            echo ��?���O���Ī� Git ??
        )
    ) else (
        echo �h�X
        exit /b 1
    )
)

pause

