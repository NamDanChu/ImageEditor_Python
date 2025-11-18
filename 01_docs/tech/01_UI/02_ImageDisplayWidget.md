# ImageDisplayWidget 클래스

## 개요
이미지를 표시하고 드래그하여 이동할 수 있는 위젯입니다.

## 위치
`Final_ImageProcessing/main.py`

## 클래스 정의
```python
class ImageDisplayWidget(QWidget):
    """이미지 표시 위젯 (드래그 가능)"""
```

## 주요 메서드

### `set_image(self, image)`
이미지를 설정하고 표시 영역을 업데이트합니다.

### `_calculate_scale(self)`
이미지 크기에 맞게 스케일을 계산합니다.

### `paintEvent(self, event)`
이미지를 화면에 그립니다.

## 사용 예제
```python
display = ImageDisplayWidget()
display.set_image(cv2.imread("test.jpg"))
```

