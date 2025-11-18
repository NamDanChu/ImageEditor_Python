# 설정 패널 (Settings Panel) 문서

## 개요

설정 패널은 이미지 처리 기능을 제어하는 하단 패널입니다. SOLID 원칙에 따라 모듈화되어 있으며, 각 처리 카테고리(Pixel, Area, Geometric)별로 독립적인 설정 위젯으로 구성됩니다.

## 구조

### 파일 위치
- `Final_ImageProcessing/image_processor/UI/settings_panel.py`

### 클래스 구조

```
SettingsPanel (메인 패널)
├── PixelSettings (Pixel 처리 설정)
├── AreaSettings (Area 처리 설정)
└── GeometricSettings (Geometric 처리 설정)
```

## 클래스 상세

### SettingsPanel

**책임**: 설정 패널의 레이아웃 관리 및 탭별 가시성 제어

**주요 메서드**:
- `init_ui()`: UI 초기화
- `set_current_tab(tab_name)`: 현재 탭 설정 및 가시성 업데이트
- `update_visibility()`: 설정 위젯 가시성 업데이트
- `get_reset_button()`: RESET 버튼 반환
- `get_pixel_settings()`: Pixel 설정 위젯 반환
- `get_area_settings()`: Area 설정 위젯 반환
- `get_geometric_settings()`: Geometric 설정 위젯 반환

**속성**:
- `current_tab`: 현재 활성화된 탭 ('Pixel', 'Area', 'Geometric')
- `pixel_settings`: PixelSettings 인스턴스
- `area_settings`: AreaSettings 인스턴스
- `geometric_settings`: GeometricSettings 인스턴스

**크기**: 고정 높이 280px (기존 180px에서 확대)

### PixelSettings

**책임**: Pixel 처리 관련 컨트롤 관리

**제공하는 컨트롤**:
- Grayscale 버튼 (토글)
- Invert 버튼 (토글)
- Brightness 슬라이더 (0-200, 기본값: 0)
- Contrast 슬라이더 (0-200, 기본값: 100)
- Threshold 슬라이더 (0-255, 기본값: 127)

**주요 메서드**:
- `get_grayscale_button()`: Grayscale 버튼 반환
- `get_invert_button()`: Invert 버튼 반환
- `get_brightness_slider()`: Brightness 슬라이더 반환
- `get_contrast_slider()`: Contrast 슬라이더 반환
- `get_threshold_slider()`: Threshold 슬라이더 반환

### AreaSettings

**책임**: Area 처리 관련 컨트롤 관리

**제공하는 컨트롤**:
- Blur 슬라이더 (0-20, 기본값: 0)
- Canny Low 슬라이더 (0-255, 기본값: 50)
- Canny High 슬라이더 (0-255, 기본값: 150)
- Sharpen 슬라이더 (0-100, 기본값: 0)

**주요 메서드**:
- `get_blur_slider()`: Blur 슬라이더 반환
- `get_canny_low_slider()`: Canny Low 슬라이더 반환
- `get_canny_high_slider()`: Canny High 슬라이더 반환
- `get_sharpen_slider()`: Sharpen 슬라이더 반환

### GeometricSettings

**책임**: Geometric 처리 관련 컨트롤 관리

**제공하는 컨트롤**:
- Flip H 버튼 (토글)
- Flip V 버튼 (토글)
- Rotation 슬라이더 (0-360, 기본값: 0)
- Resize W 슬라이더 (10-200, 기본값: 100)
- Resize H 슬라이더 (10-200, 기본값: 100)

**주요 메서드**:
- `get_flip_h_button()`: Flip H 버튼 반환
- `get_flip_v_button()`: Flip V 버튼 반환
- `get_rotation_slider()`: Rotation 슬라이더 반환
- `get_resize_w_slider()`: Resize W 슬라이더 반환
- `get_resize_h_slider()`: Resize H 슬라이더 반환

## SOLID 원칙 적용

### Single Responsibility Principle (단일 책임 원칙)
- `SettingsPanel`: 설정 패널 레이아웃 관리만 담당
- `PixelSettings`: Pixel 처리 컨트롤만 담당
- `AreaSettings`: Area 처리 컨트롤만 담당
- `GeometricSettings`: Geometric 처리 컨트롤만 담당

### Open/Closed Principle (개방-폐쇄 원칙)
- 새로운 설정 위젯을 추가하려면 새로운 클래스를 생성하고 `SettingsPanel`에 추가
- 기존 코드 수정 없이 확장 가능

### Dependency Inversion Principle (의존성 역전 원칙)
- `main.py`는 구체적인 구현이 아닌 인터페이스(메서드)를 통해 위젯에 접근
- Getter 메서드를 통해 위젯에 접근하여 결합도 감소

## 사용 예시

```python
from image_processor.UI.settings_panel import SettingsPanel

# 설정 패널 생성
settings_panel = SettingsPanel()

# RESET 버튼 연결
reset_btn = settings_panel.get_reset_button()
reset_btn.clicked.connect(on_reset_clicked)

# Pixel 설정 위젯 사용
pixel_settings = settings_panel.get_pixel_settings()
grayscale_btn = pixel_settings.get_grayscale_button()
grayscale_btn.clicked.connect(on_grayscale_toggled)

brightness_slider = pixel_settings.get_brightness_slider()
brightness_slider.valueChanged.connect(on_brightness_changed)

# 탭 변경
settings_panel.set_current_tab('Area')  # Area 탭으로 전환
```

## 스타일

### 패널 스타일
- 배경색: `#282828`
- 상단 테두리: `2px solid #404040`
- 고정 높이: `280px`

### 버튼 스타일
- 기본 배경색: `#505050`
- 호버 배경색: `#606060`
- 활성화 배경색: `#00c800` (녹색)
- RESET 버튼 배경색: `#b43228` (빨간색)

### 슬라이더 그룹 스타일
- QGroupBox로 구성
- 테두리: `1px solid #404040`
- 텍스트 색상: `#dcdcdc`

## 변경 이력

- 2024: 초기 구현 (180px 높이)
- 2024: 크기 확대 (280px 높이)
- 2024: SOLID 원칙에 맞게 모듈화

