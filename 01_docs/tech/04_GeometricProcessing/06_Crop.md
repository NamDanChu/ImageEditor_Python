# apply_crop 함수

## 개요
이미지의 특정 영역만 잘라내는 함수입니다.

## 위치
`Final_ImageProcessing/image_processor/geometric_processing.py`

## 함수 정의
```python
def apply_crop(img, x, y, width, height):
    """이미지 자르기
    x, y: 시작 좌표 (픽셀)
    width: 자를 너비 (픽셀)
    height: 자를 높이 (픽셀)
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `x (int)`
- 시작 x 좌표 (픽셀)
- 0부터 시작 (왼쪽 상단)

### `y (int)`
- 시작 y 좌표 (픽셀)
- 0부터 시작 (왼쪽 상단)

### `width (int)`
- 자를 너비 (픽셀)
- 1 이상

### `height (int)`
- 자를 높이 (픽셀)
- 1 이상

## 반환값
- `numpy.ndarray`: 잘린 이미지 배열
- 지정된 크기의 이미지

## 동작 원리

1. **범위 검증**: 좌표와 크기를 이미지 범위 내로 제한합니다
   ```python
   x = max(0, min(x, w - 1))
   y = max(0, min(y, h - 1))
   width = max(1, min(width, w - x))
   height = max(1, min(height, h - y))
   ```

2. **이미지 자르기**: NumPy 배열 슬라이싱을 사용합니다
   ```python
   return img[y:y+height, x:x+width].copy()
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import geometric_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 중앙 영역 자르기
h, w = image.shape[:2]
center_x = w // 2
center_y = h // 2
crop_width = w // 2
crop_height = h // 2

cropped = geometric_processing.apply_crop(
    image,
    center_x - crop_width // 2,
    center_y - crop_height // 2,
    crop_width,
    crop_height
)

cv2.imshow("Original", image)
cv2.imshow("Cropped", cropped)
cv2.waitKey(0)
```

### 다양한 영역 자르기
```python
from image_processor import geometric_processing
import cv2

image = cv2.imread("test.jpg")
h, w = image.shape[:2]

# 왼쪽 상단
crop1 = geometric_processing.apply_crop(image, 0, 0, w//2, h//2)

# 오른쪽 상단
crop2 = geometric_processing.apply_crop(image, w//2, 0, w//2, h//2)

# 왼쪽 하단
crop3 = geometric_processing.apply_crop(image, 0, h//2, w//2, h//2)

# 오른쪽 하단
crop4 = geometric_processing.apply_crop(image, w//2, h//2, w//2, h//2)

cv2.imshow("Crop 1", crop1)
cv2.imshow("Crop 2", crop2)
cv2.imshow("Crop 3", crop3)
cv2.imshow("Crop 4", crop4)
cv2.waitKey(0)
```

## 수학적 설명

자르기는 NumPy 배열 슬라이싱을 사용합니다:

```
I_out = I_in[y:y+height, x:x+width]
```

여기서:
- `I_in`: 입력 이미지
- `I_out`: 잘린 이미지
- `(x, y)`: 시작 좌표
- `width, height`: 자를 크기

## 활용 사례

1. **관심 영역 추출**: 이미지의 특정 부분만 추출
2. **데이터 증강**: 다양한 영역을 잘라 학습 데이터 생성
3. **전처리**: 일부 알고리즘은 특정 크기의 이미지를 요구
4. **이미지 편집**: 사용자가 선택한 영역만 편집

## 주의사항

1. **범위 검증**: 함수가 자동으로 좌표와 크기를 이미지 범위 내로 제한합니다.

2. **복사본**: `.copy()`를 사용하여 원본 이미지가 변경되지 않도록 합니다.

3. **좌표 시스템**: OpenCV는 (y, x) 순서를 사용하지만, 이 함수는 (x, y) 순서를 사용합니다.

4. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원합니다.

5. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

## 관련 함수

- `apply_resize()`: 크기 조절
- `apply_translate()`: 이동
- `apply_affine_transform()`: 어파인 변환

