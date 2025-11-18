# UI 아키텍처 문서

## 개요

이미지 편집기 UI는 PyQt5를 기반으로 하며, SOLID 원칙에 따라 모듈화되어 있습니다.

## 디렉토리 구조

```
Final_ImageProcessing/
├── main.py                          # 메인 애플리케이션
└── image_processor/
    └── UI/
        ├── __init__.py              # UI 모듈 초기화
        ├── constants.py              # UI 상수 정의
        ├── components.py             # OpenCV 기반 UI 컴포넌트 (레거시)
        ├── layout.py                 # 레이아웃 관리 (레거시)
        ├── renderer.py               # 렌더링 관리 (레거시)
        ├── event_handler.py          # 이벤트 처리 (레거시)
        └── settings_panel.py         # PyQt5 설정 패널 모듈
```

## 모듈 설명

### main.py
메인 애플리케이션 파일로, 다음을 포함합니다:
- `ImageDisplayWidget`: 이미지 표시 위젯
- `FileListWidget`: 파일 리스트 위젯
- `ImageEditor`: 메인 윈도우 클래스

### image_processor/UI/

#### constants.py
UI 관련 상수 정의:
- 색상 정의
- 창 크기
- 레이아웃 상수
- 탭 정의
- 메뉴 항목

#### settings_panel.py
PyQt5 기반 설정 패널 모듈:
- `SettingsPanel`: 메인 설정 패널
- `PixelSettings`: Pixel 처리 설정
- `AreaSettings`: Area 처리 설정
- `GeometricSettings`: Geometric 처리 설정

#### components.py, layout.py, renderer.py, event_handler.py
OpenCV 기반 UI 모듈 (레거시):
- 초기 OpenCV UI 구현 시 사용
- 현재는 PyQt5로 전환되어 사용되지 않음
- 참고용으로 유지

## UI 구조

```
ImageEditor (QMainWindow)
├── Left Panel (FileListWidget)
│   └── 파일 리스트
├── Right Panel
│   ├── Top Bar (MenuBar + Tab Buttons)
│   ├── Info Bar (파일 정보)
│   ├── Image Display (ImageDisplayWidget)
│   └── Settings Panel (SettingsPanel)
│       ├── PixelSettings (현재 탭에 따라 표시/숨김)
│       ├── AreaSettings (현재 탭에 따라 표시/숨김)
│       ├── GeometricSettings (현재 탭에 따라 표시/숨김)
│       └── RESET Button
```

## 주요 컴포넌트

### ImageDisplayWidget
- 이미지 표시 및 드래그 기능
- OpenCV 이미지를 QPixmap으로 변환하여 표시
- 스케일 조정 및 중앙 정렬

### FileListWidget
- 파일 리스트 표시
- 드래그 앤 드롭 지원
- 파일 선택 시 이미지 로드

### SettingsPanel
- 하단 설정 패널 (280px 높이)
- 탭별 설정 위젯 관리
- RESET 버튼 포함

## SOLID 원칙 적용

### Single Responsibility Principle
각 클래스는 단일 책임을 가집니다:
- `SettingsPanel`: 설정 패널 레이아웃 관리
- `PixelSettings`: Pixel 처리 컨트롤 관리
- `AreaSettings`: Area 처리 컨트롤 관리
- `GeometricSettings`: Geometric 처리 컨트롤 관리

### Open/Closed Principle
- 새로운 설정 위젯 추가 시 기존 코드 수정 없이 확장 가능
- Getter 메서드를 통한 인터페이스 제공

### Dependency Inversion Principle
- `main.py`는 구체적인 구현이 아닌 인터페이스를 통해 위젯에 접근
- Getter 메서드를 통한 결합도 감소

## 이벤트 흐름

1. 사용자가 탭 클릭
   - `on_tab_clicked()` 호출
   - `update_settings_visibility()` 호출
   - `SettingsPanel.set_current_tab()` 호출
   - 해당 탭의 설정 위젯만 표시

2. 사용자가 슬라이더 조작
   - 슬라이더의 `valueChanged` 시그널 발생
   - `on_slider_changed()` 호출
   - `apply_all_effects()` 호출
   - 이미지 처리 및 표시 업데이트

3. 사용자가 버튼 클릭
   - 버튼의 `clicked` 시그널 발생
   - `on_button_toggled()` 호출
   - `apply_all_effects()` 호출
   - 이미지 처리 및 표시 업데이트

## 스타일 가이드

### 색상 스키마
- 배경색: `#282828`, `#323232`
- 텍스트 색상: `#dcdcdc`
- 하이라이트: `#0096ff` (파란색)
- 활성 버튼: `#00c800` (녹색)
- RESET 버튼: `#b43228` (빨간색)

### 크기
- 설정 패널 높이: 280px
- 파일 리스트 너비: 250px
- 상단 바 높이: 40px
- 정보 바 높이: 30px

## 확장 가이드

### 새로운 설정 위젯 추가
1. `settings_panel.py`에 새로운 설정 클래스 생성
2. `SettingsPanel.init_ui()`에 위젯 추가
3. `SettingsPanel.update_visibility()`에 가시성 로직 추가
4. `main.py`의 `create_settings_panel()`에서 이벤트 연결

### 새로운 탭 추가
1. `constants.py`의 `TABS`에 탭 이름 추가
2. `constants.py`의 `MENU_ITEMS`에 메뉴 항목 추가
3. `main.py`의 `create_top_bar()`에 탭 버튼 추가
4. 새로운 설정 위젯 클래스 생성 및 연결

## 참고 문서
- [SettingsPanel.md](./SettingsPanel.md): 설정 패널 상세 문서
- [UITech.md](./UITech.md): 초기 UI 기술 문서 (레거시)
- [Main.md](./Main.md): 메인 UI 문서

