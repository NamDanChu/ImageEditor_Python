# FileListWidget 클래스

## 개요
파일 리스트를 표시하고 드래그 앤 드롭을 지원하는 위젯입니다.

## 위치
`Final_ImageProcessing/main.py`

## 클래스 정의
```python
class FileListWidget(QListWidget):
    """파일 리스트 위젯 (드래그 앤 드롭 지원)"""
```

## 주요 메서드

### `dragEnterEvent(self, event)`
드래그 진입 이벤트를 처리합니다.

### `dropEvent(self, event)`
드롭 이벤트를 처리하고 파일을 images 폴더로 복사합니다.

## 시그널

### `file_dropped(str)`
파일이 드롭되면 파일 경로를 전달합니다.

## 사용 예제
```python
file_list = FileListWidget(images_dir="images/")
file_list.file_dropped.connect(self.on_file_dropped)
```

