"""
설정 패널 모듈
SOLID 원칙에 따라 설정 패널 관련 기능을 모듈화
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, 
    QLabel, QGroupBox, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal


class SettingsPanel(QWidget):
    """설정 패널 메인 위젯 (단일 책임: 설정 패널 레이아웃 관리)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(280)  # 크기 확대: 180 -> 280
        self.setStyleSheet("background-color: #282828; border-top: 2px solid #404040;")
        
        self.current_tab = 'Pixel'
        self.pixel_settings = None
        self.area_settings = None
        self.geometric_settings = None
        self.file_settings = None
        
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화 - 탭별로 필터링된 설정 표시"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        
        # 제목
        title = QLabel('Detailed Settings')
        title.setStyleSheet("color: #dcdcdc; font-size: 12px; font-weight: bold;")
        layout.addWidget(title)
        
        # 스크롤 가능한 설정 영역
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        self.settings_container = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_container)
        self.settings_layout.setSpacing(5)
        self.settings_layout.setContentsMargins(5, 5, 5, 5)
        
        # 각 탭별 설정 위젯 생성
        self.pixel_settings = PixelSettings()
        self.area_settings = AreaSettings()
        self.geometric_settings = GeometricSettings()
        self.file_settings = FileSettings()
        
        scroll_area.setWidget(self.settings_container)
        layout.addWidget(scroll_area)
        
        # RESET 버튼 (하단 고정)
        reset_container = QWidget()
        reset_layout = QHBoxLayout(reset_container)
        reset_layout.addStretch()
        self.reset_btn = QPushButton('RESET')
        self.reset_btn.setFixedSize(120, 35)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #b43228;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #c84238;
            }
        """)
        reset_layout.addWidget(self.reset_btn)
        layout.addWidget(reset_container)
        
        # 초기 표시 (Pixel 탭)
        self.update_visibility()
    
    def set_current_tab(self, tab_name):
        """현재 탭 설정 및 가시성 업데이트"""
        self.current_tab = tab_name
        self.update_visibility()
    
    def update_visibility(self):
        """설정 위젯 가시성 업데이트 - 선택된 탭만 표시"""
        # 기존 위젯 제거
        while self.settings_layout.count():
            item = self.settings_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        
        # 선택된 탭에 맞는 위젯만 추가
        if self.current_tab == 'Pixel':
            self.settings_layout.addWidget(self.pixel_settings)
        elif self.current_tab == 'Area':
            self.settings_layout.addWidget(self.area_settings)
        elif self.current_tab == 'Geometric':
            self.settings_layout.addWidget(self.geometric_settings)
        elif self.current_tab == 'File':
            self.settings_layout.addWidget(self.file_settings)
        
        self.settings_layout.addStretch()
    
    def get_reset_button(self):
        """RESET 버튼 반환"""
        return self.reset_btn
    
    def get_pixel_settings(self):
        """Pixel 설정 위젯 반환"""
        return self.pixel_settings
    
    def get_area_settings(self):
        """Area 설정 위젯 반환"""
        return self.area_settings
    
    def get_geometric_settings(self):
        """Geometric 설정 위젯 반환"""
        return self.geometric_settings
    
    def get_file_settings(self):
        """File 설정 위젯 반환"""
        return self.file_settings


class PixelSettings(QWidget):
    """Pixel 처리 설정 위젯 (단일 책임: Pixel 처리 관련 컨트롤)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화 - 각 기능을 1줄씩 세로로 배치"""
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Grayscale 버튼 (1줄)
        grayscale_row = QHBoxLayout()
        grayscale_row.addWidget(QLabel('Grayscale:'))
        self.grayscale_btn = self._create_toggle_button('Grayscale', 100, 30)
        grayscale_row.addWidget(self.grayscale_btn)
        grayscale_row.addStretch()
        layout.addLayout(grayscale_row)
        
        # Invert 버튼 (1줄)
        invert_row = QHBoxLayout()
        invert_row.addWidget(QLabel('Invert:'))
        self.invert_btn = self._create_toggle_button('Invert', 100, 30)
        invert_row.addWidget(self.invert_btn)
        invert_row.addStretch()
        layout.addLayout(invert_row)
        
        # Brightness 슬라이더 (1줄)
        self.brightness_group = self._create_slider_group_row('Brightness', 0, 200, 100)
        layout.addLayout(self.brightness_group)
        
        # Contrast 슬라이더 (1줄)
        self.contrast_group = self._create_slider_group_row('Contrast', 0, 200, 100)
        layout.addLayout(self.contrast_group)
        
        # Threshold 슬라이더 (1줄)
        self.threshold_group = self._create_slider_group_row('Threshold', 0, 255, 127)
        layout.addLayout(self.threshold_group)
    
    def _create_toggle_button(self, text, width, height):
        """토글 버튼 생성"""
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setFixedSize(width, height)
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
                background-color: #00c800;
                color: white;
            }
        """)
        return btn
    
    def _create_slider_group_row(self, label_text, min_val, max_val, default_val):
        """슬라이더 그룹 생성 (1줄 레이아웃)"""
        row = QHBoxLayout()
        
        # 라벨
        label = QLabel(f'{label_text}:')
        label.setFixedWidth(100)
        label.setStyleSheet("color: #dcdcdc; font-size: 11px;")
        row.addWidget(label)
        
        # 슬라이더
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        slider.setMinimumWidth(200)
        row.addWidget(slider)
        
        # 값 표시 라벨
        value_label = QLabel(str(default_val))
        value_label.setFixedWidth(50)
        value_label.setStyleSheet("color: #dcdcdc; font-size: 11px;")
        value_label.setAlignment(Qt.AlignCenter)
        slider.valueChanged.connect(lambda val: value_label.setText(str(val)))
        row.addWidget(value_label)
        
        row.addStretch()
        
        # 슬라이더를 레이아웃에 저장하기 위해 속성 추가
        row.slider = slider
        row.value_label = value_label
        
        return row
    
    def get_grayscale_button(self):
        """Grayscale 버튼 반환"""
        return self.grayscale_btn
    
    def get_invert_button(self):
        """Invert 버튼 반환"""
        return self.invert_btn
    
    def get_brightness_slider(self):
        """Brightness 슬라이더 반환"""
        return self.brightness_group.slider
    
    def get_contrast_slider(self):
        """Contrast 슬라이더 반환"""
        return self.contrast_group.slider
    
    def get_threshold_slider(self):
        """Threshold 슬라이더 반환"""
        return self.threshold_group.slider


