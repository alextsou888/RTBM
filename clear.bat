@echo off
REM 移除 .git\modules 內的子模組資料夾
rmdir /s /q .git\modules\GitHub\desktop-tutorial

REM 從 Git 索引中移除子模組資料夾
git rm -f GitHub/desktop-tutorial

REM 如果 rm 成功，提交變更
git commit -m "Remove broken submodule GitHub/desktop-tutorial"

REM 設定 main 分支遠端上游並推送
git push --set-upstream origin main
