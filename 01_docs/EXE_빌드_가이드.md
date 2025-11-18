# Image Editor EXE 파일 생성 가이드

## 📋 목차
1. [EXE 파일 생성 방법](#exe-파일-생성-방법)
2. [단계별 상세 가이드](#단계별-상세-가이드)
3. [문제 해결](#문제-해결)

---

## EXE 파일 생성 방법

### 방법 1: 배치 파일 사용 (가장 쉬움) ⭐ 추천

#### 1단계: 배치 파일 실행
```
Final_ImageProcessing 폴더에서 build_exe.bat 더블클릭
또는
명령 프롬프트에서: build_exe.bat
```

#### 2단계: 완료 대기
- 빌드가 완료될 때까지 기다립니다 (5-10분 소요)
- "빌드 완료!" 메시지가 나오면 끝

#### 3단계: EXE 파일 확인
- `dist` 폴더에 `ImageEditor.exe` 파일이 생성됩니다

---

### 방법 2: 명령어 직접 입력

#### 1단계: PyInstaller 설치
```bash
pip install pyinstaller
```

#### 2단계: 빌드 명령어 실행
```bash
cd Final_ImageProcessing
pyinstaller --name="ImageEditor" --onefile --windowed --add-data "images;images" main.py
```

#### 3단계: 결과 확인
- `dist/ImageEditor.exe` 파일 확인

---

### 방법 3: Spec 파일 사용 (고급)

#### 1단계: Spec 파일 생성
```bash
pyinstaller --name="ImageEditor" --onefile --windowed main.py
```

#### 2단계: Spec 파일 수정
생성된 `ImageEditor.spec` 파일을 편집하여 설정 조정

#### 3단계: Spec 파일로 빌드
```bash
pyinstaller ImageEditor.spec
```

---

## 단계별 상세 가이드

### 🔧 준비 단계

#### 1. 가상환경 활성화 (선택사항)
```bash
# 가상환경이 있다면
cd Final_ImageProcessing
..\venv\Scripts\activate
```

#### 2. 필요한 패키지 확인
```bash
pip list
# 다음 패키지들이 있어야 합니다:
# - PyQt5
# - opencv-python
# - numpy
# - pyinstaller (없으면 설치)
```

#### 3. PyInstaller 설치
```bash
pip install pyinstaller
```

---

### 🚀 빌드 단계

#### 기본 빌드 (가장 간단)
```bash
pyinstaller --name="ImageEditor" --onefile --windowed main.py
```

#### 완전한 빌드 (모든 의존성 포함) ⭐ 권장
```bash
pyinstaller --name="ImageEditor" ^
    --onefile ^
    --windowed ^
    --add-data "images;images" ^
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
    main.py
```

#### 옵션 설명
- `--name="ImageEditor"`: 생성될 EXE 파일 이름
- `--onefile`: 단일 파일로 생성 (모든 것을 하나의 EXE에 포함)
- `--windowed` 또는 `-w`: 콘솔 창 숨김 (GUI 앱용)
- `--add-data "images;images"`: images 폴더를 포함
- `--hidden-import`: 자동으로 감지되지 않는 모듈 명시
- `--collect-all`: 특정 패키지의 모든 하위 모듈 포함

---

### 📁 빌드 결과

빌드가 완료되면:

```
Final_ImageProcessing/
├── build/              (임시 파일, 삭제 가능)
├── dist/
│   └── ImageEditor.exe (실행 파일 - 이것만 배포!)
├── ImageEditor.spec    (설정 파일, 재빌드 시 사용)
└── main.py
```

**배포할 파일**: `dist/ImageEditor.exe` **하나만** 필요합니다!

---

## 문제 해결

### ❌ 문제 1: "ModuleNotFoundError" 발생

**해결 방법:**
```bash
# 누락된 모듈을 --hidden-import에 추가
pyinstaller --hidden-import=누락된_모듈명 --onefile --windowed main.py
```

또는 고급 빌드 스크립트 사용:
```bash
build_exe_advanced.bat
```

---

### ❌ 문제 2: OpenCV 관련 오류

**해결 방법:**
```bash
# --collect-all=cv2 옵션 추가
pyinstaller --collect-all=cv2 --onefile --windowed main.py
```

---

### ❌ 문제 3: PyQt5 관련 오류

**해결 방법:**
```bash
# --collect-all=PyQt5 옵션 추가
pyinstaller --collect-all=PyQt5 --onefile --windowed main.py
```

---

### ❌ 문제 4: 실행 시 오류 확인이 필요한 경우

**해결 방법:**
```bash
# 콘솔 창을 표시하여 오류 확인
pyinstaller --onefile --console main.py
```

또는
```bash
# 디버그 모드
pyinstaller --onefile --windowed --debug=all main.py
```

---

### ❌ 문제 5: 파일 크기가 너무 큰 경우

**해결 방법 1: 폴더 형태로 생성**
```bash
# --onefile 대신 폴더 형태로 생성 (더 작은 크기)
pyinstaller --name="ImageEditor" --windowed main.py
# 결과: dist/ImageEditor/ 폴더 전체를 배포
```

**해결 방법 2: UPX 압축 사용**
1. UPX 다운로드: https://upx.github.io/
2. UPX를 PATH에 추가
3. 빌드 시 자동으로 압축됨

---

### ❌ 문제 6: 아이콘 추가

**해결 방법:**
1. `.ico` 파일 준비 (예: `icon.ico`)
2. 빌드 명령어에 추가:
```bash
pyinstaller --icon=icon.ico --onefile --windowed main.py
```

---

## 📝 체크리스트

빌드 전 확인사항:
- [ ] Python 가상환경 활성화 (선택사항)
- [ ] PyInstaller 설치됨 (`pip install pyinstaller`)
- [ ] 모든 의존성 설치됨 (`pip install -r requirements.txt`)
- [ ] `main.py`가 정상 실행됨 (`python main.py`)
- [ ] `images` 폴더가 존재함

빌드 후 확인사항:
- [ ] `dist/ImageEditor.exe` 파일이 생성됨
- [ ] EXE 파일이 실행됨 (더블클릭)
- [ ] 이미지 로드가 정상 작동함
- [ ] 모든 기능이 정상 작동함

---

## 🎯 요약

### EXE 파일만으로 실행 가능한가?
**✅ 네, 가능합니다!**
- `--onefile` 옵션 사용 시 모든 의존성이 포함됩니다
- Python 설치 불필요
- 다른 PC에서도 바로 실행 가능

### 가장 쉬운 생성 방법
1. `build_exe.bat` 파일 실행
2. 완료 대기
3. `dist/ImageEditor.exe` 사용

### 배포 방법
- `dist/ImageEditor.exe` 파일 하나만 복사해서 배포
- 받는 사람은 EXE 파일만 더블클릭하면 실행됨

---

## 📚 추가 자료

- PyInstaller 공식 문서: https://pyinstaller.org/
- PyInstaller 옵션 목록: https://pyinstaller.org/en/stable/usage.html

