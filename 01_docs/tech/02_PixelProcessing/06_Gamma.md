# apply_gamma 함수

## 개요
감마 보정(Gamma Correction)을 적용하는 함수입니다. 이미지의 중간 밝기 영역을 조절하여 전체적인 밝기를 자연스럽게 변경합니다.

## 위치
`Final_ImageProcessing/image_processor/pixel_processing.py`

## 함수 정의
```python
def apply_gamma(img, gamma):
    """감마 보정
    gamma: 감마 값 (0.1 ~ 3.0, 1.0이 원본)
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `gamma (float)`
- 감마 값
- 범위: 0.1 ~ 3.0 (권장)
- 1.0: 원본 (변화 없음)
- 1.0보다 작으면: 밝게 (감마 감소)
- 1.0보다 크면: 어둡게 (감마 증가)

## 반환값
- `numpy.ndarray`: 감마 보정이 적용된 이미지 배열

## 동작 원리

1. **감마 값 확인**: `gamma`가 1.0이면 원본을 반환합니다
   ```python
   if gamma == 1.0:
       return img
   ```

2. **LUT 생성**: 감마 보정을 위한 Look-Up Table을 생성합니다
   ```python
   inv_gamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** inv_gamma) * 255
                     for i in np.arange(0, 256)]).astype("uint8")
   ```

3. **LUT 적용**: OpenCV의 `cv2.LUT()`를 사용하여 변환을 적용합니다
   ```python
   return cv2.LUT(img, table)
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import pixel_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 감마 보정 (밝게)
bright = pixel_processing.apply_gamma(image, 0.5)

# 감마 보정 (어둡게)
dark = pixel_processing.apply_gamma(image, 2.0)

# 원본
original = pixel_processing.apply_gamma(image, 1.0)

cv2.imshow("Original", image)
cv2.imshow("Bright (gamma=0.5)", bright)
cv2.imshow("Dark (gamma=2.0)", dark)
cv2.waitKey(0)
```

### 다양한 감마 값 테스트
```python
from image_processor import pixel_processing
import cv2

image = cv2.imread("test.jpg")

# 다양한 감마 값 테스트
gamma_values = [0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 2.5]

for gamma in gamma_values:
    adjusted = pixel_processing.apply_gamma(image, gamma)
    cv2.imshow(f"Gamma {gamma}", adjusted)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

## 수학적 설명

감마 보정은 다음 공식을 사용합니다:

```
I_out(x, y) = 255 * (I_in(x, y) / 255) ^ (1 / gamma)
```

여기서:
- `I_in(x, y)`: 입력 이미지의 픽셀 값
- `gamma`: 감마 값
- `I_out(x, y)`: 보정된 이미지의 픽셀 값

### 감마 곡선

- **gamma < 1.0**: 밝은 영역을 더 밝게, 어두운 영역의 변화는 적음 (밝기 증가)
- **gamma = 1.0**: 선형 변환 (변화 없음)
- **gamma > 1.0**: 어두운 영역을 더 어둡게, 밝은 영역의 변화는 적음 (밝기 감소)

## 활용 사례

1. **디스플레이 보정**: 모니터나 프린터의 감마 특성 보정
2. **이미지 향상**: 어두운 이미지를 밝게 하거나 과도하게 밝은 이미지를 어둡게
3. **예술적 효과**: 특정 분위기를 연출하기 위한 밝기 조절
4. **전처리**: 일부 이미지 처리 알고리즘의 전처리 단계

## 주의사항

1. **값 범위**: `gamma`는 0보다 큰 값이어야 합니다. 0에 가까우면 매우 밝아지고, 매우 크면 매우 어두워집니다.

2. **LUT 사용**: LUT(Look-Up Table)를 사용하여 성능을 최적화합니다.

3. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원하며, 모든 채널에 동일한 감마 값이 적용됩니다.

4. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

5. **비가역적**: 감마 보정은 비가역적 연산입니다. 원본으로 완전히 복원할 수 없습니다.

## 관련 함수

- `apply_brightness()`: 밝기 조절 (선형 변환)
- `apply_contrast()`: 명암 조절
- `apply_histogram_equalization()`: 히스토그램 평활화

