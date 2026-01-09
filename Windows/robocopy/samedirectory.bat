robocopy "Windows\cmd\tests" "Windows\cmd\tests copy" /E /L /COPY:DAT /R:0 /W:0

@REM robocopy: The command itself.
@REM "Windows\cmd\tests": The source directory. Quotation marks are good practice for paths, though not strictly necessary here.
@REM "Windows\cmd\tests copy": The destination directory. The space in the name requires quotation marks.
@REM /E: Copies subdirectories, including empty ones [1].
@REM /L: List only — specifies that files are to be listed, but not actually copied, moved, or deleted [1]. This is useful for previewing what the copy operation would do.
@REM /R:0: Specifies zero retries on failed copies (the default is 1 million) [1].
@REM /W:0: Specifies zero wait time between retries (the default is 30 seconds) [1]. 
@REM This command will list the files that would be copied from Windows\cmd\tests to Windows\cmd\tests copy without actually performing the copy. 