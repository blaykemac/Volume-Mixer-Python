venv\Scripts\pyinstaller.exe --onefile --hidden-import pkg_resources --hidden-import infi.systray --icon="VolumeIcon.ico" --clean source\VolumeMixer.pyw
echo "Done compiling."
pause