"""
UI 모듈
SOLID 원칙에 따라 UI 관련 기능을 모듈화
PyQt5 기반으로 재구성
"""

from .constants import UIConstants
from .settings_panel import SettingsPanel, PixelSettings, AreaSettings, GeometricSettings
from .widgets import FileListWidget, ImageDisplayWidget, TopBarWidget, InfoBarWidget
from .layout_manager import LayoutManager

# 레거시 모듈 (OpenCV 기반 - 참고용)
from .components import Button, Tab, FileList, SettingsPanel as LegacySettingsPanel, DropdownMenu
from .layout import LayoutManager as LegacyLayoutManager
from .renderer import UIRenderer
from .event_handler import EventHandler

__all__ = [
    # PyQt5 기반 모듈
    'UIConstants',
    'SettingsPanel',
    'PixelSettings',
    'AreaSettings',
    'GeometricSettings',
    'FileListWidget',
    'ImageDisplayWidget',
    'TopBarWidget',
    'InfoBarWidget',
    'LayoutManager',
    # 레거시 모듈 (OpenCV 기반)
    'Button',
    'Tab',
    'FileList',
    'LegacySettingsPanel',
    'DropdownMenu',
    'LegacyLayoutManager',
    'UIRenderer',
    'EventHandler'
]

