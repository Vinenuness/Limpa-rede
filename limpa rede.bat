@echo off
setlocal
title Limpa Rede
color 0A

set "APP=%~dp0dist\LimpaRede.exe"
set "SCRIPT=%~dp0limpa_rede.py"

echo ====================================================
echo                 LIMPA REDE - WINDOWS
echo ====================================================
echo.
echo  [1] Diagnostico
echo  [2] Simular reparo (nao altera nada)
echo  [3] Reparo conservador
echo  [4] Reparo com reset da pilha de rede
echo  [0] Sair
echo.
choice /c 12340 /n /m "Escolha uma opcao: "

if errorlevel 5 exit /b 0
if errorlevel 4 set "ARGS=reparo --reset-stack" & goto run
if errorlevel 3 set "ARGS=reparo" & goto run
if errorlevel 2 set "ARGS=reparo --dry-run" & goto run
if errorlevel 1 set "ARGS=diagnostico" & goto run

:run
if exist "%APP%" (
    "%APP%" %ARGS%
    set "EXITCODE=%errorlevel%"
) else if exist "%SCRIPT%" (
    where python >nul 2>&1
    if errorlevel 1 (
        echo.
        echo [ERRO] Python nao foi encontrado neste computador.
        set "EXITCODE=1"
    ) else (
        python "%SCRIPT%" %ARGS%
        set "EXITCODE=%errorlevel%"
    )
) else (
    echo.
    echo [ERRO] Nao foi encontrado o executavel nem o script Python.
    set "EXITCODE=1"
)

echo.
if not "%EXITCODE%"=="0" echo O comando terminou com codigo %EXITCODE%.
pause
exit /b %EXITCODE%
