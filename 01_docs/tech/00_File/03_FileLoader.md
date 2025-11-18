# FileLoader 클래스

## 개요
파일 로드 클래스는 이미지 파일을 불러오는 기능을 담당하는 단일 책임 클래스입니다. SOLID 원칙의 Single Responsibility Principle을 따릅니다.

## 위치
`Final_ImageProcessing/image_processor/file_operations.py`

## 클래스 정의
```python
class FileLoader:
    """파일 로드 클래스 (단일 책임: 파일 로드)"""
```

## 메서드

### `load(file_path: str) -> Optional[numpy.ndarray]`
이미지 파일을 로드합니다.

**매개변수:**
- `file_path (str)`: 로드할 파일 경로

**반환값:**
- `Optional[numpy.ndarray]`: 로드된 이미지 배열, 실패 시 `None`

**동작 방식:**
1. `cv2.imread()`를 사용하여 이미지를 로드합니다
2. 로드 실패 시 콘솔에 오류 메시지를 출력하고 `None`을 반환합니다

**예외 처리:**
- 예외 발생 시 콘솔에 오류 메시지를 출력하고 `None`을 반환합니다

**예제:**
```python
from image_processor import file_operations

loader = file_operations.FileLoader()
image = loader.load("test.jpg")
if image is not None:
    print(f"이미지 로드 성공: {image.shape}")
else:
    print("이미지 로드 실패")
```

---

### `load_from_dialog(default_path: str = None) -> Tuple[Optional[str], Optional[numpy.ndarray]]`
파일 다이얼로그를 통한 이미지 로드입니다.

**매개변수:**
- `default_path (str, optional)`: 기본 경로 (선택)

**반환값:**
- `Tuple[Optional[str], Optional[numpy.ndarray]]`: (파일 경로, 이미지) 튜플
  - 파일 선택 시: (파일 경로, 이미지 배열)
  - 취소 시: (None, None)
  - 로드 실패 시: (파일 경로, None)

**동작 방식:**
1. PyQt5의 `QFileDialog.getOpenFileName()`을 사용하여 파일 선택 다이얼로그를 표시합니다
2. 사용자가 파일을 선택하면 `load()` 메서드를 호출하여 이미지를 로드합니다
3. 파일 경로와 이미지를 튜플로 반환합니다

**지원 파일 형식:**
- JPG, JPEG, PNG, BMP, TIFF

**예제:**
```python
from image_processor import file_operations

loader = file_operations.FileLoader()
file_path, image = loader.load_from_dialog("C:/Users/Default/")

if file_path and image is not None:
    print(f"로드 성공: {file_path}")
    print(f"이미지 크기: {image.shape}")
elif file_path:
    print(f"로드 실패: {file_path}")
else:
    print("파일 선택 취소됨")
```

## 사용 예제

### 기본 로드
```python
from image_processor import file_operations
import cv2

loader = file_operations.FileLoader()
image = loader.load("test.jpg")

if image is not None:
    # 이미지 처리
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", gray)
    cv2.waitKey(0)
```

### 다이얼로그를 통한 로드
```python
from image_processor import file_operations

loader = file_operations.FileLoader()
file_path, image = loader.load_from_dialog()

if file_path and image is not None:
    print(f"선택된 파일: {file_path}")
    print(f"이미지 크기: {image.shape}")
```

### 에러 처리
```python
from image_processor import file_operations

loader = file_operations.FileLoader()

# 존재하지 않는 파일 로드 시도
image = loader.load("nonexistent.jpg")
if image is None:
    print("파일을 찾을 수 없습니다")
```

## SOLID 원칙 적용

### Single Responsibility Principle (SRP)
- `FileLoader`는 파일 로드 기능만 담당합니다.
- 파일 저장이나 히스토리 관리는 다른 클래스가 담당합니다.

### Static Method 사용
- 모든 메서드가 `@staticmethod`로 선언되어 있어 인스턴스 생성 없이 사용할 수 있습니다.
- 상태를 가지지 않는 순수 함수로 설계되었습니다.

## 주의사항

1. **OpenCV 이미지 형식**: OpenCV는 BGR 형식으로 이미지를 로드합니다. RGB로 변환이 필요한 경우 `cv2.cvtColor(image, cv2.COLOR_BGR2RGB)`를 사용하세요.

2. **파일 경로**: Windows와 Linux/Mac의 경로 구분자가 다릅니다. `os.path.join()`을 사용하여 경로를 구성하는 것이 좋습니다.

3. **메모리 관리**: 큰 이미지를 로드할 때는 메모리 사용량을 고려하세요.

