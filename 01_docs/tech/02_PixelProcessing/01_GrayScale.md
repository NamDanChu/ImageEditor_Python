# Grayscale 변환 함수

## 개요
컬러 이미지를 그레이스케일(흑백) 이미지로 변환하는 함수입니다. 두 개의 함수가 있으며, 동일한 기능을 수행합니다.

## 위치
`Final_ImageProcessing/image_processor/pixel_processing.py`

## 함수 정의

### `to_grayscale(image)`
```python
def to_grayscale(image):
    """
    컬러 이미지를 그레이스케일 이미지로 변환합니다.
    """
```

### `apply_grayscale(img)`
```python
def apply_grayscale(img):
    """그레이스케일 변환 (별칭)"""
    return to_grayscale(img)
```

## 매개변수

### `image` 또는 `img (numpy.ndarray)`
- 입력 이미지 배열
- 컬러(BGR) 또는 그레이스케일 형식 지원
- 이미 그레이스케일이면 그대로 반환

## 반환값
- `numpy.ndarray`: 그레이스케일 이미지 배열
- 원본이 이미 그레이스케일이면 원본 그대로 반환

## 동작 원리

1. **이미지 형식 확인**: 이미지의 차원을 확인합니다
   ```python
   if len(image.shape) == 3:
   ```
   - `len(shape) == 3`: 컬러 이미지 (B, G, R 채널)
   - `len(shape) == 2`: 그레이스케일 이미지

2. **그레이스케일 변환**: 컬러 이미지인 경우 OpenCV의 `cv2.cvtColor()`를 사용합니다
   ```python
   return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   ```

3. **그레이스케일 이미지**: 이미 그레이스케일이면 그대로 반환합니다
   ```python
   return image
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import pixel_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 그레이스케일 변환
gray = pixel_processing.to_grayscale(image)
# 또는
gray = pixel_processing.apply_grayscale(image)

cv2.imshow("Original", image)
cv2.imshow("Grayscale", gray)
cv2.waitKey(0)
```

### UI와 연동
```python
def on_grayscale_toggled(self, checked):
    """그레이스케일 버튼 토글 시 호출"""
    self.button_states['grayscale'] = checked
    self.apply_all_effects()

def apply_all_effects(self):
    """모든 효과 적용"""
    if self.original_image is None:
        return
    
    result = self.original_image.copy()
    
    # 그레이스케일 적용
    if self.button_states['grayscale']:
        result = pixel_processing.apply_grayscale(result)
    
    self.processed_image = result
    self.update_display()
```

### 이미 그레이스케일인 경우
```python
from image_processor import pixel_processing
import cv2

# 그레이스케일 이미지 로드
gray = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)

# 그레이스케일 변환 (이미 그레이스케일이므로 그대로 반환)
result = pixel_processing.to_grayscale(gray)
# result == gray (동일한 배열)
```

## 수학적 설명

그레이스케일 변환은 BGR 값을 가중 평균으로 계산합니다:

```
Gray = 0.299 * R + 0.587 * G + 0.114 * B
```

OpenCV의 `cv2.COLOR_BGR2GRAY`는 이 공식을 사용합니다:
- 빨강(R): 0.299 가중치
- 초록(G): 0.587 가중치 (가장 높음)
- 파랑(B): 0.114 가중치

이는 인간의 눈이 초록색에 가장 민감하다는 특성을 반영합니다.

## 활용 사례

1. **이미지 전처리**: 많은 이미지 처리 알고리즘은 그레이스케일 이미지를 요구합니다
2. **엣지 검출**: Canny 엣지 검출 등은 그레이스케일 이미지에서 수행됩니다
3. **메모리 절약**: 그레이스케일 이미지는 컬러 이미지보다 메모리를 적게 사용합니다
4. **시각적 효과**: 흑백 사진 효과를 만들 때 사용합니다

## 주의사항

1. **정보 손실**: 컬러에서 그레이스케일로 변환하면 색상 정보가 손실됩니다. 이는 비가역적입니다.

2. **이미 그레이스케일**: 이미 그레이스케일인 이미지에 적용해도 안전합니다. 함수가 자동으로 감지하여 그대로 반환합니다.

3. **BGR 형식**: OpenCV는 BGR 형식을 사용하므로, RGB 이미지를 직접 변환하면 색상이 다르게 보일 수 있습니다.

4. **성능**: `cv2.cvtColor()`는 매우 빠른 연산입니다.

## 관련 함수

- `apply_brightness()`: 밝기 조절
- `apply_contrast()`: 명암 조절
- `apply_threshold()`: 이진화 (그레이스케일 이미지 필요)