class AreaSettings(QWidget):
    """Area 처리 설정 위젯 (단일 책임: Area 처리 관련 컨트롤)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화 - 각 기능을 1줄씩 세로로 배치"""
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Blur 슬라이더 (1줄)
        self.blur_group = self._create_slider_group_row('Blur', 0, 20, 0)
        layout.addLayout(self.blur_group)
        
        # Canny Low 슬라이더 (1줄)
        self.canny_low_group = self._create_slider_group_row('Canny Low', 0, 255, 50)
        layout.addLayout(self.canny_low_group)
        
        # Canny High 슬라이더 (1줄)
        self.canny_high_group = self._create_slider_group_row('Canny High', 0, 255, 150)
        layout.addLayout(self.canny_high_group)
        
        # Sharpen 슬라이더 (1줄)
        self.sharpen_group = self._create_slider_group_row('Sharpen', 0, 100, 0)
        layout.addLayout(self.sharpen_group)
    
    def _create_slider_group_row(self, label_text, min_val, max_val, default_val):
        """슬라이더 그룹 생성 (1줄 레이아웃)"""
        row = QHBoxLayout()
        
        # 라벨
        label = QLabel(f'{label_text}:')
        label.setFixedWidth(100)
        label.setStyleSheet("color: #dcdcdc; font-size: 11px;")
        row.addWidget(label)
        
        # 슬라이더
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        slider.setMinimumWidth(200)
        row.addWidget(slider)
        
        # 값 표시 라벨
        value_label = QLabel(str(default_val))
        value_label.setFixedWidth(50)
        value_label.setStyleSheet("color: #dcdcdc; font-size: 11px;")
        value_label.setAlignment(Qt.AlignCenter)
        slider.valueChanged.connect(lambda val: value_label.setText(str(val)))
        row.addWidget(value_label)
        
        row.addStretch()
        
        # 슬라이더를 레이아웃에 저장하기 위해 속성 추가
        row.slider = slider
        row.value_label = value_label
        
        return row
    
    def get_blur_slider(self):
        """Blur 슬라이더 반환"""
        return self.blur_group.slider
    
    def get_canny_low_slider(self):
        """Canny Low 슬라이더 반환"""
        return self.canny_low_group.slider
    
    def get_canny_high_slider(self):
        """Canny High 슬라이더 반환"""
        return self.canny_high_group.slider
    
    def get_sharpen_slider(self):
        """Sharpen 슬라이더 반환"""
        return self.sharpen_group.slider


