# FileSaver 클래스

## 개요
파일 저장 클래스는 이미지 파일을 저장하는 기능을 담당하는 단일 책임 클래스입니다. SOLID 원칙의 Single Responsibility Principle을 따릅니다.

## 위치
`Final_ImageProcessing/image_processor/file_operations.py`

## 클래스 정의
```python
class FileSaver:
    """파일 저장 클래스 (단일 책임: 파일 저장)"""
```

## 메서드

### `save(image, file_path: str) -> bool`
이미지를 파일로 저장합니다.

**매개변수:**
- `image (numpy.ndarray)`: 저장할 이미지 배열
- `file_path (str)`: 저장할 파일 경로

**반환값:**
- `bool`: 저장 성공 여부

**동작 방식:**
1. 저장 경로의 디렉토리가 없으면 생성합니다
2. `cv2.imwrite()`를 사용하여 이미지를 저장합니다
3. 저장 성공 여부를 반환합니다

**예외 처리:**
- 예외 발생 시 콘솔에 오류 메시지를 출력하고 `False`를 반환합니다

**예제:**
```python
from image_processor import file_operations
import cv2
import numpy as np

# 이미지 생성
image = np.zeros((100, 100, 3), dtype=np.uint8)

# 저장
saver = file_operations.FileSaver()
success = saver.save(image, "output.jpg")
if success:
    print("저장 성공")
else:
    print("저장 실패")
```

---

### `save_as(image, default_path: str = None) -> Optional[str]`
다른 이름으로 저장 다이얼로그를 통해 이미지를 저장합니다.

**매개변수:**
- `image (numpy.ndarray)`: 저장할 이미지 배열
- `default_path (str, optional)`: 기본 경로 (선택)

**반환값:**
- `Optional[str]`: 저장된 파일 경로, 취소 시 `None`

**동작 방식:**
1. PyQt5의 `QFileDialog.getSaveFileName()`을 사용하여 저장 다이얼로그를 표시합니다
2. 사용자가 파일 경로를 선택하면 `save()` 메서드를 호출하여 저장합니다
3. 저장 성공 시 파일 경로를 반환합니다

**지원 파일 형식:**
- JPG, JPEG, PNG, BMP, TIFF

**예제:**
```python
from image_processor import file_operations
import cv2

# 이미지 로드
image = cv2.imread("input.jpg")

# 다른 이름으로 저장
saver = file_operations.FileSaver()
saved_path = saver.save_as(image, "default.jpg")
if saved_path:
    print(f"저장됨: {saved_path}")
else:
    print("저장 취소됨")
```

## 사용 예제

### 기본 저장
```python
from image_processor import file_operations
import cv2

image = cv2.imread("input.jpg")
saver = file_operations.FileSaver()

# 현재 경로에 저장
success = saver.save(image, "output.jpg")
```

### 다른 이름으로 저장
```python
from image_processor import file_operations
import cv2

image = cv2.imread("input.jpg")
saver = file_operations.FileSaver()

# 다이얼로그를 통한 저장
saved_path = saver.save_as(image, "input.jpg")
if saved_path:
    print(f"새 파일로 저장: {saved_path}")
```

### 에러 처리
```python
from image_processor import file_operations
import numpy as np

image = np.zeros((100, 100, 3), dtype=np.uint8)
saver = file_operations.FileSaver()

# 잘못된 경로로 저장 시도
success = saver.save(image, "/invalid/path/image.jpg")
if not success:
    print("저장 실패 - 경로를 확인하세요")
```

## SOLID 원칙 적용

### Single Responsibility Principle (SRP)
- `FileSaver`는 파일 저장 기능만 담당합니다.
- 파일 로드나 히스토리 관리는 다른 클래스가 담당합니다.

### Static Method 사용
- 모든 메서드가 `@staticmethod`로 선언되어 있어 인스턴스 생성 없이 사용할 수 있습니다.
- 상태를 가지지 않는 순수 함수로 설계되었습니다.

