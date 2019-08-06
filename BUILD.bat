@echo off
cd /d %cd%
cd %cd%
pyinstaller tea.py --noconsole --upx-dir .\upx395_win64
pause
exit