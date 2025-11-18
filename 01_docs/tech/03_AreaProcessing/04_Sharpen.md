# apply_sharpen 함수

## 개요
샤프닝(Sharpening)을 적용하는 함수입니다. 이미지의 경계를 강조하여 선명하게 만듭니다.

## 위치
`Final_ImageProcessing/image_processor/area_processing.py`

## 함수 정의
```python
def apply_sharpen(img, strength=1.0):
    """샤프닝 적용
    strength: 샤프닝 강도 (0.0 ~ 3.0)
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `strength (float)`
- 샤프닝 강도
- 범위: 0.0 ~ 3.0 (권장)
- 0.0: 샤프닝 없음 (원본 반환)
- 값이 클수록 더 강한 샤프닝 효과

## 반환값
- `numpy.ndarray`: 샤프닝이 적용된 이미지 배열

## 동작 원리

1. **강도 확인**: `strength`가 0 이하이면 원본을 반환합니다
   ```python
   if strength <= 0:
       return img
   ```

2. **샤프닝 커널 생성**: 샤프닝 커널을 생성합니다
   ```python
   kernel = np.array([[-1, -1, -1],
                      [-1,  9, -1],
                      [-1, -1, -1]]) * strength
   ```

3. **커널 정규화**: 커널을 정규화합니다
   ```python
   kernel[1, 1] = 8 * strength + 1
   ```

4. **필터 적용**: OpenCV의 `cv2.filter2D()`를 사용합니다
   ```python
   sharpened = cv2.filter2D(img, -1, kernel)
   ```

5. **범위 제한**: 결과 값을 0 ~ 255 범위로 제한합니다
   ```python
   return np.clip(sharpened, 0, 255).astype(np.uint8)
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import area_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 샤프닝 적용
sharpened = area_processing.apply_sharpen(image, 1.0)

cv2.imshow("Original", image)
cv2.imshow("Sharpened", sharpened)
cv2.waitKey(0)
```

### 다양한 강도 테스트
```python
from image_processor import area_processing
import cv2

image = cv2.imread("test.jpg")

# 다양한 강도 테스트
strengths = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

for strength in strengths:
    sharpened = area_processing.apply_sharpen(image, strength)
    cv2.imshow(f"Sharpen {strength}", sharpened)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

## 수학적 설명

샤프닝은 라플라시안 필터를 사용합니다:

```
I_out(x, y) = I_in(x, y) + α * Laplacian(I_in(x, y))
```

여기서:
- `I_in(x, y)`: 입력 이미지의 픽셀 값
- `α`: 샤프닝 강도 (`strength`)
- `Laplacian()`: 라플라시안 연산자

### 샤프닝 커널

```
[-1, -1, -1]
[-1,  9, -1]  * strength
[-1, -1, -1]
```

이 커널은 중심 픽셀을 강조하고 주변 픽셀을 약화시켜 엣지를 강조합니다.

## 활용 사례

1. **이미지 선명화**: 흐릿한 이미지를 선명하게 만듭니다
2. **엣지 강조**: 객체의 경계를 더 명확하게 만듭니다
3. **후처리**: 블러나 다른 필터 적용 후 선명도 복원
4. **인쇄 준비**: 인쇄용 이미지의 선명도 향상

## 주의사항

1. **과도한 적용**: 과도하게 적용하면 노이즈가 증폭되거나 부자연스러울 수 있습니다.

2. **노이즈 증폭**: 노이즈가 있는 이미지에서는 노이즈가 더 두드러질 수 있습니다.

3. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원하며, 각 채널에 독립적으로 샤프닝이 적용됩니다.

4. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

5. **성능**: `cv2.filter2D()`는 빠른 연산이지만, 큰 이미지에서는 시간이 걸릴 수 있습니다.

## 관련 함수

- `apply_blur()`: 블러 (반대 효과)
- `apply_median_blur()`: 미디언 블러
- `apply_canny()`: 엣지 검출

