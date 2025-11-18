# main.py

import sys
import os
import glob
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QLabel, QListWidget, QListWidgetItem,
    QMenuBar, QMenu, QStatusBar, QFileDialog, QMessageBox,
    QScrollArea, QGroupBox, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QMimeData
from PyQt5.QtGui import QImage, QPixmap, QFont, QDragEnterEvent, QDropEvent
import cv2
import numpy as np
from image_processor import pixel_processing, area_processing, geometric_processing, file_operations
from image_processor.UI.settings_panel import SettingsPanel


class ImageDisplayWidget(QWidget):
    """이미지 표시 위젯 (드래그 가능)"""
    
    def __init__(self):
        super().__init__()
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
        self.scale_factor = min(scale_w, scale_h, 1.0)  # 최대 1.0 (원본 크기 이상 확대 안 함)
        
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
        from PyQt5.QtGui import QPainter
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


class FileListWidget(QListWidget):
    """파일 리스트 위젯 (드래그 앤 드롭 지원)"""
    
    file_dropped = pyqtSignal(str)
    
    def __init__(self, images_dir=None):
        super().__init__()
        self.images_dir = images_dir
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DropOnly)  # 드롭만 허용
        print(f"FileListWidget 초기화됨, images_dir: {images_dir}")
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
        print("dragEnterEvent 호출됨")
        if event.mimeData().hasUrls():
            print(f"URLs 발견: {len(event.mimeData().urls())}개")
            event.acceptProposedAction()
            event.accept()
        else:
            print("URLs 없음")
            event.ignore()
    
    def dragMoveEvent(self, event):
        """드래그 이동 이벤트"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event: QDropEvent):
        """드롭 이벤트 - 파일을 images 폴더로 복사"""
        print("dropEvent 호출됨")
        if event.mimeData().hasUrls():
            print(f"드롭된 URLs: {len(event.mimeData().urls())}개")
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            print(f"드롭된 파일 경로: {file_path}")
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                print(f"파일 확장자: {ext}")
                if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
                    # images 폴더 경로 사용
                    if self.images_dir is None:
                        # images_dir이 설정되지 않았으면 기본 경로 사용
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        images_dir = os.path.join(current_dir, 'images')
                    else:
                        images_dir = self.images_dir
                    
                    if not os.path.exists(images_dir):
                        os.makedirs(images_dir)
                    
                    # 파일명 추출 및 복사
                    file_name = os.path.basename(file_path)
                    dest_path = os.path.join(images_dir, file_name)
                    
                    # 동일한 파일명이 있으면 번호 추가
                    counter = 1
                    base_name, ext_name = os.path.splitext(file_name)
                    while os.path.exists(dest_path):
                        new_name = f"{base_name}_{counter}{ext_name}"
                        dest_path = os.path.join(images_dir, new_name)
                        counter += 1
                    
                    # 파일 복사
                    import shutil
                    try:
                        shutil.copy2(file_path, dest_path)
                        print(f"파일 복사 완료: {file_path} -> {dest_path}")
                        self.file_dropped.emit(dest_path)
                        event.acceptProposedAction()
                    except Exception as e:
                        from PyQt5.QtWidgets import QMessageBox
                        error_msg = f"파일 복사에 실패했습니다.\n원본: {file_path}\n대상: {dest_path}\n오류: {str(e)}"
                        print(error_msg)
                        QMessageBox.warning(None, "복사 실패", error_msg)
                        event.ignore()
                else:
                    print(f"지원하지 않는 확장자: {ext}")
                    event.ignore()
            else:
                print(f"파일이 존재하지 않음: {file_path}")
                event.ignore()
        else:
            print("드롭 이벤트에 URLs가 없음")
            event.ignore()


class ImageEditor(QMainWindow):
    """이미지 편집기 메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.processed_image = None
        self.image_files = []
        self.current_file_path = None
        
        # images 폴더 경로 설정
        # EXE 파일로 실행되는 경우와 일반 실행을 구분
        if getattr(sys, 'frozen', False):
            # PyInstaller로 빌드된 EXE 실행 시
            # EXE 파일이 있는 디렉토리를 기준으로 images 폴더 생성
            # sys.executable은 EXE 파일의 경로를 가리킴
            current_dir = os.path.dirname(os.path.abspath(sys.executable))
        else:
            # 일반 Python 스크립트 실행 시
            current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.images_dir = os.path.join(current_dir, 'images')
        # images 폴더가 없으면 생성 (빈 폴더로 시작)
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
            print(f"images 폴더 생성됨: {self.images_dir}")
        
        # 상태
        self.button_states = {
            'grayscale': False,
            'invert': False,
            'flip_h': False,
            'flip_v': False
        }
        self.trackbar_values = {
            'brightness': 100,  # 중간값으로 변경
            'contrast': 100,
            'threshold': 127,
            'blur': 0,
            'canny_low': 50,
            'canny_high': 150,
            'sharpen': 0,
            'rotation': 0,
            'resize_w': 100,
            'resize_h': 100
        }
        
        # File 관리자 초기화
        self.file_manager = file_operations.FileManager()
        self.history_manager = file_operations.HistoryManager(self.file_manager)
        self.file_saver = file_operations.FileSaver()
        self.file_loader = file_operations.FileLoader()
        self.settings_manager = file_operations.SettingsManager()
        
        self.current_tab = 'Pixel'
        self.init_ui()
        self.scan_image_files()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('Image Editor')
        self.setGeometry(100, 100, 1600, 900)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 왼쪽 패널 (파일 리스트)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel)
        
        # 오른쪽 영역
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # 상단 메뉴바
        top_bar = self.create_top_bar()
        right_layout.addWidget(top_bar)
        
        # 정보 바
        info_bar = self.create_info_bar()
        right_layout.addWidget(info_bar)
        
        # 중앙 이미지 표시 영역
        self.image_display = ImageDisplayWidget()
        right_layout.addWidget(self.image_display, 1)
        
        # 하단 설정 패널
        settings_panel = self.create_settings_panel()
        right_layout.addWidget(settings_panel)
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget, 1)
        
        # 상태바
        self.statusBar().showMessage('Ready')
    
    def create_left_panel(self):
        """왼쪽 파일 리스트 패널 생성"""
        panel = QWidget()
        panel.setFixedWidth(250)
        panel.setStyleSheet("background-color: #323232;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 제목
        title = QLabel('Image Files')
        title.setStyleSheet("color: #dcdcdc; font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(title)
        
        # 파일 리스트
        self.file_list = FileListWidget(images_dir=self.images_dir)
        self.file_list.itemClicked.connect(self.on_file_selected)
        self.file_list.file_dropped.connect(self.on_file_dropped)
        layout.addWidget(self.file_list)
        
        return panel
    
    def create_top_bar(self):
        """상단 메뉴바 생성"""
        bar = QWidget()
        bar.setFixedHeight(40)
        bar.setStyleSheet("background-color: #323232; border-bottom: 2px solid #505050;")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # 메뉴바 (드롭다운 메뉴 포함)
        self.menu_bar = QMenuBar(bar)
        self.menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #323232;
                color: #dcdcdc;
                border: none;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #0096ff;
            }
            QMenu {
                background-color: #373737;
                color: #dcdcdc;
                border: 1px solid #505050;
            }
            QMenu::item:selected {
                background-color: #0096ff;
            }
        """)
        
        # 메뉴 항목 정의 (File을 맨 앞으로)
        menu_items = {
            'File': ['Save', 'Save As', 'Load', 'Undo', 'Redo', 'Settings', 'Exit'],
            'Pixel': ['Brightness', 'Contrast', 'Threshold', 'Grayscale', 'Invert'],
            'Area': ['Blur', 'Canny Edge', 'Sharpen', 'Median Blur'],
            'Geometric': ['Rotation', 'Flip H', 'Flip V', 'Resize', 'Translate']
        }
        
        self.tab_menus = {}
        for tab_name, items in menu_items.items():
            menu = self.menu_bar.addMenu(tab_name)
            for item in items:
                action = menu.addAction(item)
                # File 카테고리는 메뉴 항목 클릭 시 바로 실행
                if tab_name == 'File':
                    action.triggered.connect(lambda checked, i=item: self.on_file_menu_action(i))
                else:
                    action.triggered.connect(lambda checked, t=tab_name: self.on_tab_clicked(t))
            self.tab_menus[tab_name] = menu
        
        layout.addWidget(self.menu_bar)
        layout.addStretch()
        
        # 탭 버튼들 (메뉴와 함께 사용) - File을 맨 앞으로
        self.tab_buttons = {}
        tabs = ['File', 'Pixel', 'Area', 'Geometric']
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
        
        return bar
    
    def create_info_bar(self):
        """정보 바 생성"""
        bar = QWidget()
        bar.setFixedHeight(30)
        bar.setStyleSheet("background-color: #2d2d2d; border-bottom: 1px solid #404040;")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(10, 0, 10, 0)
        
        self.info_label = QLabel('File: No Image | Size: 0 KB')
        self.info_label.setStyleSheet("color: #dcdcdc; font-size: 11px;")
        layout.addWidget(self.info_label)
        
        return bar
    
    def create_settings_panel(self):
        """하단 설정 패널 생성"""
        panel = SettingsPanel()
        
        # RESET 버튼 연결
        panel.get_reset_button().clicked.connect(self.on_reset_clicked)
        
        # Pixel 설정 위젯 연결
        pixel_settings = panel.get_pixel_settings()
        pixel_settings.get_grayscale_button().clicked.connect(
            lambda: self.on_button_toggled('grayscale'))
        pixel_settings.get_invert_button().clicked.connect(
            lambda: self.on_button_toggled('invert'))
        pixel_settings.get_brightness_slider().valueChanged.connect(
            lambda val: self.on_slider_changed('brightness', val))
        pixel_settings.get_contrast_slider().valueChanged.connect(
            lambda val: self.on_slider_changed('contrast', val))
        pixel_settings.get_threshold_slider().valueChanged.connect(
            lambda val: self.on_slider_changed('threshold', val))
        
        # Area 설정 위젯 연결
        area_settings = panel.get_area_settings()
        area_settings.get_blur_slider().valueChanged.connect(
            lambda val: self.on_slider_changed('blur', val))
        area_settings.get_canny_low_slider().valueChanged.connect(
            lambda val: self.on_slider_changed('canny_low', val))
        area_settings.get_canny_high_slider().valueChanged.connect(
            lambda val: self.on_slider_changed('canny_high', val))
        area_settings.get_sharpen_slider().valueChanged.connect(
            lambda val: self.on_slider_changed('sharpen', val))
        
        # Geometric 설정 위젯 연결
        geometric_settings = panel.get_geometric_settings()
        geometric_settings.get_flip_h_button().clicked.connect(
            lambda: self.on_button_toggled('flip_h'))
        geometric_settings.get_flip_v_button().clicked.connect(
            lambda: self.on_button_toggled('flip_v'))
        geometric_settings.get_rotation_slider().valueChanged.connect(
            lambda val: self.on_slider_changed('rotation', val))
        geometric_settings.get_resize_w_slider().valueChanged.connect(
            lambda val: self.on_slider_changed('resize_w', val))
        geometric_settings.get_resize_h_slider().valueChanged.connect(
            lambda val: self.on_slider_changed('resize_h', val))
        
        # File 설정 위젯 연결
        file_settings = panel.get_file_settings()
        file_settings.get_save_button().clicked.connect(self.on_save_clicked)
        file_settings.get_save_as_button().clicked.connect(self.on_save_as_clicked)
        file_settings.get_load_button().clicked.connect(self.on_load_clicked)
        file_settings.get_undo_button().clicked.connect(self.on_undo_clicked)
        file_settings.get_redo_button().clicked.connect(self.on_redo_clicked)
        file_settings.get_settings_button().clicked.connect(self.on_settings_clicked)
        file_settings.get_exit_button().clicked.connect(self.on_exit_clicked)
        
        # 설정 패널 참조 저장
        self.settings_panel = panel
        self.pixel_settings = pixel_settings
        self.area_settings = area_settings
        self.geometric_settings = geometric_settings
        self.file_settings = file_settings
        
        return panel
    
    
    def scan_image_files(self):
        """이미지 파일 스캔 - images 폴더 기준"""
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff',
                      '*.JPG', '*.JPEG', '*.PNG', '*.BMP', '*.GIF', '*.TIFF']
        self.image_files = []
        for ext in extensions:
            # images 폴더 내에서만 검색
            pattern = os.path.join(self.images_dir, ext)
            found_files = glob.glob(pattern)
            self.image_files.extend(found_files)
        self.image_files = sorted(list(set(self.image_files)))
        print(f"스캔된 이미지 파일 수: {len(self.image_files)}")
        
        # 파일 리스트 업데이트
        self.file_list.clear()
        for file_path in self.image_files:
            file_name = os.path.basename(file_path)
            item = QListWidgetItem(file_name)
            self.file_list.addItem(item)
    
    def load_image(self, file_path):
        """이미지 로드"""
        img = cv2.imread(file_path)
        if img is not None:
            self.original_image = img
            self.processed_image = self.original_image.copy()
            self.current_file_path = file_path
            self.file_manager.set_current_file(file_path)
            # 히스토리 초기화 및 첫 이미지 추가
            self.file_manager.history = [self.original_image.copy()]
            self.file_manager.history_index = 0
            self._reset_states()
            self.update_image_display()
            self.update_file_info()
            return True
        return False
    
    def _reset_states(self):
        """상태 초기화"""
        self.button_states = {k: False for k in self.button_states}
        self.trackbar_values = {
            'brightness': 100,  # 중간값으로 변경
            'contrast': 100,
            'threshold': 127,
            'blur': 0,
            'canny_low': 50,
            'canny_high': 150,
            'sharpen': 0,
            'rotation': 0,
            'resize_w': 100,
            'resize_h': 100
        }
        
        # 슬라이더 값 초기화
        if hasattr(self, 'pixel_settings'):
            self.pixel_settings.get_brightness_slider().setValue(100)
            self.pixel_settings.get_contrast_slider().setValue(100)
            self.pixel_settings.get_threshold_slider().setValue(127)
            self.pixel_settings.get_grayscale_button().setChecked(False)
            self.pixel_settings.get_invert_button().setChecked(False)
        
        if hasattr(self, 'area_settings'):
            self.area_settings.get_blur_slider().setValue(0)
            self.area_settings.get_canny_low_slider().setValue(50)
            self.area_settings.get_canny_high_slider().setValue(150)
            self.area_settings.get_sharpen_slider().setValue(0)
        
        if hasattr(self, 'geometric_settings'):
            self.geometric_settings.get_rotation_slider().setValue(0)
            self.geometric_settings.get_resize_w_slider().setValue(100)
            self.geometric_settings.get_resize_h_slider().setValue(100)
            self.geometric_settings.get_flip_h_button().setChecked(False)
            self.geometric_settings.get_flip_v_button().setChecked(False)
    
    def on_file_selected(self, item):
        """파일 선택 이벤트"""
        index = self.file_list.row(item)
        if 0 <= index < len(self.image_files):
            self.load_image(self.image_files[index])
    
    def on_file_dropped(self, file_path):
        """파일 드롭 이벤트 - 이미 images 폴더로 복사된 파일"""
        # 파일이 이미 images 폴더에 복사되어 있음
        self.load_image(file_path)
        # 파일 리스트 업데이트
        self.scan_image_files()
        # 현재 파일을 리스트에서 선택
        if file_path in self.image_files:
            index = self.image_files.index(file_path)
            self.file_list.setCurrentRow(index)
    
    def on_tab_clicked(self, tab_name):
        """탭 클릭 이벤트"""
        # File 카테고리는 detail 패널을 표시하지 않음
        if tab_name == 'File':
            return
        
        self.current_tab = tab_name
        # 모든 탭 버튼 해제
        for btn in self.tab_buttons.values():
            btn.setChecked(False)
        # 선택된 탭만 체크
        self.tab_buttons[tab_name].setChecked(True)
        self.update_settings_visibility()
    
    def on_file_menu_action(self, action_name):
        """File 메뉴 항목 클릭 이벤트 - 바로 실행"""
        if action_name == 'Save':
            self.on_save_clicked()
        elif action_name == 'Save As':
            self.on_save_as_clicked()
        elif action_name == 'Load':
            self.on_load_clicked()
        elif action_name == 'Undo':
            self.on_undo_clicked()
        elif action_name == 'Redo':
            self.on_redo_clicked()
        elif action_name == 'Settings':
            self.on_settings_clicked()
        elif action_name == 'Exit':
            self.on_exit_clicked()
    
    def update_settings_visibility(self):
        """설정 패널 가시성 업데이트"""
        if hasattr(self, 'settings_panel'):
            self.settings_panel.set_current_tab(self.current_tab)
    
    def on_button_toggled(self, button_key):
        """버튼 토글 이벤트"""
        if button_key in self.button_states:
            # Pixel 설정에서 버튼 찾기
            if button_key == 'grayscale' and hasattr(self, 'pixel_settings'):
                self.button_states[button_key] = self.pixel_settings.get_grayscale_button().isChecked()
            elif button_key == 'invert' and hasattr(self, 'pixel_settings'):
                self.button_states[button_key] = self.pixel_settings.get_invert_button().isChecked()
            # Geometric 설정에서 버튼 찾기
            elif button_key == 'flip_h' and hasattr(self, 'geometric_settings'):
                self.button_states[button_key] = self.geometric_settings.get_flip_h_button().isChecked()
            elif button_key == 'flip_v' and hasattr(self, 'geometric_settings'):
                self.button_states[button_key] = self.geometric_settings.get_flip_v_button().isChecked()
            self.apply_all_effects()
    
    def on_slider_changed(self, key, value):
        """슬라이더 변경 이벤트"""
        self.trackbar_values[key] = value
        self.apply_all_effects()
    
    def on_reset_clicked(self):
        """리셋 버튼 클릭"""
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self._reset_states()
            self.apply_all_effects()
    
    def apply_all_effects(self):
        """모든 효과 적용"""
        if self.original_image is None:
            return
        
        img = self.original_image.copy()
        
        # 버튼 효과
        if self.button_states['grayscale']:
            img = pixel_processing.to_grayscale(img)
        if self.button_states['invert']:
            img = pixel_processing.apply_invert(img)
        if self.button_states['flip_h']:
            img = geometric_processing.apply_flip_horizontal(img)
        if self.button_states['flip_v']:
            img = geometric_processing.apply_flip_vertical(img)
        
        # 트랙바 효과
        if self.trackbar_values['brightness'] != 100:
            img = pixel_processing.apply_brightness(img, self.trackbar_values['brightness'])
        if self.trackbar_values['contrast'] != 100:
            img = pixel_processing.apply_contrast(img, self.trackbar_values['contrast'])
        if self.trackbar_values['blur'] > 0:
            img = area_processing.apply_blur(img, self.trackbar_values['blur'])
        if self.trackbar_values['canny_low'] != 50 or self.trackbar_values['canny_high'] != 150:
            img = area_processing.apply_canny(img, self.trackbar_values['canny_low'],
                                             self.trackbar_values['canny_high'])
        if self.trackbar_values['threshold'] != 127:
            img = pixel_processing.apply_threshold(img, self.trackbar_values['threshold'])
        if self.trackbar_values['rotation'] != 0:
            img = geometric_processing.apply_rotation(img, self.trackbar_values['rotation'])
        
        # Resize 적용 (퍼센트 값으로 처리)
        if self.trackbar_values['resize_w'] != 100 or self.trackbar_values['resize_h'] != 100:
            h, w = img.shape[:2]
            # 퍼센트를 실제 크기로 변환
            new_width = int(w * self.trackbar_values['resize_w'] / 100.0)
            new_height = int(h * self.trackbar_values['resize_h'] / 100.0)
            img = geometric_processing.apply_resize(img, width=new_width, height=new_height)
        
        self.processed_image = img
        # 히스토리에 추가 (이미지 처리 후)
        if self.original_image is not None:
            self.file_manager.add_to_history(self.processed_image)
        self.update_image_display()
    
    def update_image_display(self):
        """이미지 표시 업데이트"""
        self.image_display.set_image(self.processed_image)
    
    def update_file_info(self):
        """파일 정보 업데이트"""
        if self.current_file_path:
            file_name = os.path.basename(self.current_file_path)
            file_size = os.path.getsize(self.current_file_path)
            if file_size < 1024:
                size_str = f"{file_size} B"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            
            ext = os.path.splitext(file_name)[1].upper()
            self.info_label.setText(f"File: {file_name} | Extension: {ext} | Size: {size_str}")
        else:
            self.info_label.setText(f"File: No Image | Size: {len(self.image_files)} files")
    
    def on_save_clicked(self):
        """저장하기 버튼 클릭"""
        if self.processed_image is not None and self.current_file_path:
            if self.file_saver.save(self.processed_image, self.current_file_path):
                QMessageBox.information(self, "저장 완료", "파일이 저장되었습니다.")
            else:
                QMessageBox.warning(self, "저장 실패", "파일 저장에 실패했습니다.")
        else:
            QMessageBox.warning(self, "저장 불가", "저장할 이미지가 없습니다.")
    
    def on_save_as_clicked(self):
        """다른이름으로 저장하기 버튼 클릭"""
        if self.processed_image is not None:
            saved_path = self.file_saver.save_as(self.processed_image, self.current_file_path)
            if saved_path:
                self.current_file_path = saved_path
                self.file_manager.set_current_file(saved_path)
                self.update_file_info()
                QMessageBox.information(self, "저장 완료", "파일이 저장되었습니다.")
        else:
            QMessageBox.warning(self, "저장 불가", "저장할 이미지가 없습니다.")
    
    def on_load_clicked(self):
        """불러오기 버튼 클릭 - 파일을 images 폴더로 복사 후 로드"""
        file_path, image = self.file_loader.load_from_dialog(self.current_file_path)
        if file_path and image is not None:
            # 파일명 추출 및 복사
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.images_dir, file_name)
            
            # 동일한 파일명이 있으면 번호 추가
            counter = 1
            base_name, ext_name = os.path.splitext(file_name)
            while os.path.exists(dest_path):
                new_name = f"{base_name}_{counter}{ext_name}"
                dest_path = os.path.join(images_dir, new_name)
                counter += 1
            
            # 파일 복사
            import shutil
            try:
                shutil.copy2(file_path, dest_path)
                # 복사된 파일 로드
                self.load_image(dest_path)
                # 파일 리스트 업데이트
                self.scan_image_files()
                # 현재 파일을 리스트에서 선택
                if dest_path in self.image_files:
                    index = self.image_files.index(dest_path)
                    self.file_list.setCurrentRow(index)
            except Exception as e:
                QMessageBox.warning(self, "복사 실패", f"파일 복사에 실패했습니다: {str(e)}")
    
    def on_undo_clicked(self):
        """되돌리기 버튼 클릭"""
        if self.history_manager.can_undo():
            image = self.history_manager.undo()
            if image is not None:
                self.processed_image = image
                self.update_image_display()
        else:
            QMessageBox.information(self, "되돌리기", "더 이상 되돌릴 수 없습니다.")
    
    def on_redo_clicked(self):
        """앞으로 돌리기 버튼 클릭"""
        if self.history_manager.can_redo():
            image = self.history_manager.redo()
            if image is not None:
                self.processed_image = image
                self.update_image_display()
        else:
            QMessageBox.information(self, "앞으로 돌리기", "더 이상 앞으로 돌릴 수 없습니다.")
    
    def on_settings_clicked(self):
        """설정하기 버튼 클릭"""
        self.settings_manager.show_settings_dialog()
    
    def on_exit_clicked(self):
        """종료하기 버튼 클릭"""
        reply = QMessageBox.question(
            self, "종료 확인", "정말 종료하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            file_operations.ApplicationManager.exit_application()


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    # 다크 테마 스타일
    app.setStyle('Fusion')
    palette = app.palette()
    palette.setColor(palette.Window, Qt.darkGray)
    palette.setColor(palette.WindowText, Qt.white)
    app.setPalette(palette)
    
    editor = ImageEditor()
    editor.show()
    
    # 첫 번째 이미지 자동 로드
    if len(editor.image_files) > 0:
        editor.load_image(editor.image_files[0])
        editor.file_list.setCurrentRow(0)
    else:
        # 테스트 이미지 생성
        test_image = np.zeros((400, 600, 3), dtype=np.uint8)
        cv2.rectangle(test_image, (50, 50), (550, 350), (100, 150, 200), -1)
        cv2.putText(test_image, "Test Image - Drag to move", (150, 200),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        editor.original_image = test_image
        editor.processed_image = test_image.copy()
        editor.update_image_display()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
