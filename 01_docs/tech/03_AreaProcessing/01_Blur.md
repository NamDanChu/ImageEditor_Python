# apply_blur 함수

## 개요
이미지에 가우시안 블러(Gaussian Blur) 효과를 적용하는 함수입니다. 주변 픽셀을 고려하여 부드러운 블러 효과를 만듭니다.

## 위치
`Final_ImageProcessing/image_processor/area_processing.py`

## 함수 정의
```python
def apply_blur(img, value):
    """가우시안 블러 적용
    value: 블러 강도 (0 ~ 20, 홀수만 유효)
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `value (int)`
- 블러 강도
- 범위: 0 ~ 20
- 0: 블러 없음 (원본 반환)
- 값이 클수록 더 강한 블러 효과

## 반환값
- `numpy.ndarray`: 블러가 적용된 이미지 배열

## 동작 원리

1. **값 확인**: `value`가 0 이하이면 원본을 반환합니다
   ```python
   if value <= 0:
       return img
   ```

2. **커널 크기 계산**: `value`를 홀수 커널 크기로 변환합니다
   ```python
   kernel_size = value * 2 + 1
   ```
   - `value = 1` → `kernel_size = 3`
   - `value = 5` → `kernel_size = 11`
   - `value = 10` → `kernel_size = 21`

3. **가우시안 블러 적용**: OpenCV의 `cv2.GaussianBlur()`를 사용합니다
   ```python
   return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
   ```
   - `(kernel_size, kernel_size)`: 커널 크기 (정사각형)
   - `0`: 표준 편차 (0이면 자동 계산)

## 사용 예제

### 기본 사용
```python
from image_processor import area_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 블러 적용 (약한 블러)
blurred_light = area_processing.apply_blur(image, 3)

# 블러 적용 (강한 블러)
blurred_heavy = area_processing.apply_blur(image, 10)

cv2.imshow("Original", image)
cv2.imshow("Light Blur", blurred_light)
cv2.imshow("Heavy Blur", blurred_heavy)
cv2.waitKey(0)
```

### 다양한 블러 강도 테스트
```python
from image_processor import area_processing
import cv2

image = cv2.imread("test.jpg")

# 다양한 블러 강도 테스트
blur_values = [0, 2, 5, 10, 15, 20]

for value in blur_values:
    blurred = area_processing.apply_blur(image, value)
    cv2.imshow(f"Blur {value}", blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

### UI와 연동
```python
def on_blur_changed(self, value):
    """슬라이더 값 변경 시 호출"""
    self.trackbar_values['blur'] = value
    self.apply_all_effects()

def apply_all_effects(self):
    """모든 효과 적용"""
    if self.original_image is None:
        return
    
    result = self.original_image.copy()
    
    # 블러 적용
    blur_value = self.trackbar_values['blur']
    result = area_processing.apply_blur(result, blur_value)
    
    self.processed_image = result
    self.update_display()
```

## 수학적 설명

가우시안 블러는 가우시안 함수를 사용한 컨볼루션 연산입니다:

```
G(x, y) = (1 / (2πσ²)) * exp(-(x² + y²) / (2σ²))
```

여기서:
- `σ (sigma)`: 표준 편차 (블러 강도)
- `(x, y)`: 커널 내 픽셀 위치

각 픽셀은 주변 픽셀들의 가중 평균으로 대체됩니다. 중심에 가까운 픽셀일수록 더 높은 가중치를 가집니다.

## 활용 사례

1. **노이즈 제거**: 이미지의 노이즈를 줄이는 데 사용
2. **부드러운 효과**: 이미지를 부드럽게 만들어 자연스러운 느낌
3. **전처리**: 일부 이미지 처리 알고리즘의 전처리 단계
4. **초점 효과**: 특정 영역만 선명하게 하고 나머지는 블러 처리

## 주의사항

1. **커널 크기**: 커널 크기는 항상 홀수여야 합니다. 함수가 자동으로 홀수로 변환합니다.

2. **성능**: 커널 크기가 클수록 처리 시간이 증가합니다.

3. **정보 손실**: 블러는 정보 손실이 있는 연산입니다. 과도한 블러는 이미지의 세부 정보를 손실시킵니다.

4. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원하며, 각 채널에 독립적으로 블러가 적용됩니다.

5. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

## 관련 함수

- `apply_canny()`: 엣지 검출 (블러 후 적용하면 더 나은 결과)
- `pixel_processing.apply_threshold()`: 이진화

