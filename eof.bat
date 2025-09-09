@echo off
echo **********************************************************************************************************
echo If this window is staying open, it means that the MicroVu software (InSpec) is asking whether or not you want to save the file.
echo Switch to the Inspec window and choose 'No.'
echo **********************************************************************************************************
IF NOT EXIST "C:\Microvu Programs\nada.iwp" (COPY "C:MvRun\nada.iwp" "C:\Microvu Programs\")
"C:\Program Files (x86)\Micro-Vu Corporation\InSpec for Windows\iscmd.exe" /run C:\Microvu Programs\nada.iwp
cd "C:\Microvu Programs\MvRun"
DEL *.iwp /Q /F
powershell -command "$mvRunProcess = Get-Process -Name MvRun* -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }; if ($mvRunProcess) { (New-Object -ComObject wscript.shell).AppActivate($mvRunProcess.Id)}"