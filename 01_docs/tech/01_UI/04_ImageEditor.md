# ImageEditor 클래스

## 개요
이미지 편집기의 메인 윈도우 클래스입니다. 모든 UI 요소와 이미지 처리를 관리합니다.

## 위치
`Final_ImageProcessing/main.py`

## 클래스 정의
```python
class ImageEditor(QMainWindow):
    """이미지 편집기 메인 윈도우"""
```

## 주요 메서드

### `init_ui(self)`
UI를 초기화합니다.

### `create_left_panel(self)`
왼쪽 파일 리스트 패널을 생성합니다.

### `create_top_bar(self)`
상단 메뉴바를 생성합니다.

### `create_settings_panel(self)`
하단 설정 패널을 생성합니다.

### `apply_all_effects(self)`
모든 이미지 처리 효과를 적용합니다.

### `on_file_menu_action(self, action)`
File 메뉴 액션을 처리합니다.

## 주요 속성

- `original_image`: 원본 이미지
- `processed_image`: 처리된 이미지
- `file_manager`: 파일 관리자
- `history_manager`: 히스토리 관리자

