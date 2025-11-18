# apply_threshold 함수

## 개요
이미지를 이진화(binarization)하는 함수입니다. 임계값을 기준으로 픽셀을 흑백으로 분류합니다.

## 위치
`Final_ImageProcessing/image_processor/pixel_processing.py`

## 함수 정의
```python
def apply_threshold(img, value):
    """이진화 처리
    value: 임계값 (0 ~ 255)
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `value (int)`
- 임계값
- 범위: 0 ~ 255
- 이 값보다 작은 픽셀은 0 (검은색), 크거나 같은 픽셀은 255 (흰색)로 변환됩니다

## 반환값
- `numpy.ndarray`: 이진화된 이미지 배열
- 원본이 컬러였으면 BGR 형식으로 반환
- 원본이 그레이스케일이었으면 그레이스케일 형식으로 반환

## 동작 원리

1. **그레이스케일 변환**: 컬러 이미지인 경우 먼저 그레이스케일로 변환합니다
   ```python
   if len(img.shape) == 3:
       gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   ```

2. **이진화**: OpenCV의 `cv2.threshold()` 함수를 사용합니다
   ```python
   _, binary = cv2.threshold(gray, value, 255, cv2.THRESH_BINARY)
   ```
   - `value`: 임계값
   - `255`: 최대값 (임계값 이상인 픽셀의 값)
   - `cv2.THRESH_BINARY`: 이진화 모드

3. **컬러 복원**: 원본이 컬러였으면 BGR 형식으로 변환하여 반환합니다
   ```python
   if len(img.shape) == 3:
       return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import pixel_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 이진화 (임계값 127)
binary = pixel_processing.apply_threshold(image, 127)

cv2.imshow("Original", image)
cv2.imshow("Binary", binary)
cv2.waitKey(0)
```

### 다양한 임계값 테스트
```python
from image_processor import pixel_processing
import cv2

image = cv2.imread("test.jpg")

# 다양한 임계값 테스트
thresholds = [50, 100, 127, 150, 200]

for thresh in thresholds:
    binary = pixel_processing.apply_threshold(image, thresh)
    cv2.imshow(f"Threshold {thresh}", binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

### UI와 연동
```python
def on_threshold_changed(self, value):
    """슬라이더 값 변경 시 호출"""
    self.trackbar_values['threshold'] = value
    self.apply_all_effects()

def apply_all_effects(self):
    """모든 효과 적용"""
    if self.original_image is None:
        return
    
    result = self.original_image.copy()
    
    # 이진화 적용
    threshold_value = self.trackbar_values['threshold']
    result = pixel_processing.apply_threshold(result, threshold_value)
    
    self.processed_image = result
    self.update_display()
```

## 수학적 설명

이진화 연산은 다음과 같이 표현됩니다:

```
I_out(x, y) = {
    255,  if I_in(x, y) >= threshold
    0,    if I_in(x, y) < threshold
}
```

여기서:
- `I_in(x, y)`: 입력 이미지의 픽셀 값 (그레이스케일)
- `threshold`: 임계값
- `I_out(x, y)`: 이진화된 이미지의 픽셀 값

### 임계값 선택

- **낮은 임계값 (예: 50)**: 더 많은 픽셀이 흰색(255)이 됨
- **중간 임계값 (예: 127)**: 균형잡힌 이진화
- **높은 임계값 (예: 200)**: 더 많은 픽셀이 검은색(0)이 됨

## 활용 사례

1. **문서 스캔**: 문서 이미지에서 텍스트와 배경을 분리
2. **엣지 검출 전처리**: 이진화 후 엣지 검출 알고리즘 적용
3. **객체 분할**: 특정 밝기 범위의 객체를 분리
4. **OCR 전처리**: 텍스트 인식을 위한 전처리 단계

## 주의사항

1. **컬러 이미지**: 컬러 이미지는 자동으로 그레이스케일로 변환된 후 이진화됩니다.

2. **임계값 선택**: 적절한 임계값 선택이 중요합니다. 이미지에 따라 최적의 임계값이 다를 수 있습니다.

3. **자동 임계값**: 고정 임계값 대신 Otsu 방법 등 자동 임계값 선택 방법도 고려할 수 있습니다.

4. **정보 손실**: 이진화는 정보 손실이 큰 연산입니다. 원본 이미지의 세부 정보가 사라집니다.

## 관련 함수

- `apply_grayscale()`: 그레이스케일 변환
- `apply_invert()`: 이미지 반전
- `area_processing.apply_canny()`: 캐니 엣지 검출 (이진화와 유사한 결과)

