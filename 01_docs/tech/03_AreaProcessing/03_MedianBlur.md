# apply_median_blur 함수

## 개요
미디언 블러(Median Blur)를 적용하는 함수입니다. 점처럼 찍힌 노이즈(소금-후추 노이즈) 제거에 효과적입니다.

## 위치
`Final_ImageProcessing/image_processor/area_processing.py`

## 함수 정의
```python
def apply_median_blur(img, kernel_size):
    """미디언 블러 적용
    kernel_size: 커널 크기 (홀수, 3 이상)
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `kernel_size (int)`
- 커널 크기
- 범위: 3 이상 (홀수 권장)
- 값이 클수록 더 강한 블러 효과

## 반환값
- `numpy.ndarray`: 미디언 블러가 적용된 이미지 배열

## 동작 원리

1. **커널 크기 검증**: `kernel_size`가 3보다 작으면 원본을 반환합니다
   ```python
   if kernel_size < 3:
       return img
   ```

2. **홀수 변환**: 커널 크기를 홀수로 변환합니다
   ```python
   if kernel_size % 2 == 0:
       kernel_size += 1
   ```

3. **미디언 블러 적용**: OpenCV의 `cv2.medianBlur()`를 사용합니다
   ```python
   return cv2.medianBlur(img, kernel_size)
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import area_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 미디언 블러 적용
blurred = area_processing.apply_median_blur(image, 5)

cv2.imshow("Original", image)
cv2.imshow("Median Blur", blurred)
cv2.waitKey(0)
```

### 다양한 커널 크기 테스트
```python
from image_processor import area_processing
import cv2

image = cv2.imread("test.jpg")

# 다양한 커널 크기 테스트
kernel_sizes = [3, 5, 7, 9, 11, 15]

for size in kernel_sizes:
    blurred = area_processing.apply_median_blur(image, size)
    cv2.imshow(f"Median Blur {size}", blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

## 가우시안 블러 vs 미디언 블러

### 가우시안 블러
- **용도**: 일반적인 노이즈 제거, 부드러운 효과
- **방법**: 가중 평균 사용
- **특징**: 모든 픽셀에 영향을 줌

### 미디언 블러
- **용도**: 소금-후추 노이즈 제거, 엣지 보존
- **방법**: 중간값(median) 사용
- **특징**: 엣지를 보존하면서 노이즈 제거

## 활용 사례

1. **노이즈 제거**: 소금-후추 노이즈가 있는 이미지 처리
2. **엣지 보존**: 엣지를 보존하면서 노이즈 제거가 필요한 경우
3. **전처리**: 일부 이미지 처리 알고리즘의 전처리 단계
4. **의료 이미지**: 의료 이미지의 노이즈 제거

## 주의사항

1. **커널 크기**: 커널 크기는 홀수여야 합니다. 함수가 자동으로 홀수로 변환합니다.

2. **성능**: 커널 크기가 클수록 처리 시간이 증가합니다. 특히 큰 이미지에서는 성능에 주의해야 합니다.

3. **엣지 보존**: 가우시안 블러보다 엣지를 더 잘 보존하지만, 완벽하지는 않습니다.

4. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원하며, 각 채널에 독립적으로 블러가 적용됩니다.

5. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

## 관련 함수

- `apply_blur()`: 가우시안 블러
- `apply_sharpen()`: 샤프닝
- `apply_morphology()`: 모폴로지 연산

