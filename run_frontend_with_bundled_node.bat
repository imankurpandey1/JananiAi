@echo off
cd /d "%~dp0"
set NODE_EXE=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe
set PNPM_CLI=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\pnpm\bin\pnpm.cjs
"%NODE_EXE%" "%PNPM_CLI%" install
"%NODE_EXE%" "%PNPM_CLI%" -F storycraft-ai-frontend run dev
