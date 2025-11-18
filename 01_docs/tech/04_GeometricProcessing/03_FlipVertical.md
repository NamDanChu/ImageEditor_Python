# apply_flip_vertical 함수

## 개요
이미지를 상하로 대칭 반전(수직 뒤집기)하는 함수입니다.

## 위치
`Final_ImageProcessing/image_processor/geometric_processing.py`

## 함수 정의
```python
def apply_flip_vertical(img):
    """상하 대칭 (수직 뒤집기)"""
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

## 반환값
- `numpy.ndarray`: 상하로 뒤집힌 이미지 배열
- 원본과 동일한 크기

## 동작 원리

OpenCV의 `cv2.flip()` 함수를 사용합니다:

```python
return cv2.flip(img, 0)
```

- `img`: 입력 이미지
- `0`: 수직 뒤집기 플래그

## 사용 예제

### 기본 사용
```python
from image_processor import geometric_processing
import cv2

image = cv2.imread("test.jpg")
flipped = geometric_processing.apply_flip_vertical(image)

cv2.imshow("Original", image)
cv2.imshow("Flipped Vertical", flipped)
cv2.waitKey(0)
```

### UI와 연동
```python
def on_flip_v_toggled(self, checked):
    self.button_states['flip_v'] = checked
    self.apply_all_effects()
```

## 관련 함수

- `apply_flip_horizontal()`: 좌우 대칭
- `apply_rotation()`: 회전

