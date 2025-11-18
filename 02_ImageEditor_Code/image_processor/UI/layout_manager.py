"""
PyQt5 기반 레이아웃 관리자
UI 요소들의 레이아웃을 관리
"""

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from .constants import UIConstants


class LayoutManager:
    """레이아웃 관리자 클래스 (PyQt5 기반)"""
    
    def __init__(self):
        self.width = UIConstants.WINDOW_WIDTH
        self.height = UIConstants.WINDOW_HEIGHT
        self.file_list_width = UIConstants.FILE_LIST_WIDTH
    
    def create_main_layout(self):
        """메인 레이아웃 생성"""
        return QHBoxLayout()
    
    def create_right_panel_layout(self):
        """오른쪽 패널 레이아웃 생성"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        return layout
    
    def create_left_panel_layout(self):
        """왼쪽 패널 레이아웃 생성"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        return layout
    
    def create_settings_layout(self):
        """설정 패널 레이아웃 생성"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        return layout

