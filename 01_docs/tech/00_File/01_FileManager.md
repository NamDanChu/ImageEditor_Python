# FileManager 클래스

## 개요
파일 관리자 클래스는 현재 파일 경로와 이미지 히스토리를 관리하는 단일 책임 클래스입니다. SOLID 원칙의 Single Responsibility Principle을 따릅니다.

## 위치
`Final_ImageProcessing/image_processor/file_operations.py`

## 클래스 정의
```python
class FileManager:
    """파일 관리자 클래스 (단일 책임: 파일 저장/로드 관리)"""
```

## 속성

### `current_file_path: Optional[str]`
- 현재 열려있는 파일의 경로를 저장합니다.
- 파일이 열려있지 않으면 `None`입니다.

### `history: list`
- 되돌리기/앞으로 돌리기를 위한 이미지 히스토리 리스트입니다.
- 각 항목은 `numpy.ndarray` 형태의 이미지입니다.

### `history_index: int`
- 현재 히스토리에서의 위치 인덱스입니다.
- -1부터 시작합니다.

### `max_history_size: int`
- 히스토리의 최대 크기입니다.
- 기본값: 50

## 메서드

### `__init__(self)`
생성자 메서드입니다. 모든 속성을 초기화합니다.

**초기화 값:**
- `current_file_path = None`
- `history = []`
- `history_index = -1`
- `max_history_size = 50`

---

### `set_current_file(self, file_path: str)`
현재 파일 경로를 설정합니다.

**매개변수:**
- `file_path (str)`: 설정할 파일 경로

**예제:**
```python
file_manager = FileManager()
file_manager.set_current_file("images/photo.jpg")
```

---

### `get_current_file(self) -> Optional[str]`
현재 파일 경로를 반환합니다.

**반환값:**
- `Optional[str]`: 현재 파일 경로, 파일이 없으면 `None`

**예제:**
```python
current = file_manager.get_current_file()
if current:
    print(f"현재 파일: {current}")
```

---

### `add_to_history(self, image)`
히스토리에 이미지를 추가합니다.

**매개변수:**
- `image (numpy.ndarray)`: 추가할 이미지

**동작 방식:**
1. 현재 인덱스 이후의 히스토리를 제거합니다 (새로운 작업 시)
2. 히스토리에 이미지를 추가합니다
3. 히스토리 인덱스를 증가시킵니다
4. 히스토리 크기가 최대값을 초과하면 가장 오래된 항목을 제거합니다

**예제:**
```python
import numpy as np
image = np.zeros((100, 100, 3), dtype=np.uint8)
file_manager.add_to_history(image)
```

---

### `can_undo(self) -> bool`
되돌리기가 가능한지 확인합니다.

**반환값:**
- `bool`: 되돌리기 가능 여부 (`history_index > 0`)

**예제:**
```python
if file_manager.can_undo():
    print("되돌리기 가능")
```

---

### `can_redo(self) -> bool`
앞으로 돌리기가 가능한지 확인합니다.

**반환값:**
- `bool`: 앞으로 돌리기 가능 여부 (`history_index < len(history) - 1`)

**예제:**
```python
if file_manager.can_redo():
    print("앞으로 돌리기 가능")
```

---

### `get_undo_image(self)`
되돌리기 이미지를 반환합니다.

**반환값:**
- `numpy.ndarray`: 이전 이미지의 복사본, 되돌리기 불가능하면 `None`

**동작 방식:**
1. `can_undo()`로 확인
2. 히스토리 인덱스를 감소시킵니다
3. 해당 인덱스의 이미지 복사본을 반환합니다

**예제:**
```python
undo_image = file_manager.get_undo_image()
if undo_image is not None:
    # 이전 이미지로 복원
    processed_image = undo_image
```

---

### `get_redo_image(self)`
앞으로 돌리기 이미지를 반환합니다.

**반환값:**
- `numpy.ndarray`: 다음 이미지의 복사본, 앞으로 돌리기 불가능하면 `None`

**동작 방식:**
1. `can_redo()`로 확인
2. 히스토리 인덱스를 증가시킵니다
3. 해당 인덱스의 이미지 복사본을 반환합니다

**예제:**
```python
redo_image = file_manager.get_redo_image()
if redo_image is not None:
    # 다음 이미지로 이동
    processed_image = redo_image
```

## 사용 예제

```python
from image_processor import file_operations
import cv2

# FileManager 생성
file_manager = file_operations.FileManager()

# 이미지 로드
image = cv2.imread("test.jpg")
file_manager.set_current_file("test.jpg")

# 히스토리에 추가
file_manager.add_to_history(image)

# 이미지 처리 후 다시 히스토리에 추가
processed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
file_manager.add_to_history(processed)

# 되돌리기
if file_manager.can_undo():
    previous = file_manager.get_undo_image()
    print("이전 이미지로 복원됨")

# 앞으로 돌리기
if file_manager.can_redo():
    next_image = file_manager.get_redo_image()
    print("다음 이미지로 이동됨")
```

## SOLID 원칙 적용

### Single Responsibility Principle (SRP)
- `FileManager`는 파일 경로와 히스토리 관리만 담당합니다.
- 실제 파일 저장/로드는 `FileSaver`와 `FileLoader`가 담당합니다.

### Open/Closed Principle (OCP)
- 새로운 히스토리 관리 방식을 추가하려면 상속이나 확장을 통해 구현할 수 있습니다.

### Dependency Inversion Principle (DIP)
- `HistoryManager`가 `FileManager`에 의존하지만, 인터페이스를 통해 결합도를 낮췄습니다.

