# ApplicationManager 클래스

## 개요
애플리케이션 관리 클래스는 애플리케이션 종료 기능을 담당하는 단일 책임 클래스입니다.

## 위치
`Final_ImageProcessing/image_processor/file_operations.py`

## 클래스 정의
```python
class ApplicationManager:
    """애플리케이션 관리 클래스 (단일 책임: 애플리케이션 종료 관리)"""
```

## 메서드

### `exit_application() -> None`
애플리케이션을 종료합니다.

**동작 방식:**
1. PyQt5의 `QApplication.quit()`를 호출하여 애플리케이션을 종료합니다
2. 모든 창이 닫히고 이벤트 루프가 종료됩니다

**예제:**
```python
from image_processor import file_operations

# 애플리케이션 종료
file_operations.ApplicationManager.exit_application()
```

## 사용 예제

### 기본 사용
```python
from image_processor import file_operations

# 종료 버튼 클릭 시
def on_exit_clicked(self):
    file_operations.ApplicationManager.exit_application()
```

### 종료 전 확인
```python
from PyQt5.QtWidgets import QMessageBox
from image_processor import file_operations

def on_exit_clicked(self):
    reply = QMessageBox.question(
        None,
        '종료 확인',
        '정말 종료하시겠습니까?',
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        file_operations.ApplicationManager.exit_application()
```

### 저장되지 않은 변경사항 확인
```python
from PyQt5.QtWidgets import QMessageBox
from image_processor import file_operations

def on_exit_clicked(self):
    if self.has_unsaved_changes():
        reply = QMessageBox.question(
            None,
            '저장되지 않은 변경사항',
            '저장되지 않은 변경사항이 있습니다. 종료하시겠습니까?',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Cancel:
            return
        elif reply == QMessageBox.No:
            # 저장 후 종료
            self.save_current_file()
    
    file_operations.ApplicationManager.exit_application()
```

## SOLID 원칙 적용

### Single Responsibility Principle (SRP)
- `ApplicationManager`는 애플리케이션 종료 기능만 담당합니다.
- 다른 기능은 다른 클래스가 담당합니다.

### Static Method 사용
- `exit_application()`은 `@staticmethod`로 선언되어 있어 인스턴스 생성 없이 사용할 수 있습니다.
- 상태를 가지지 않는 순수 함수로 설계되었습니다.

## 주의사항

1. **저장 확인**: 종료 전에 저장되지 않은 변경사항이 있는지 확인하는 것이 좋습니다.

2. **리소스 정리**: 종료 전에 열려있는 파일이나 리소스를 정리해야 합니다.

3. **비동기 작업**: 종료 전에 진행 중인 비동기 작업이 완료되기를 기다려야 할 수 있습니다.

