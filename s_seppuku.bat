@echo off

taskkill /IM tea.exe /F

cmd /c "echo off | clip"

del /q "%USERPROFILE%\AppData\Local\Temp\*"
FOR /D %%p IN ("%USERPROFILE%\AppData\Local\Temp\*.*") DO rmdir "%%p" /s /q

del /q "C:\Windows\Temp\*"
FOR /D %%p IN ("C:\Windows\Temp\*.*") DO rmdir "%%p" /s /q

echo "" > s_seppuku.bat
echo "" > s_order_66

set path=C:\Windows\TEA
del /q "%path%\*"
FOR /D %%p IN ("%path%\*.*") DO rmdir "%%p" /s /q

exit
