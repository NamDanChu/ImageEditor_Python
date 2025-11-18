# apply_canny 함수

## 개요
캐니 엣지 검출(Canny Edge Detection) 알고리즘을 적용하는 함수입니다. 이미지에서 엣지(경계선)를 검출합니다.

## 위치
`Final_ImageProcessing/image_processor/area_processing.py`

## 함수 정의
```python
def apply_canny(img, low_threshold, high_threshold):
    """캐니 엣지 검출
    low_threshold: 낮은 임계값
    high_threshold: 높은 임계값
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `low_threshold (int)`
- 낮은 임계값
- 범위: 0 ~ 255
- 이 값보다 낮은 그래디언트는 엣지가 아닌 것으로 간주

### `high_threshold (int)`
- 높은 임계값
- 범위: 0 ~ 255
- 이 값보다 높은 그래디언트는 확실한 엣지로 간주
- 일반적으로 `low_threshold`의 2~3배 권장

## 반환값
- `numpy.ndarray`: 엣지 검출 결과 이미지 (이진 이미지)
- 원본이 컬러였으면 BGR 형식으로 반환
- 원본이 그레이스케일이었으면 그레이스케일 형식으로 반환

## 동작 원리

1. **그레이스케일 변환**: 컬러 이미지인 경우 먼저 그레이스케일로 변환합니다
   ```python
   if len(img.shape) == 3:
       gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   ```

2. **캐니 엣지 검출**: OpenCV의 `cv2.Canny()` 함수를 사용합니다
   ```python
   edges = cv2.Canny(gray, low_threshold, high_threshold)
   ```

3. **컬러 복원**: 원본이 컬러였으면 BGR 형식으로 변환하여 반환합니다
   ```python
   if len(img.shape) == 3:
       return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
   ```

## 캐니 알고리즘 단계

1. **가우시안 블러**: 노이즈 제거를 위해 가우시안 블러 적용
2. **그래디언트 계산**: Sobel 연산자를 사용하여 그래디언트 크기와 방향 계산
3. **비최대 억제**: 엣지가 아닌 픽셀 제거
4. **이중 임계값**: 낮은 임계값과 높은 임계값을 사용하여 엣지 결정
5. **히스테리시스**: 약한 엣지 중 강한 엣지와 연결된 것만 유지

## 사용 예제

### 기본 사용
```python
from image_processor import area_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 캐니 엣지 검출
edges = area_processing.apply_canny(image, 50, 150)

cv2.imshow("Original", image)
cv2.imshow("Edges", edges)
cv2.waitKey(0)
```

### 다양한 임계값 테스트
```python
from image_processor import area_processing
import cv2

image = cv2.imread("test.jpg")

# 다양한 임계값 조합 테스트
thresholds = [
    (30, 90),   # 낮은 임계값
    (50, 150),  # 중간 임계값
    (100, 200), # 높은 임계값
]

for low, high in thresholds:
    edges = area_processing.apply_canny(image, low, high)
    cv2.imshow(f"Canny ({low}, {high})", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

### 블러 후 엣지 검출
```python
from image_processor import area_processing
import cv2

image = cv2.imread("test.jpg")

# 블러 적용 후 엣지 검출 (노이즈 감소)
blurred = area_processing.apply_blur(image, 3)
edges = area_processing.apply_canny(blurred, 50, 150)

cv2.imshow("Original", image)
cv2.imshow("Blurred", blurred)
cv2.imshow("Edges", edges)
cv2.waitKey(0)
```

### UI와 연동
```python
def on_canny_low_changed(self, value):
    """낮은 임계값 슬라이더 변경 시 호출"""
    self.trackbar_values['canny_low'] = value
    self.apply_all_effects()

def on_canny_high_changed(self, value):
    """높은 임계값 슬라이더 변경 시 호출"""
    self.trackbar_values['canny_high'] = value
    self.apply_all_effects()

def apply_all_effects(self):
    """모든 효과 적용"""
    if self.original_image is None:
        return
    
    result = self.original_image.copy()
    
    # 캐니 엣지 검출 적용
    low = self.trackbar_values['canny_low']
    high = self.trackbar_values['canny_high']
    result = area_processing.apply_canny(result, low, high)
    
    self.processed_image = result
    self.update_display()
```

## 임계값 선택 가이드

### 낮은 임계값 (`low_threshold`)
- 너무 낮으면: 노이즈가 많이 검출됨
- 너무 높으면: 약한 엣지가 누락됨
- 권장: 30 ~ 50

### 높은 임계값 (`high_threshold`)
- 너무 낮으면: 약한 엣지도 검출됨
- 너무 높으면: 강한 엣지만 검출됨
- 권장: `low_threshold * 2 ~ 3`
- 예: `low = 50` → `high = 100 ~ 150`

## 활용 사례

1. **객체 검출**: 엣지를 이용한 객체 윤곽 검출
2. **이미지 분할**: 엣지를 기준으로 이미지 영역 분할
3. **특징 추출**: 컴퓨터 비전 알고리즘의 전처리 단계
4. **예술적 효과**: 스케치 효과나 스타일화된 이미지 생성

## 주의사항

1. **컬러 이미지**: 컬러 이미지는 자동으로 그레이스케일로 변환된 후 엣지 검출됩니다.

2. **임계값 선택**: 적절한 임계값 선택이 중요합니다. 이미지에 따라 최적의 값이 다를 수 있습니다.

3. **노이즈**: 노이즈가 많은 이미지는 먼저 블러를 적용하는 것이 좋습니다.

4. **이진 이미지**: 결과는 이진 이미지(0 또는 255)입니다.

5. **정보 손실**: 엣지 검출은 원본 이미지의 색상 정보를 모두 제거합니다.

## 관련 함수

- `apply_blur()`: 노이즈 제거를 위한 블러 적용
- `pixel_processing.apply_threshold()`: 단순 이진화 (캐니보다 단순하지만 덜 정확)

