@echo off
chcp 65001 >nul
echo ====================================
echo Image Editor EXE 빌드 스크립트 (고급 모드)
echo 모든 의존성을 포함하여 더 안정적인 빌드
echo ====================================
echo.

REM 현재 디렉토리 확인
cd /d "%~dp0"
echo 현재 디렉토리: %CD%
echo.

REM 가상환경 활성화 (있는 경우)
if exist "..\venv\Scripts\activate.bat" (
    echo [1/5] 가상환경 활성화 중...
    call ..\venv\Scripts\activate.bat
    echo.
)

REM PyInstaller 설치 확인 및 설치
echo [2/5] PyInstaller 설치 확인 중...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller가 설치되어 있지 않습니다. 설치 중...
    pip install pyinstaller
    if errorlevel 1 (
        echo 오류: PyInstaller 설치 실패
        pause
        exit /b 1
    )
    echo PyInstaller 설치 완료!
) else (
    echo PyInstaller가 이미 설치되어 있습니다.
)
echo.

REM 기존 빌드 파일 정리
echo [3/5] 기존 빌드 파일 정리 중...
if exist "build" (
    echo build 폴더 삭제 중...
    rmdir /s /q build
)
if exist "dist" (
    echo dist 폴더 삭제 중...
    rmdir /s /q dist
)
if exist "*.spec" (
    echo 기존 spec 파일 삭제 중...
    del /q *.spec
)
echo 정리 완료!
echo.

REM PyInstaller 실행 (고급 옵션)
echo [4/5] EXE 파일 생성 중 (고급 모드)...
echo 이 과정은 몇 분 정도 걸릴 수 있습니다...
echo 모든 의존성을 수집하고 있습니다...
echo.
pyinstaller --name="ImageEditor" ^
    --onefile ^
    --windowed ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --hidden-import=image_processor ^
    --hidden-import=image_processor.pixel_processing ^
    --hidden-import=image_processor.area_processing ^
    --hidden-import=image_processor.geometric_processing ^
    --hidden-import=image_processor.file_operations ^
    --hidden-import=image_processor.UI.settings_panel ^
    --collect-all=PyQt5 ^
    --collect-all=cv2 ^
    --noconfirm ^
    --clean ^
    main.py

if errorlevel 1 (
    echo.
    echo ====================================
    echo 오류 발생!
    echo ====================================
    echo 빌드 중 오류가 발생했습니다.
    echo 오류 메시지를 확인하세요.
    pause
    exit /b 1
)

echo.
echo [5/5] 빌드 완료!
echo.
echo ====================================
echo 빌드 성공!
echo ====================================
echo.
echo EXE 파일 위치: dist\ImageEditor.exe
echo.
if exist "dist\ImageEditor.exe" (
    echo 파일 크기 확인 중...
    for %%A in ("dist\ImageEditor.exe") do (
        set /a size_mb=%%~zA/1048576
        echo 파일 크기: %%~zA bytes (약 !size_mb! MB)
    )
    echo.
    echo 테스트: dist\ImageEditor.exe 파일을 더블클릭하여 실행해보세요!
) else (
    echo 경고: EXE 파일을 찾을 수 없습니다!
)
echo.
echo ====================================
echo.
echo 참고: 고급 모드는 더 많은 의존성을 포함하므로
echo 파일 크기가 더 클 수 있습니다. 하지만 더 안정적입니다.
echo.
pause

