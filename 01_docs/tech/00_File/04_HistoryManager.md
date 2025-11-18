# HistoryManager 클래스

## 개요
히스토리 관리 클래스는 되돌리기(Undo)와 앞으로 돌리기(Redo) 기능을 관리하는 단일 책임 클래스입니다. `FileManager`의 히스토리 기능을 래핑하여 제공합니다.

## 위치
`Final_ImageProcessing/image_processor/file_operations.py`

## 클래스 정의
```python
class HistoryManager:
    """히스토리 관리 클래스 (단일 책임: 되돌리기/앞으로 돌리기 관리)"""
```

## 생성자

### `__init__(self, file_manager: FileManager)`
히스토리 관리자를 초기화합니다.

**매개변수:**
- `file_manager (FileManager)`: 파일 관리자 인스턴스

**예제:**
```python
from image_processor import file_operations

file_manager = file_operations.FileManager()
history_manager = file_operations.HistoryManager(file_manager)
```

## 메서드

### `undo(self) -> Optional[numpy.ndarray]`
되돌리기를 수행합니다.

**반환값:**
- `Optional[numpy.ndarray]`: 이전 이미지의 복사본, 되돌리기 불가능하면 `None`

**동작 방식:**
1. `FileManager.get_undo_image()`를 호출하여 이전 이미지를 가져옵니다
2. 히스토리 인덱스가 자동으로 감소합니다

**예제:**
```python
from image_processor import file_operations
import cv2

file_manager = file_operations.FileManager()
history_manager = file_operations.HistoryManager(file_manager)

# 이미지 로드 및 히스토리에 추가
image = cv2.imread("test.jpg")
file_manager.add_to_history(image)

# 이미지 처리 후 히스토리에 추가
processed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
file_manager.add_to_history(processed)

# 되돌리기
previous = history_manager.undo()
if previous is not None:
    print("이전 이미지로 복원됨")
```

---

### `redo(self) -> Optional[numpy.ndarray]`
앞으로 돌리기를 수행합니다.

**반환값:**
- `Optional[numpy.ndarray]`: 다음 이미지의 복사본, 앞으로 돌리기 불가능하면 `None`

**동작 방식:**
1. `FileManager.get_redo_image()`를 호출하여 다음 이미지를 가져옵니다
2. 히스토리 인덱스가 자동으로 증가합니다

**예제:**
```python
# 되돌리기 후 앞으로 돌리기
previous = history_manager.undo()
if previous is not None:
    # 다시 앞으로
    next_image = history_manager.redo()
    if next_image is not None:
        print("다음 이미지로 이동됨")
```

---

### `can_undo(self) -> bool`
되돌리기가 가능한지 확인합니다.

**반환값:**
- `bool`: 되돌리기 가능 여부

**예제:**
```python
if history_manager.can_undo():
    print("되돌리기 가능")
    previous = history_manager.undo()
else:
    print("되돌리기 불가능")
```

---

### `can_redo(self) -> bool`
앞으로 돌리기가 가능한지 확인합니다.

**반환값:**
- `bool`: 앞으로 돌리기 가능 여부

**예제:**
```python
if history_manager.can_redo():
    print("앞으로 돌리기 가능")
    next_image = history_manager.redo()
else:
    print("앞으로 돌리기 불가능")
```

## 사용 예제

### 기본 사용
```python
from image_processor import file_operations
import cv2
import numpy as np

# 관리자 생성
file_manager = file_operations.FileManager()
history_manager = file_operations.HistoryManager(file_manager)

# 이미지 로드
image = cv2.imread("test.jpg")
file_manager.add_to_history(image)

# 여러 작업 수행
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
file_manager.add_to_history(gray)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)
file_manager.add_to_history(blurred)

# 되돌리기
if history_manager.can_undo():
    previous = history_manager.undo()  # blurred -> gray
    print("되돌리기 완료")

# 다시 되돌리기
if history_manager.can_undo():
    previous = history_manager.undo()  # gray -> image
    print("한 번 더 되돌리기 완료")

# 앞으로 돌리기
if history_manager.can_redo():
    next_image = history_manager.redo()  # image -> gray
    print("앞으로 돌리기 완료")
```

### UI와 연동
```python
# UI에서 버튼 클릭 시
def on_undo_clicked(self):
    if self.history_manager.can_undo():
        previous_image = self.history_manager.undo()
        if previous_image is not None:
            self.processed_image = previous_image
            self.update_display()
            self.update_undo_redo_buttons()

def on_redo_clicked(self):
    if self.history_manager.can_redo():
        next_image = self.history_manager.redo()
        if next_image is not None:
            self.processed_image = next_image
            self.update_display()
            self.update_undo_redo_buttons()

def update_undo_redo_buttons(self):
    # 버튼 활성화/비활성화
    self.undo_button.setEnabled(self.history_manager.can_undo())
    self.redo_button.setEnabled(self.history_manager.can_redo())
```

## SOLID 원칙 적용

### Single Responsibility Principle (SRP)
- `HistoryManager`는 되돌리기/앞으로 돌리기 기능만 담당합니다.
- 실제 히스토리 저장은 `FileManager`가 담당합니다.

### Dependency Inversion Principle (DIP)
- `HistoryManager`는 `FileManager`에 의존하지만, 구체적인 구현이 아닌 인터페이스에 의존합니다.
- `FileManager`의 히스토리 관리 메서드를 사용하여 결합도를 낮췄습니다.

## 주의사항

1. **히스토리 크기**: 기본 최대 히스토리 크기는 50입니다. 큰 이미지의 경우 메모리 사용량이 증가할 수 있습니다.

2. **새로운 작업 시**: 새로운 작업을 수행하면 현재 인덱스 이후의 히스토리가 제거됩니다.

3. **이미지 복사**: 히스토리에 저장되는 이미지는 복사본입니다. 원본 이미지를 수정해도 히스토리에 영향을 주지 않습니다.

