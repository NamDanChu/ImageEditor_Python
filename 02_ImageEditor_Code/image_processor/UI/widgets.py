"""
PyQt5 기반 UI 위젯 모듈
SOLID 원칙에 따라 UI 위젯을 모듈화
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import os


class FileListWidget(QListWidget):
    """파일 리스트 위젯 (드래그 앤 드롭 지원)"""
    
    file_dropped = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QListWidget {
                background-color: #323232;
                color: #dcdcdc;
                border: 1px solid #505050;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #404040;
            }
            QListWidget::item:selected {
                background-color: #6496c8;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #505050;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """드래그 진입 이벤트"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """드롭 이벤트"""
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
                    self.file_dropped.emit(file_path)
            event.acceptProposedAction()


class ImageDisplayWidget(QWidget):
    """이미지 표시 위젯 (드래그 가능)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = None
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.is_dragging = False
        self.drag_start_pos = None
        self.setMinimumSize(800, 500)
        self.setStyleSheet("background-color: #1e1e1e;")
    
    def set_image(self, image):
        """이미지 설정"""
        if image is not None:
            self.image = image.copy()
            self._calculate_scale()
            self.update()
    
    def _calculate_scale(self):
        """이미지 크기에 맞게 스케일 계산"""
        if self.image is None:
            return
        
        h, w = self.image.shape[:2]
        widget_w = self.width()
        widget_h = self.height()
        
        scale_w = widget_w / w
        scale_h = widget_h / h
        self.scale_factor = min(scale_w, scale_h, 1.0)
        
        # 중앙 정렬
        scaled_w = int(w * self.scale_factor)
        scaled_h = int(h * self.scale_factor)
        self.offset_x = (widget_w - scaled_w) // 2
        self.offset_y = (widget_h - scaled_h) // 2
    
    def mousePressEvent(self, event):
        """마우스 클릭 이벤트"""
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_start_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        """마우스 이동 이벤트"""
        if self.is_dragging and self.drag_start_pos:
            delta = event.pos() - self.drag_start_pos
            self.offset_x += delta.x()
            self.offset_y += delta.y()
            self.drag_start_pos = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        """마우스 릴리즈 이벤트"""
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.drag_start_pos = None
    
    def resizeEvent(self, event):
        """위젯 크기 변경 이벤트"""
        self._calculate_scale()
        self.update()
    
    def paintEvent(self, event):
        """그리기 이벤트"""
        from PyQt5.QtGui import QPainter, QImage
        from PyQt5.QtGui import QPixmap
        import cv2
        
        painter = QPainter(self)
        
        if self.image is None:
            return
        
        # OpenCV 이미지를 QImage로 변환
        if len(self.image.shape) == 2:
            q_image = QImage(self.image.data, self.image.shape[1], self.image.shape[0],
                           self.image.strides[0], QImage.Format_Grayscale8)
        else:
            rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            q_image = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0],
                           rgb_image.strides[0], QImage.Format_RGB888)
        
        # 이미지 크기 조정
        scaled_pixmap = QPixmap.fromImage(q_image).scaled(
            int(self.image.shape[1] * self.scale_factor),
            int(self.image.shape[0] * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        # 이미지 그리기
        painter.drawPixmap(self.offset_x, self.offset_y, scaled_pixmap)


class TopBarWidget(QWidget):
    """상단 메뉴바 위젯"""
    
    tab_clicked = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setStyleSheet("background-color: #323232; border-bottom: 2px solid #505050;")
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # 탭 버튼들
        self.tab_buttons = {}
        tabs = ['Pixel', 'Area', 'Geometric', 'Actions']
        for tab_name in tabs:
            btn = QPushButton(tab_name)
            btn.setFixedSize(80, 30)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, name=tab_name: self.on_tab_clicked(name))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #505050;
                    color: #dcdcdc;
                    border: 1px solid #606060;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #606060;
                }
                QPushButton:checked {
                    background-color: #0096ff;
                    color: white;
                }
            """)
            self.tab_buttons[tab_name] = btn
            layout.addWidget(btn)
        
        layout.addStretch()
    
    def on_tab_clicked(self, tab_name):
        """탭 클릭 이벤트"""
        # 모든 탭 버튼 해제
        for btn in self.tab_buttons.values():
            btn.setChecked(False)
        # 선택된 탭만 체크
        self.tab_buttons[tab_name].setChecked(True)
        self.tab_clicked.emit(tab_name)
    
    def set_active_tab(self, tab_name):
        """활성 탭 설정"""
        for name, btn in self.tab_buttons.items():
            btn.setChecked(name == tab_name)


class InfoBarWidget(QWidget):
    """정보 바 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: #2d2d2d; border-bottom: 1px solid #404040;")
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        self.info_label = QLabel('File: No Image | Size: 0 KB')
        self.info_label.setStyleSheet("color: #dcdcdc; font-size: 11px;")
        layout.addWidget(self.info_label)
    
    def set_info(self, text):
        """정보 텍스트 설정"""
        self.info_label.setText(text)

