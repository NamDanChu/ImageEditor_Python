# apply_translate 함수

## 개요
이미지를 상하좌우로 이동시키는 함수입니다.

## 위치
`Final_ImageProcessing/image_processor/geometric_processing.py`

## 함수 정의
```python
def apply_translate(img, tx, ty):
    """이미지 이동
    tx: x축 이동량 (픽셀, 양수: 오른쪽, 음수: 왼쪽)
    ty: y축 이동량 (픽셀, 양수: 아래, 음수: 위)
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `tx (int 또는 float)`
- x축 이동량 (픽셀)
- 양수: 오른쪽으로 이동
- 음수: 왼쪽으로 이동
- 0: 이동 없음

### `ty (int 또는 float)`
- y축 이동량 (픽셀)
- 양수: 아래로 이동
- 음수: 위로 이동
- 0: 이동 없음

## 반환값
- `numpy.ndarray`: 이동된 이미지 배열
- 원본과 동일한 크기
- 빈 영역은 검은색(0, 0, 0)으로 채워짐

## 동작 원리

1. **이동량 확인**: `tx`와 `ty`가 모두 0이면 원본을 반환합니다
   ```python
   if tx == 0 and ty == 0:
       return img
   ```

2. **이동 행렬 생성**: 이동 행렬을 생성합니다
   ```python
   M = np.float32([[1, 0, tx],
                   [0, 1, ty]])
   ```

3. **이동 적용**: OpenCV의 `cv2.warpAffine()`을 사용합니다
   ```python
   translated = cv2.warpAffine(img, M, (w, h),
                               flags=cv2.INTER_LINEAR,
                               borderMode=cv2.BORDER_CONSTANT,
                               borderValue=(0, 0, 0))
   ```

## 사용 예제

### 기본 사용
```python
from image_processor import geometric_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 오른쪽으로 50픽셀, 아래로 30픽셀 이동
translated = geometric_processing.apply_translate(image, 50, 30)

# 왼쪽으로 50픽셀, 위로 30픽셀 이동
translated_left = geometric_processing.apply_translate(image, -50, -30)

cv2.imshow("Original", image)
cv2.imshow("Translated", translated)
cv2.waitKey(0)
```

### 다양한 이동 테스트
```python
from image_processor import geometric_processing
import cv2

image = cv2.imread("test.jpg")

# 다양한 이동 조합
translations = [
    (50, 0),    # 오른쪽
    (-50, 0),   # 왼쪽
    (0, 50),    # 아래
    (0, -50),   # 위
    (50, 50),   # 오른쪽 아래
    (-50, -50)  # 왼쪽 위
]

for tx, ty in translations:
    translated = geometric_processing.apply_translate(image, tx, ty)
    cv2.imshow(f"Translate ({tx}, {ty})", translated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

## 수학적 설명

이동 변환은 다음과 같은 행렬을 사용합니다:

```
[1  0  tx]
[0  1  ty]
[0  0   1]
```

변환 공식:
```
x' = x + tx
y' = y + ty
```

여기서:
- `(x, y)`: 원본 이미지의 픽셀 좌표
- `(x', y')`: 이동된 이미지의 픽셀 좌표
- `tx, ty`: 이동량

## 활용 사례

1. **이미지 정렬**: 이미지를 특정 위치로 이동
2. **데이터 증강**: 머신러닝 학습 데이터 증강
3. **패닝**: 큰 이미지의 특정 영역 표시
4. **전처리**: 일부 알고리즘의 전처리 단계

## 주의사항

1. **빈 영역**: 이동 후 생기는 빈 영역은 검은색(0, 0, 0)으로 채워집니다.

2. **이미지 크기**: 이동 후 이미지 크기는 변경되지 않습니다.

3. **범위 초과**: 이동량이 이미지 크기를 초과하면 이미지가 잘립니다.

4. **컬러 이미지**: BGR 형식의 컬러 이미지도 지원합니다.

5. **그레이스케일**: 그레이스케일 이미지도 동일하게 처리됩니다.

## 관련 함수

- `apply_rotation()`: 회전
- `apply_resize()`: 크기 조절
- `apply_affine_transform()`: 어파인 변환 (이동 포함)

