@echo off
powershell -command "Stop-Process -Name InSpec* -Force"
cd "C:\Microvu Programs\MvRun"
powershell -command "foreach ($a in (ls -r -i info* -File)) { del $a.FullName }
cd "C:\Program Files (x86)\Micro-Vu Corporation\InSpec for Windows\"
start "" "InSpec.exe"
powershell -command "$mvRunProcess = Get-Process -Name MvRun -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }; if ($mvRunProcess) { (New-Object -ComObject wscript.shell).AppActivate($mvRunProcess.Id)}"
