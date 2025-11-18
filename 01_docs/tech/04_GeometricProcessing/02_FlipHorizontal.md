# apply_flip_horizontal 함수

## 개요
이미지를 좌우로 대칭 반전(수평 뒤집기)하는 함수입니다. 거울에 비친 것처럼 좌우가 바뀝니다.

## 위치
`Final_ImageProcessing/image_processor/geometric_processing.py`

## 함수 정의
```python
def apply_flip_horizontal(img):
    """좌우 대칭 (수평 뒤집기)"""
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

## 반환값
- `numpy.ndarray`: 좌우로 뒤집힌 이미지 배열
- 원본과 동일한 크기

## 동작 원리

OpenCV의 `cv2.flip()` 함수를 사용합니다:

```python
return cv2.flip(img, 1)
```

- `img`: 입력 이미지
- `1`: 수평 뒤집기 플래그
  - `0`: 수직 뒤집기 (상하)
  - `1`: 수평 뒤집기 (좌우)
  - `-1`: 수평 + 수직 뒤집기

## 사용 예제

### 기본 사용
```python
from image_processor import geometric_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 좌우 대칭
flipped = geometric_processing.apply_flip_horizontal(image)

cv2.imshow("Original", image)
cv2.imshow("Flipped Horizontal", flipped)
cv2.waitKey(0)
```

### UI와 연동
```python
def on_flip_h_toggled(self, checked):
    """좌우 대칭 버튼 토글 시 호출"""
    self.button_states['flip_h'] = checked
    self.apply_all_effects()

def apply_all_effects(self):
    """모든 효과 적용"""
    if self.original_image is None:
        return
    
    result = self.original_image.copy()
    
    # 좌우 대칭 적용
    if self.button_states['flip_h']:
        result = geometric_processing.apply_flip_horizontal(result)
    
    self.processed_image = result
    self.update_display()
```

### 수직 뒤집기와 함께 사용
```python
from image_processor import geometric_processing
import cv2

image = cv2.imread("test.jpg")

# 좌우 대칭
flipped_h = geometric_processing.apply_flip_horizontal(image)

# 상하 대칭
flipped_v = geometric_processing.apply_flip_vertical(image)

# 둘 다 적용 (180도 회전과 유사)
flipped_hv = geometric_processing.apply_flip_horizontal(image)
flipped_hv = geometric_processing.apply_flip_vertical(flipped_hv)

cv2.imshow("Original", image)
cv2.imshow("Horizontal", flipped_h)
cv2.imshow("Vertical", flipped_v)
cv2.imshow("Both", flipped_hv)
cv2.waitKey(0)
```

## 수학적 설명

수평 뒤집기는 다음과 같이 표현됩니다:

```
I_out(x, y) = I_in(width - 1 - x, y)
```

여기서:
- `I_in(x, y)`: 입력 이미지의 픽셀
- `I_out(x, y)`: 뒤집힌 이미지의 픽셀
- `width`: 이미지의 너비

### 예시

원본 이미지:
```
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
```

수평 뒤집기 후:
```
[3, 2, 1]
[6, 5, 4]
[9, 8, 7]
```

## 활용 사례

1. **데이터 증강**: 머신러닝 학습 데이터 증강
2. **이미지 정렬**: 스캔된 문서나 사진의 방향 조정
3. **예술적 효과**: 거울 효과나 대칭 이미지 생성
4. **전처리**: 일부 알고리즘은 특정 방향의 이미지를 요구

## 주의사항

1. **크기 유지**: 뒤집기 후 이미지 크기는 변경되지 않습니다.

2. **정보 보존**: 뒤집기는 정보 손실이 없는 연산입니다. 두 번 적용하면 원본으로 돌아갑니다.

3. **성능**: `cv2.flip()`은 매우 빠른 연산입니다.

4. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원하며, 모든 채널이 함께 뒤집힙니다.

5. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

## 관련 함수

- `apply_flip_vertical()`: 상하 대칭
- `apply_rotation()`: 회전 (180도 회전과 유사한 효과)

