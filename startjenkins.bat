@echo off
setlocal

REM ====== 1. 設定變數 ======
set JENKINS_WAR="C:\Program Files\Jenkins\Jenkins.war"
set INIT_DIR=%USERPROFILE%\.jenkins\init.groovy.d
set GROOVY_FILE=%INIT_DIR%\create_user.groovy
set USERNAME=alextsou
set PASSWORD=daria0904@
set FULLNAME="Alex Tsou"
set INSTANCE_PORT=8080

REM ====== 2. 建立 init.groovy.d 來自動新增帳號（若尚未存在） ======
if not exist "%INIT_DIR%" (
    mkdir "%INIT_DIR%"
)

if not exist "%GROOVY_FILE%" (
    echo Creating groovy script to auto-create user...

    > "%GROOVY_FILE%" (
        echo import jenkins.model.*
        echo import hudson.security.*
        echo def instance = Jenkins.getInstance()
        echo def hudsonRealm = new HudsonPrivateSecurityRealm(false)
        echo hudsonRealm.createAccount("%USERNAME%", "%PASSWORD%")
        echo instance.setSecurityRealm(hudsonRealm)
        echo def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
        echo instance.setAuthorizationStrategy(strategy)
        echo instance.save()
    )
)

REM ====== 3. 啟動 Jenkins ======
echo Starting Jenkins...
start cmd /k "java -jar %JENKINS_WAR% --httpPort=%INSTANCE_PORT%"

REM ====== 4. 等待幾秒再開網頁 ======
timeout /t 10 > nul
start http://localhost:%INSTANCE_PORT%

endlocal