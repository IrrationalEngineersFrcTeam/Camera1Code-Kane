@echo off
title Deploy Python code to Raspberry Pi
@echo off

"C:\Program Files (x86)\WinSCP\WinSCP.com" ^
  /log="D:\Users\kthsd2\Documents\Robotics\Vision\Camera1Code-Kane\WinSCP.log" /ini=nul ^
  /command ^
    "open sftp://pi:raspberry@10.62.39.12/ -hostkey=""ssh-ed25519 256 HyWTbWildpUktR38azRhgWLODiJQkNXO5tdu3KgiReM=""" ^
    "put "ShapeDetectionTest.py"" ^
    "put "findshapespipeline.py"" ^
    "put "ShapeDetector.py"" ^
	"exit"

set WINSCP_RESULT=%ERRORLEVEL%
if %WINSCP_RESULT% equ 0 (
  echo Success
) else (
  echo Error
)
echo Done

exit /b %WINSCP_RESULT%

putty -ssh pi@10.62.39.12 -pw raspberry -m puttyCommands.txt

