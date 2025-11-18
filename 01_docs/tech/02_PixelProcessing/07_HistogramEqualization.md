# apply_histogram_equalization 함수

## 개요
히스토그램 평활화(Histogram Equalization)를 적용하는 함수입니다. 명암 대비를 극대화하여 이미지를 선명하게 만듭니다.

## 위치
`Final_ImageProcessing/image_processor/pixel_processing.py`

## 함수 정의
```python
def apply_histogram_equalization(img):
    """히스토그램 평활화
    명암 대비를 극대화하여 이미지를 선명하게 만듭니다.
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

## 반환값
- `numpy.ndarray`: 히스토그램 평활화가 적용된 이미지 배열

## 동작 원리

### 그레이스케일 이미지
```python
return cv2.equalizeHist(img)
```

### 컬러 이미지
1. **YUV 변환**: BGR을 YUV 색공간으로 변환합니다
   ```python
   yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
   ```

2. **Y 채널 평활화**: 밝기 정보만 담고 있는 Y 채널에만 평활화를 적용합니다
   ```python
   yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
   ```

3. **BGR 복원**: YUV를 다시 BGR로 변환합니다
   ```python
   return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import pixel_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 히스토그램 평활화
equalized = pixel_processing.apply_histogram_equalization(image)

cv2.imshow("Original", image)
cv2.imshow("Equalized", equalized)
cv2.waitKey(0)
```

### 그레이스케일 이미지
```python
from image_processor import pixel_processing
import cv2

# 그레이스케일 이미지 로드
gray = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)

# 히스토그램 평활화
equalized = pixel_processing.apply_histogram_equalization(gray)

cv2.imshow("Original Gray", gray)
cv2.imshow("Equalized Gray", equalized)
cv2.waitKey(0)
```

## 수학적 설명

히스토그램 평활화는 다음 공식을 사용합니다:

```
I_out(x, y) = T(I_in(x, y))
```

여기서 `T`는 누적 분포 함수(CDF)를 기반으로 한 변환 함수입니다:

```
T(k) = round((L - 1) * CDF(k) / (M * N))
```

- `L`: 픽셀 값의 범위 (256)
- `CDF(k)`: 값 k까지의 누적 분포
- `M * N`: 이미지의 총 픽셀 수

### 효과

- **대비 향상**: 명암 대비가 극대화됩니다
- **히스토그램 분포**: 픽셀 값이 전체 범위에 고르게 분포됩니다
- **선명도 증가**: 이미지가 더 선명해 보입니다

## 활용 사례

1. **어두운 이미지 향상**: 어두운 이미지의 세부 정보를 드러냅니다
2. **의료 이미지**: X-ray나 CT 스캔 이미지의 대비 향상
3. **전처리**: 일부 이미지 처리 알고리즘의 전처리 단계
4. **시각화**: 데이터 시각화에서 대비 향상

## 주의사항

1. **컬러 이미지**: 컬러 이미지는 YUV 색공간으로 변환하여 밝기 채널만 평활화합니다. 색상 정보는 보존됩니다.

2. **과도한 적용**: 일부 이미지에서는 과도하게 적용되면 부자연스러울 수 있습니다.

3. **노이즈 증폭**: 노이즈가 있는 이미지에서는 노이즈가 더 두드러질 수 있습니다.

4. **비가역적**: 히스토그램 평활화는 비가역적 연산입니다.

5. **성능**: `cv2.equalizeHist()`는 매우 빠른 연산입니다.

## 관련 함수

- `apply_contrast()`: 명암 조절 (수동)
- `apply_gamma()`: 감마 보정
- `apply_brightness()`: 밝기 조절

