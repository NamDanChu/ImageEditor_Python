# apply_invert 함수

## 개요
이미지의 색상을 반전시키는 함수입니다. 각 픽셀 값을 255에서 빼서 반전 효과를 만듭니다.

## 위치
`Final_ImageProcessing/image_processor/pixel_processing.py`

## 함수 정의
```python
def apply_invert(img):
    """이미지 반전 (색상 반전)"""
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

## 반환값
- `numpy.ndarray`: 반전된 이미지 배열

## 동작 원리

1. **비트 반전**: OpenCV의 `cv2.bitwise_not()` 함수를 사용합니다
   ```python
   inverted = cv2.bitwise_not(img)
   ```

2. **수학적 표현**: 각 픽셀 값에 대해 `255 - value` 연산을 수행합니다
   - 0 → 255
   - 128 → 127
   - 255 → 0

## 사용 예제

### 기본 사용
```python
from image_processor import pixel_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 이미지 반전
inverted = pixel_processing.apply_invert(image)

cv2.imshow("Original", image)
cv2.imshow("Inverted", inverted)
cv2.waitKey(0)
```

### UI와 연동
```python
def on_invert_toggled(self, checked):
    """반전 버튼 토글 시 호출"""
    self.button_states['invert'] = checked
    self.apply_all_effects()

def apply_all_effects(self):
    """모든 효과 적용"""
    if self.original_image is None:
        return
    
    result = self.original_image.copy()
    
    # 반전 적용
    if self.button_states['invert']:
        result = pixel_processing.apply_invert(result)
    
    self.processed_image = result
    self.update_display()
```

### 그레이스케일 이미지 반전
```python
from image_processor import pixel_processing
import cv2

# 그레이스케일 이미지 로드
gray = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)

# 반전
inverted_gray = pixel_processing.apply_invert(gray)

cv2.imshow("Gray", gray)
cv2.imshow("Inverted Gray", inverted_gray)
cv2.waitKey(0)
```

## 수학적 설명

반전 연산은 다음과 같이 표현됩니다:

```
I_out(x, y) = 255 - I_in(x, y)
```

여기서:
- `I_in(x, y)`: 입력 이미지의 픽셀 값
- `I_out(x, y)`: 반전된 이미지의 픽셀 값

### 컬러 이미지의 경우

BGR 형식의 컬러 이미지에서는 각 채널이 독립적으로 반전됩니다:

```
B_out(x, y) = 255 - B_in(x, y)
G_out(x, y) = 255 - G_in(x, y)
R_out(x, y) = 255 - R_in(x, y)
```

## 활용 사례

1. **네거티브 효과**: 사진의 네거티브 필름 효과를 만들 때 사용
2. **시각적 강조**: 특정 영역을 강조하기 위해 반전 사용
3. **전처리**: 일부 이미지 처리 알고리즘의 전처리 단계에서 사용

## 주의사항

1. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원하며, 각 채널이 독립적으로 반전됩니다.

2. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

3. **비가역적**: 반전을 두 번 적용하면 원본으로 돌아갑니다 (토글 가능).

4. **성능**: `cv2.bitwise_not()`은 매우 빠른 연산입니다.

## 관련 함수

- `apply_grayscale()`: 그레이스케일 변환
- `apply_threshold()`: 이진화