class GeometricSettings(QWidget):
    """Geometric 처리 설정 위젯 (단일 책임: Geometric 처리 관련 컨트롤)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화 - 각 기능을 1줄씩 세로로 배치"""
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Flip H 버튼 (1줄)
        flip_h_row = QHBoxLayout()
        flip_h_row.addWidget(QLabel('Flip H:'))
        self.flip_h_btn = self._create_toggle_button('Flip H', 100, 30)
        flip_h_row.addWidget(self.flip_h_btn)
        flip_h_row.addStretch()
        layout.addLayout(flip_h_row)
        
        # Flip V 버튼 (1줄)
        flip_v_row = QHBoxLayout()
        flip_v_row.addWidget(QLabel('Flip V:'))
        self.flip_v_btn = self._create_toggle_button('Flip V', 100, 30)
        flip_v_row.addWidget(self.flip_v_btn)
        flip_v_row.addStretch()
        layout.addLayout(flip_v_row)
        
        # Rotation 슬라이더 (1줄)
        self.rotation_group = self._create_slider_group_row('Rotation', 0, 360, 0)
        layout.addLayout(self.rotation_group)
        
        # Resize W 슬라이더 (1줄)
        self.resize_w_group = self._create_slider_group_row('Resize W', 10, 200, 100)
        layout.addLayout(self.resize_w_group)
        
        # Resize H 슬라이더 (1줄)
        self.resize_h_group = self._create_slider_group_row('Resize H', 10, 200, 100)
        layout.addLayout(self.resize_h_group)
    
    def _create_toggle_button(self, text, width, height):
        """토글 버튼 생성"""
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setFixedSize(width, height)
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
                background-color: #00c800;
                color: white;
            }
        """)
        return btn
    
    def _create_slider_group_row(self, label_text, min_val, max_val, default_val):
        """슬라이더 그룹 생성 (1줄 레이아웃)"""
        row = QHBoxLayout()
        
        # 라벨
        label = QLabel(f'{label_text}:')
        label.setFixedWidth(100)
        label.setStyleSheet("color: #dcdcdc; font-size: 11px;")
        row.addWidget(label)
        
        # 슬라이더
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        slider.setMinimumWidth(200)
        row.addWidget(slider)
        
        # 값 표시 라벨
        value_label = QLabel(str(default_val))
        value_label.setFixedWidth(50)
        value_label.setStyleSheet("color: #dcdcdc; font-size: 11px;")
        value_label.setAlignment(Qt.AlignCenter)
        slider.valueChanged.connect(lambda val: value_label.setText(str(val)))
        row.addWidget(value_label)
        
        row.addStretch()
        
        # 슬라이더를 레이아웃에 저장하기 위해 속성 추가
        row.slider = slider
        row.value_label = value_label
        
        return row
    
    def get_flip_h_button(self):
        """Flip H 버튼 반환"""
        return self.flip_h_btn
    
    def get_flip_v_button(self):
        """Flip V 버튼 반환"""
        return self.flip_v_btn
    
    def get_rotation_slider(self):
        """Rotation 슬라이더 반환"""
        return self.rotation_group.slider
    
    def get_resize_w_slider(self):
        """Resize W 슬라이더 반환"""
        return self.resize_w_group.slider
    
    def get_resize_h_slider(self):
        """Resize H 슬라이더 반환"""
        return self.resize_h_group.slider


class FileSettings(QWidget):
    """File 처리 설정 위젯 (단일 책임: File 처리 관련 컨트롤)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화 - 각 기능을 1줄씩 세로로 배치"""
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 저장하기 버튼 (1줄)
        save_row = QHBoxLayout()
        save_row.addWidget(QLabel('Save:'))
        self.save_btn = self._create_button('Save', 120, 30)
        save_row.addWidget(self.save_btn)
        save_row.addStretch()
        layout.addLayout(save_row)
        
        # 다른이름으로 저장하기 버튼 (1줄)
        save_as_row = QHBoxLayout()
        save_as_row.addWidget(QLabel('Save As:'))
        self.save_as_btn = self._create_button('Save As', 120, 30)
        save_as_row.addWidget(self.save_as_btn)
        save_as_row.addStretch()
        layout.addLayout(save_as_row)
        
        # 불러오기 버튼 (1줄)
        load_row = QHBoxLayout()
        load_row.addWidget(QLabel('Load:'))
        self.load_btn = self._create_button('Load', 120, 30)
        load_row.addWidget(self.load_btn)
        load_row.addStretch()
        layout.addLayout(load_row)
        
        # 되돌리기 버튼 (1줄)
        undo_row = QHBoxLayout()
        undo_row.addWidget(QLabel('Undo:'))
        self.undo_btn = self._create_button('Undo', 120, 30)
        undo_row.addWidget(self.undo_btn)
        undo_row.addStretch()
        layout.addLayout(undo_row)
        
        # 앞으로 돌리기 버튼 (1줄)
        redo_row = QHBoxLayout()
        redo_row.addWidget(QLabel('Redo:'))
        self.redo_btn = self._create_button('Redo', 120, 30)
        redo_row.addWidget(self.redo_btn)
        redo_row.addStretch()
        layout.addLayout(redo_row)
        
        # 설정하기 버튼 (1줄)
        settings_row = QHBoxLayout()
        settings_row.addWidget(QLabel('Settings:'))
        self.settings_btn = self._create_button('Settings', 120, 30)
        settings_row.addWidget(self.settings_btn)
        settings_row.addStretch()
        layout.addLayout(settings_row)
        
        # 종료하기 버튼 (1줄)
        exit_row = QHBoxLayout()
        exit_row.addWidget(QLabel('Exit:'))
        self.exit_btn = self._create_button('Exit', 120, 30)
        exit_row.addWidget(self.exit_btn)
        exit_row.addStretch()
        layout.addLayout(exit_row)
    
    def _create_button(self, text, width, height):
        """버튼 생성"""
        btn = QPushButton(text)
        btn.setFixedSize(width, height)
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
        """)
        return btn
    
    def get_save_button(self):
        """Save 버튼 반환"""
        return self.save_btn
    
    def get_save_as_button(self):
        """Save As 버튼 반환"""
        return self.save_as_btn
    
    def get_load_button(self):
        """Load 버튼 반환"""
        return self.load_btn
    
    def get_undo_button(self):
        """Undo 버튼 반환"""
        return self.undo_btn
    
    def get_redo_button(self):
        """Redo 버튼 반환"""
        return self.redo_btn
    
    def get_settings_button(self):
        """Settings 버튼 반환"""
        return self.settings_btn
    
    def get_exit_button(self):
        """Exit 버튼 반환"""
        return self.exit_btn

