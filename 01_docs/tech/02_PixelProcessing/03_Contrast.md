# apply_contrast 함수

## 개요
이미지의 명암(대비)을 조절하는 함수입니다. 픽셀 값에 곱셈 연산을 적용하여 대비를 조정합니다.

## 위치
`Final_ImageProcessing/image_processor/pixel_processing.py`

## 함수 정의
```python
def apply_contrast(img, value):
    """명암 조절
    value: 0 ~ 200 범위 (100이 원본)
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `value (int)`
- 명암 조절 값
- 범위: 0 ~ 200
- 100: 원본 명암
- 100보다 크면: 대비 증가 (밝은 부분은 더 밝게, 어두운 부분은 더 어둡게)
- 100보다 작으면: 대비 감소 (전체적으로 중간 톤으로)

## 반환값
- `numpy.ndarray`: 명암이 조절된 이미지 배열

## 동작 원리

1. **팩터 계산**: `value / 100.0`을 팩터로 사용합니다
   - `value = 100` → 팩터 = `1.0` (원본)
   - `value = 200` → 팩터 = `2.0` (대비 2배)
   - `value = 50` → 팩터 = `0.5` (대비 절반)

2. **픽셀 값 곱셈**: 각 픽셀 값에 팩터를 곱합니다
   ```python
   adjusted = img.astype(np.float32) * factor
   ```

3. **범위 제한**: 결과 값을 0 ~ 255 범위로 제한합니다
   ```python
   adjusted = np.clip(adjusted, 0, 255)
   ```

4. **타입 변환**: `uint8` 형식으로 변환하여 반환합니다

## 사용 예제

### 기본 사용
```python
from image_processor import pixel_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 명암 조절 (대비 증가)
high_contrast = pixel_processing.apply_contrast(image, 150)

# 명암 조절 (대비 감소)
low_contrast = pixel_processing.apply_contrast(image, 50)

# 원본 명암
original = pixel_processing.apply_contrast(image, 100)
```

### UI와 연동
```python
def on_contrast_changed(self, value):
    """슬라이더 값 변경 시 호출"""
    self.trackbar_values['contrast'] = value
    self.apply_all_effects()

def apply_all_effects(self):
    """모든 효과 적용"""
    if self.original_image is None:
        return
    
    result = self.original_image.copy()
    
    # 명암 조절
    contrast_value = self.trackbar_values['contrast']
    result = pixel_processing.apply_contrast(result, contrast_value)
    
    self.processed_image = result
    self.update_display()
```

### 밝기와 명암 함께 사용
```python
from image_processor import pixel_processing
import cv2

image = cv2.imread("test.jpg")

# 밝기 조절 후 명암 조절
result = pixel_processing.apply_brightness(image, 120)
result = pixel_processing.apply_contrast(result, 130)

cv2.imshow("Adjusted", result)
cv2.waitKey(0)
```

## 수학적 설명

명암 조절은 곱셈 변환을 사용합니다:

```
I_out(x, y) = clip(I_in(x, y) * factor, 0, 255)
```

여기서:
- `I_in(x, y)`: 입력 이미지의 픽셀 값
- `factor = value / 100.0`: 명암 조절 팩터
- `clip()`: 0 ~ 255 범위로 제한

### 밝기 vs 명암

- **밝기 (Brightness)**: 모든 픽셀에 동일한 값을 더하거나 빼는 방식
  - 전체적으로 밝거나 어두워짐
  - 대비는 유지됨

- **명암 (Contrast)**: 모든 픽셀에 동일한 값을 곱하는 방식
  - 밝은 부분은 더 밝아지고, 어두운 부분은 더 어두워짐
  - 대비가 증가하거나 감소함

## 주의사항

1. **값 범위**: `value`는 0 ~ 200 범위를 권장하지만, 이 범위를 벗어나도 동작합니다.

2. **부동소수점 연산**: `float32` 타입을 사용하여 정밀도를 유지합니다.

3. **오버플로우**: 곱셈 연산으로 인해 값이 255를 초과할 수 있으므로 `np.clip()`으로 제한합니다.

4. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원하며, 모든 채널에 동일한 팩터가 적용됩니다.

5. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

## 관련 함수

- `apply_brightness()`: 밝기 조절 (덧셈 방식)
- `apply_threshold()`: 이진화 (극단적인 대비)

