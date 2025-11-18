# apply_morphology 함수

## 개요
모폴로지 연산(Morphological Operations)을 적용하는 함수입니다. 이미지의 형태를 변형하여 노이즈 제거, 객체 분리 등을 수행합니다.

## 위치
`Final_ImageProcessing/image_processor/area_processing.py`

## 함수 정의
```python
def apply_morphology(img, operation='open', kernel_size=5, iterations=1):
    """모폴로지 연산
    operation: 'erode', 'dilate', 'open', 'close', 'gradient', 'tophat', 'blackhat'
    kernel_size: 커널 크기 (홀수)
    iterations: 반복 횟수
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `operation (str)`
- 모폴로지 연산 종류
- `'erode'`: 침식 (Erosion)
- `'dilate'`: 팽창 (Dilation)
- `'open'`: 열림 (Opening) - 침식 후 팽창
- `'close'`: 닫힘 (Closing) - 팽창 후 침식
- `'gradient'`: 그라디언트 - 팽창과 침식의 차이
- `'tophat'`: 탑햇 - 원본과 열림의 차이
- `'blackhat'`: 블랙햇 - 닫힘과 원본의 차이

### `kernel_size (int)`
- 커널 크기
- 범위: 3 이상 (홀수 권장)
- 기본값: 5

### `iterations (int)`
- 반복 횟수
- 범위: 1 이상
- 기본값: 1

## 반환값
- `numpy.ndarray`: 모폴로지 연산이 적용된 이미지 배열

## 동작 원리

1. **커널 크기 검증 및 변환**: 커널 크기를 홀수로 변환합니다
   ```python
   if kernel_size < 3:
       kernel_size = 3
   if kernel_size % 2 == 0:
       kernel_size += 1
   ```

2. **구조 요소 생성**: 사각형 구조 요소를 생성합니다
   ```python
   kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
   ```

3. **연산 수행**: 선택된 연산을 수행합니다
   ```python
   if operation == 'erode':
       return cv2.erode(img, kernel, iterations=iterations)
   # ... 기타 연산들
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import area_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 침식
eroded = area_processing.apply_morphology(image, 'erode', 5, 1)

# 팽창
dilated = area_processing.apply_morphology(image, 'dilate', 5, 1)

# 열림
opened = area_processing.apply_morphology(image, 'open', 5, 1)

# 닫힘
closed = area_processing.apply_morphology(image, 'close', 5, 1)

cv2.imshow("Original", image)
cv2.imshow("Eroded", eroded)
cv2.imshow("Dilated", dilated)
cv2.imshow("Opened", opened)
cv2.imshow("Closed", closed)
cv2.waitKey(0)
```

### 다양한 연산 테스트
```python
from image_processor import area_processing
import cv2

image = cv2.imread("test.jpg")

operations = ['erode', 'dilate', 'open', 'close', 'gradient', 'tophat', 'blackhat']

for op in operations:
    result = area_processing.apply_morphology(image, op, 5, 1)
    cv2.imshow(f"Morphology {op}", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

## 모폴로지 연산 종류

### 1. 침식 (Erosion)
- 객체를 축소시킵니다
- 작은 노이즈 제거에 효과적
- 객체 경계를 축소

### 2. 팽창 (Dilation)
- 객체를 확장시킵니다
- 구멍 채우기에 효과적
- 객체 경계를 확장

### 3. 열림 (Opening)
- 침식 후 팽창
- 작은 노이즈 제거
- 객체 분리

### 4. 닫힘 (Closing)
- 팽창 후 침식
- 작은 구멍 채우기
- 객체 연결

### 5. 그라디언트 (Gradient)
- 팽창과 침식의 차이
- 객체 경계 검출

### 6. 탑햇 (Top Hat)
- 원본과 열림의 차이
- 밝은 작은 객체 검출

### 7. 블랙햇 (Black Hat)
- 닫힘과 원본의 차이
- 어두운 작은 객체 검출

## 활용 사례

1. **노이즈 제거**: 작은 노이즈 제거 (열림 연산)
2. **객체 분리**: 연결된 객체 분리 (열림 연산)
3. **구멍 채우기**: 객체 내부의 작은 구멍 채우기 (닫힘 연산)
4. **경계 검출**: 객체의 경계 검출 (그라디언트 연산)
5. **이진화 후처리**: 이진화된 이미지의 후처리

## 주의사항

1. **이진 이미지**: 모폴로지 연산은 주로 이진 이미지에 사용되지만, 그레이스케일 이미지에도 적용 가능합니다.

2. **커널 크기**: 커널 크기가 클수록 더 강한 효과가 나타납니다.

3. **반복 횟수**: 반복 횟수가 많을수록 효과가 누적됩니다.

4. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원하며, 각 채널에 독립적으로 연산이 적용됩니다.

5. **성능**: 반복 횟수와 커널 크기에 따라 처리 시간이 증가합니다.

## 관련 함수

- `apply_blur()`: 블러
- `apply_median_blur()`: 미디언 블러
- `pixel_processing.apply_threshold()`: 이진화 (모폴로지 전처리)

