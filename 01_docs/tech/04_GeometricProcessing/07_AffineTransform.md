# apply_affine_transform 함수

## 개요
어파인 변환(Affine Transform)을 적용하는 함수입니다. 평행 관계를 유지하며 이미지를 변환합니다 (이동, 회전, 크기 조절 복합).

## 위치
`Final_ImageProcessing/image_processor/geometric_processing.py`

## 함수 정의
```python
def apply_affine_transform(img, src_points, dst_points):
    """어파인 변환
    src_points: 원본 이미지의 3개 점 좌표 (numpy array, shape: (3, 2))
    dst_points: 변환 후 이미지의 3개 점 좌표 (numpy array, shape: (3, 2))
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `src_points (numpy.ndarray)`
- 원본 이미지의 3개 점 좌표
- Shape: `(3, 2)`
- 각 행은 `[x, y]` 좌표

### `dst_points (numpy.ndarray)`
- 변환 후 이미지의 3개 점 좌표
- Shape: `(3, 2)`
- 각 행은 `[x, y]` 좌표

## 반환값
- `numpy.ndarray`: 어파인 변환이 적용된 이미지 배열
- 원본과 동일한 크기
- 빈 영역은 검은색(0, 0, 0)으로 채워짐

## 동작 원리

1. **입력 검증**: 점의 개수와 형태를 검증합니다
   ```python
   if src_points.shape != (3, 2) or dst_points.shape != (3, 2):
       raise ValueError("src_points and dst_points must be (3, 2) arrays")
   ```

2. **어파인 변환 행렬 계산**: OpenCV의 `cv2.getAffineTransform()`을 사용합니다
   ```python
   M = cv2.getAffineTransform(src_points.astype(np.float32),
                               dst_points.astype(np.float32))
   ```

3. **변환 적용**: OpenCV의 `cv2.warpAffine()`을 사용합니다
   ```python
   transformed = cv2.warpAffine(img, M, (w, h),
                                 flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_CONSTANT,
                                 borderValue=(0, 0, 0))
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import geometric_processing
import cv2
import numpy as np

# 이미지 로드
image = cv2.imread("test.jpg")
h, w = image.shape[:2]

# 원본 이미지의 3개 점 (왼쪽 상단, 오른쪽 상단, 왼쪽 하단)
src_points = np.array([
    [0, 0],           # 왼쪽 상단
    [w-1, 0],         # 오른쪽 상단
    [0, h-1]          # 왼쪽 하단
], dtype=np.float32)

# 변환 후 이미지의 3개 점 (이동 및 회전)
dst_points = np.array([
    [50, 50],         # 왼쪽 상단 이동
    [w-1+50, 50],     # 오른쪽 상단 이동
    [50, h-1+50]      # 왼쪽 하단 이동
], dtype=np.float32)

transformed = geometric_processing.apply_affine_transform(image, src_points, dst_points)

cv2.imshow("Original", image)
cv2.imshow("Transformed", transformed)
cv2.waitKey(0)
```

### 회전 및 크기 조절
```python
from image_processor import geometric_processing
import cv2
import numpy as np

image = cv2.imread("test.jpg")
h, w = image.shape[:2]

# 원본 이미지의 3개 점
src_points = np.array([
    [0, 0],
    [w-1, 0],
    [0, h-1]
], dtype=np.float32)

# 45도 회전 및 0.8배 축소
angle = np.radians(45)
scale = 0.8
center_x, center_y = w // 2, h // 2

# 변환 후 점 계산
cos_a = np.cos(angle) * scale
sin_a = np.sin(angle) * scale

dst_points = np.array([
    [center_x + (0 - center_x) * cos_a - (0 - center_y) * sin_a,
     center_y + (0 - center_x) * sin_a + (0 - center_y) * cos_a],
    [center_x + (w-1 - center_x) * cos_a - (0 - center_y) * sin_a,
     center_y + (w-1 - center_x) * sin_a + (0 - center_y) * cos_a],
    [center_x + (0 - center_x) * cos_a - (h-1 - center_y) * sin_a,
     center_y + (0 - center_x) * sin_a + (h-1 - center_y) * cos_a]
], dtype=np.float32)

transformed = geometric_processing.apply_affine_transform(image, src_points, dst_points)

cv2.imshow("Original", image)
cv2.imshow("Rotated & Scaled", transformed)
cv2.waitKey(0)
```

## 수학적 설명

어파인 변환은 다음과 같은 행렬을 사용합니다:

```
[x']   [a  b  tx] [x]
[y'] = [c  d  ty] [y]
[1 ]   [0  0  1 ] [1]
```

여기서:
- `(x, y)`: 원본 이미지의 픽셀 좌표
- `(x', y')`: 변환된 이미지의 픽셀 좌표
- `a, b, c, d`: 회전 및 크기 조절 매개변수
- `tx, ty`: 이동 매개변수

### 어파인 변환의 특성

- **평행선 보존**: 평행선은 변환 후에도 평행합니다
- **비율 보존**: 직선의 비율이 유지됩니다
- **3점으로 결정**: 3개의 점만 지정하면 변환이 결정됩니다

## 활용 사례

1. **이미지 정렬**: 스캔된 문서나 사진을 정렬
2. **기하학적 보정**: 왜곡된 이미지 보정
3. **데이터 증강**: 머신러닝 학습 데이터 증강
4. **복합 변환**: 이동, 회전, 크기 조절을 한 번에 적용

## 주의사항

1. **점의 개수**: 정확히 3개의 점이 필요합니다.

2. **점의 위치**: 3개의 점이 한 직선 위에 있으면 안 됩니다.

3. **좌표 순서**: `src_points`와 `dst_points`의 점 순서가 일치해야 합니다.

4. **빈 영역**: 변환 후 생기는 빈 영역은 검은색(0, 0, 0)으로 채워집니다.

5. **이미지 크기**: 변환 후 이미지 크기는 변경되지 않습니다.

## 관련 함수

- `apply_rotation()`: 회전
- `apply_translate()`: 이동
- `apply_resize()`: 크기 조절

