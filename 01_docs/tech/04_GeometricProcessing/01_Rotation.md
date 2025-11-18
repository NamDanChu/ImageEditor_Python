# apply_rotation 함수

## 개요
이미지를 지정한 각도만큼 회전시키는 함수입니다. 중심을 기준으로 회전하며, 회전 후 이미지가 잘리지 않도록 크기를 자동 조정합니다.

## 위치
`Final_ImageProcessing/image_processor/geometric_processing.py`

## 함수 정의
```python
def apply_rotation(img, angle):
    """이미지 회전
    angle: 회전 각도 (0 ~ 360)
    """
```

## 매개변수

### `img (numpy.ndarray)`
- 입력 이미지 배열
- BGR 또는 그레이스케일 형식 지원

### `angle (int 또는 float)`
- 회전 각도
- 범위: 0 ~ 360 (또는 그 이상)
- 양수: 시계 방향 회전
- 음수: 반시계 방향 회전
- 0: 회전 없음 (원본 반환)

## 반환값
- `numpy.ndarray`: 회전된 이미지 배열
- 회전 후 크기가 변경될 수 있음

## 동작 원리

1. **각도 확인**: `angle`이 0이면 원본을 반환합니다
   ```python
   if angle == 0:
       return img
   ```

2. **이미지 크기 및 중심 계산**
   ```python
   h, w = img.shape[:2]
   center = (w // 2, h // 2)
   ```

3. **회전 행렬 생성**: OpenCV의 `cv2.getRotationMatrix2D()`를 사용합니다
   ```python
   rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
   ```
   - `center`: 회전 중심점
   - `angle`: 회전 각도
   - `1.0`: 스케일 팩터 (크기 변경 없음)

4. **회전 후 크기 계산**: 회전된 이미지가 잘리지 않도록 새로운 크기를 계산합니다
   ```python
   cos = np.abs(rotation_matrix[0, 0])
   sin = np.abs(rotation_matrix[0, 1])
   new_w = int((h * sin) + (w * cos))
   new_h = int((h * cos) + (w * sin))
   ```

5. **회전 행렬 조정**: 새로운 크기에 맞게 중심점을 이동합니다
   ```python
   rotation_matrix[0, 2] += (new_w / 2) - center[0]
   rotation_matrix[1, 2] += (new_h / 2) - center[1]
   ```

6. **이미지 회전**: `cv2.warpAffine()`을 사용하여 회전을 적용합니다
   ```python
   rotated = cv2.warpAffine(img, rotation_matrix, (new_w, new_h),
                           flags=cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT,
                           borderValue=(0, 0, 0))
   ```
   - `cv2.INTER_LINEAR`: 선형 보간
   - `cv2.BORDER_CONSTANT`: 빈 영역을 검은색(0, 0, 0)으로 채움

## 사용 예제

### 기본 사용
```python
from image_processor import geometric_processing
import cv2

# 이미지 로드
image = cv2.imread("test.jpg")

# 45도 회전
rotated_45 = geometric_processing.apply_rotation(image, 45)

# 90도 회전
rotated_90 = geometric_processing.apply_rotation(image, 90)

# 180도 회전
rotated_180 = geometric_processing.apply_rotation(image, 180)

cv2.imshow("Original", image)
cv2.imshow("45 degrees", rotated_45)
cv2.imshow("90 degrees", rotated_90)
cv2.imshow("180 degrees", rotated_180)
cv2.waitKey(0)
```

### 다양한 각도 테스트
```python
from image_processor import geometric_processing
import cv2

image = cv2.imread("test.jpg")

# 다양한 각도 테스트
angles = [0, 30, 45, 90, 135, 180, 270, 360]

for angle in angles:
    rotated = geometric_processing.apply_rotation(image, angle)
    cv2.imshow(f"Rotation {angle}°", rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

### UI와 연동
```python
def on_rotation_changed(self, value):
    """회전 슬라이더 값 변경 시 호출"""
    self.trackbar_values['rotation'] = value
    self.apply_all_effects()

def apply_all_effects(self):
    """모든 효과 적용"""
    if self.original_image is None:
        return
    
    result = self.original_image.copy()
    
    # 회전 적용
    angle = self.trackbar_values['rotation']
    result = geometric_processing.apply_rotation(result, angle)
    
    self.processed_image = result
    self.update_display()
```

## 수학적 설명

회전 변환은 다음과 같은 행렬을 사용합니다:

```
[cos(θ)  -sin(θ)  tx]
[sin(θ)   cos(θ)  ty]
[  0        0      1 ]
```

여기서:
- `θ`: 회전 각도 (라디안)
- `tx, ty`: 이동량 (회전 후 크기 조정을 위해)

### 회전 후 크기 계산

회전 후 이미지가 잘리지 않도록 새로운 크기를 계산합니다:

```
new_width = height * |sin(θ)| + width * |cos(θ)|
new_height = height * |cos(θ)| + width * |sin(θ)|
```

## 활용 사례

1. **이미지 정렬**: 스캔된 문서나 사진을 올바른 방향으로 회전
2. **데이터 증강**: 머신러닝 학습 데이터 증강
3. **예술적 효과**: 이미지를 회전시켜 다른 관점 제공
4. **전처리**: 일부 알고리즘은 특정 방향의 이미지를 요구

## 주의사항

1. **크기 변경**: 회전 후 이미지 크기가 변경될 수 있습니다. 원본보다 큰 영역이 생길 수 있습니다.

2. **빈 영역**: 회전 후 생기는 빈 영역은 검은색(0, 0, 0)으로 채워집니다.

3. **보간**: `cv2.INTER_LINEAR`를 사용하므로 약간의 품질 손실이 있을 수 있습니다.

4. **성능**: 큰 이미지나 복잡한 각도에서 처리 시간이 증가할 수 있습니다.

5. **각도 단위**: 각도는 도(degree) 단위입니다. 라디안이 아닙니다.

## 관련 함수

- `apply_flip_horizontal()`: 좌우 대칭
- `apply_flip_vertical()`: 상하 대칭

