@echo off
cd /d "%~dp0"
set NODE_ROOT=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node
set NODE_DIR=%NODE_ROOT%\bin
set PATH=%NODE_DIR%;%PATH%
set NODE_EXE=%NODE_DIR%\node.exe
set PNPM_CLI=%NODE_ROOT%\node_modules\pnpm\bin\pnpm.cjs
"%NODE_EXE%" "%PNPM_CLI%" install --ignore-scripts
"%NODE_EXE%" "%PNPM_CLI%" -F storycraft-ai-frontend run dev
