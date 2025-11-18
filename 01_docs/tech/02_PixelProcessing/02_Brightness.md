# apply_brightness 함수

## 개요
이미지의 밝기를 조절하는 함수입니다. 픽셀 단위로 밝기 값을 조정합니다.

## 위치
`Final_ImageProcessing/image_processor/pixel_processing.py`

## 함수 정의
```python
def apply_brightness(img, value):
    """밝기 조절
    value: -100 ~ 100 범위 (0이 원본)
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `value (int)`
- 밝기 조절 값
- 범위: -100 ~ 100
- 0: 원본 밝기
- 양수: 밝게
- 음수: 어둡게

## 반환값
- `numpy.ndarray`: 밝기가 조절된 이미지 배열

## 동작 원리

1. **값 변환**: `-100 ~ 100` 범위를 `0 ~ 200` 범위로 변환합니다
   - 실제 조절 값 = `value - 100`
   - 예: `value = 100` → 조절 값 = `0` (원본)
   - 예: `value = 150` → 조절 값 = `50` (밝게)
   - 예: `value = 50` → 조절 값 = `-50` (어둡게)

2. **픽셀 값 조정**: 각 픽셀 값에 조절 값을 더합니다
   ```python
   adjusted = img.astype(np.int16) + (value - 100)
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

# 밝기 조절 (밝게)
bright_image = pixel_processing.apply_brightness(image, 150)

# 밝기 조절 (어둡게)
dark_image = pixel_processing.apply_brightness(image, 50)

# 원본 밝기
original = pixel_processing.apply_brightness(image, 100)
```

### UI와 연동
```python
def on_brightness_changed(self, value):
    """슬라이더 값 변경 시 호출"""
    self.trackbar_values['brightness'] = value
    self.apply_all_effects()

def apply_all_effects(self):
    """모든 효과 적용"""
    if self.original_image is None:
        return
    
    result = self.original_image.copy()
    
    # 밝기 조절
    brightness_value = self.trackbar_values['brightness']
    result = pixel_processing.apply_brightness(result, brightness_value)
    
    self.processed_image = result
    self.update_display()
```

### 다양한 밝기 값 테스트
```python
from image_processor import pixel_processing
import cv2
import numpy as np

image = cv2.imread("test.jpg")

# 다양한 밝기 값 테스트
brightness_values = [0, 50, 100, 150, 200]

for value in brightness_values:
    adjusted = pixel_processing.apply_brightness(image, value)
    cv2.imshow(f"Brightness {value}", adjusted)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

## 수학적 설명

밝기 조절은 선형 변환을 사용합니다:

```
I_out(x, y) = clip(I_in(x, y) + offset, 0, 255)
```

여기서:
- `I_in(x, y)`: 입력 이미지의 픽셀 값
- `offset = value - 100`: 밝기 조절 오프셋
- `clip()`: 0 ~ 255 범위로 제한

## 주의사항

1. **값 범위**: `value`는 -100 ~ 100 범위를 권장하지만, 이 범위를 벗어나도 동작합니다.

2. **오버플로우/언더플로우**: `int16` 타입을 사용하여 오버플로우를 방지하고, `np.clip()`으로 최종 범위를 제한합니다.

3. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원하며, 모든 채널에 동일한 조절이 적용됩니다.

4. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

## 관련 함수

- `apply_contrast()`: 명암 조절 (밝기와 유사하지만 곱셈 방식)
- `apply_invert()`: 이미지 반전

