# apply_resize 함수

## 개요
이미지의 크기를 조절하는 함수입니다. 너비, 높이, 또는 스케일 팩터를 사용하여 이미지 크기를 변경합니다.

## 위치
`Final_ImageProcessing/image_processor/geometric_processing.py`

## 함수 정의
```python
def apply_resize(img, width=None, height=None, scale=None, interpolation=cv2.INTER_LINEAR):
    """크기 조절
    width: 목표 너비 (픽셀)
    height: 목표 높이 (픽셀)
    scale: 스케일 팩터 (width, height가 None일 때 사용)
    interpolation: 보간 방법
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `width (int, optional)`
- 목표 너비 (픽셀)
- `None`이면 비율 유지

### `height (int, optional)`
- 목표 높이 (픽셀)
- `None`이면 비율 유지

### `scale (float, optional)`
- 스케일 팩터
- `width`와 `height`가 모두 `None`일 때 사용
- 1.0: 원본 크기
- 1.0보다 크면: 확대
- 1.0보다 작으면: 축소

### `interpolation`
- 보간 방법
- 기본값: `cv2.INTER_LINEAR`
- `cv2.INTER_NEAREST`: 최근접 이웃
- `cv2.INTER_LINEAR`: 선형 보간 (권장)
- `cv2.INTER_CUBIC`: 3차 보간
- `cv2.INTER_AREA`: 영역 보간 (축소 시 권장)
- `cv2.INTER_LANCZOS4`: Lanczos 보간

## 반환값
- `numpy.ndarray`: 크기가 조절된 이미지 배열

## 동작 원리

1. **크기 계산**: 지정된 매개변수에 따라 새로운 크기를 계산합니다
   - `width`와 `height` 모두 지정: 해당 크기로 조절
   - `width`만 지정: 비율 유지하며 너비 조절
   - `height`만 지정: 비율 유지하며 높이 조절
   - `scale` 지정: 스케일 팩터로 조절

2. **크기 조절**: OpenCV의 `cv2.resize()`를 사용합니다
   ```python
   return cv2.resize(img, new_size, interpolation=interpolation)
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import geometric_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 너비와 높이 지정
resized = geometric_processing.apply_resize(image, width=800, height=600)

# 비율 유지하며 너비만 지정
resized_width = geometric_processing.apply_resize(image, width=800)

# 비율 유지하며 높이만 지정
resized_height = geometric_processing.apply_resize(image, height=600)

# 스케일 팩터 사용
resized_scale = geometric_processing.apply_resize(image, scale=0.5)

cv2.imshow("Original", image)
cv2.imshow("Resized", resized)
cv2.waitKey(0)
```

### 다양한 보간 방법 테스트
```python
from image_processor import geometric_processing
import cv2

image = cv2.imread("test.jpg")

interpolations = [
    (cv2.INTER_NEAREST, "Nearest"),
    (cv2.INTER_LINEAR, "Linear"),
    (cv2.INTER_CUBIC, "Cubic"),
    (cv2.INTER_AREA, "Area"),
    (cv2.INTER_LANCZOS4, "Lanczos4")
]

for interp, name in interpolations:
    resized = geometric_processing.apply_resize(image, scale=2.0, interpolation=interp)
    cv2.imshow(f"Resize {name}", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

## 보간 방법 선택 가이드

### 확대 시
- **INTER_LINEAR**: 빠르고 품질 좋음 (권장)
- **INTER_CUBIC**: 더 나은 품질, 느림
- **INTER_LANCZOS4**: 최고 품질, 매우 느림

### 축소 시
- **INTER_AREA**: 가장 좋은 품질 (권장)
- **INTER_LINEAR**: 빠르고 품질 좋음

## 활용 사례

1. **이미지 리사이징**: 다양한 크기로 이미지 조절
2. **썸네일 생성**: 작은 크기의 썸네일 생성
3. **전처리**: 머신러닝 모델 입력 크기에 맞춤
4. **데이터 증강**: 다양한 크기의 이미지 생성

## 주의사항

1. **비율 유지**: `width` 또는 `height` 중 하나만 지정하면 비율이 유지됩니다.

2. **품질 손실**: 축소 후 다시 확대하면 품질이 손실됩니다.

3. **성능**: 보간 방법에 따라 처리 시간이 다릅니다.

4. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원합니다.

5. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

## 관련 함수

- `apply_rotation()`: 회전
- `apply_translate()`: 이동
- `apply_affine_transform()`: 어파인 변환

