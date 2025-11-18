# SettingsManager 클래스

## 개요
설정 관리 클래스는 애플리케이션의 설정을 관리하는 단일 책임 클래스입니다. 현재는 기본 구조만 제공되며, 추후 확장 예정입니다.

## 위치
`Final_ImageProcessing/image_processor/file_operations.py`

## 클래스 정의
```python
class SettingsManager:
    """설정 관리 클래스 (단일 책임: 애플리케이션 설정 관리)"""
```

## 생성자

### `__init__(self)`
설정 관리자를 초기화합니다.

**초기화:**
- `settings = {}`: 빈 딕셔너리로 설정 저장소를 초기화합니다

**예제:**
```python
from image_processor import file_operations

settings_manager = file_operations.SettingsManager()
```

## 메서드

### `get_setting(self, key: str, default=None)`
설정 값을 가져옵니다.

**매개변수:**
- `key (str)`: 설정 키
- `default`: 기본값 (키가 없을 때 반환할 값)

**반환값:**
- 설정 값 또는 기본값

**예제:**
```python
from image_processor import file_operations

settings_manager = file_operations.SettingsManager()

# 설정 가져오기
theme = settings_manager.get_setting("theme", "dark")
print(f"현재 테마: {theme}")
```

---

### `set_setting(self, key: str, value)`
설정 값을 설정합니다.

**매개변수:**
- `key (str)`: 설정 키
- `value`: 설정 값

**예제:**
```python
from image_processor import file_operations

settings_manager = file_operations.SettingsManager()

# 설정 저장
settings_manager.set_setting("theme", "dark")
settings_manager.set_setting("language", "ko")
settings_manager.set_setting("auto_save", True)
```

---

### `show_settings_dialog(self)`
설정 다이얼로그를 표시합니다.

**동작:**
- 현재는 정보 메시지 박스만 표시합니다
- 추후 실제 설정 다이얼로그로 확장 예정입니다

**예제:**
```python
from image_processor import file_operations

settings_manager = file_operations.SettingsManager()
settings_manager.show_settings_dialog()
```

## 사용 예제

### 기본 사용
```python
from image_processor import file_operations

settings_manager = file_operations.SettingsManager()

# 설정 저장
settings_manager.set_setting("window_width", 1600)
settings_manager.set_setting("window_height", 900)
settings_manager.set_setting("default_image_dir", "images/")

# 설정 읽기
width = settings_manager.get_setting("window_width", 800)
height = settings_manager.get_setting("window_height", 600)
image_dir = settings_manager.get_setting("default_image_dir", "./")
```

### 설정 파일 저장/로드 (확장 예정)
```python
import json
import os
from image_processor import file_operations

class ExtendedSettingsManager(file_operations.SettingsManager):
    def __init__(self, config_file="config.json"):
        super().__init__()
        self.config_file = config_file
        self.load_settings()
    
    def load_settings(self):
        """설정 파일에서 로드"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
    
    def save_settings(self):
        """설정 파일에 저장"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)

# 사용
settings_manager = ExtendedSettingsManager()
settings_manager.set_setting("theme", "dark")
settings_manager.save_settings()
```

## SOLID 원칙 적용

### Single Responsibility Principle (SRP)
- `SettingsManager`는 설정 관리 기능만 담당합니다.
- 실제 설정 저장/로드는 추후 확장 가능하도록 설계되었습니다.

### Open/Closed Principle (OCP)
- 기본 클래스는 확장 가능하도록 설계되었습니다.
- 새로운 설정 타입을 추가하려면 상속을 통해 확장할 수 있습니다.

## 향후 확장 계획

1. **파일 기반 저장**: JSON 또는 INI 파일로 설정을 저장/로드
2. **설정 다이얼로그**: PyQt5를 사용한 실제 설정 UI
3. **설정 검증**: 설정 값의 유효성 검사
4. **설정 그룹**: 관련 설정을 그룹화하여 관리

