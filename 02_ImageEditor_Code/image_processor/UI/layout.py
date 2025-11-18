"""
레이아웃 관리자
UI 요소들의 위치와 크기를 관리
"""

from .constants import UIConstants
from .components import Tab, Button, FileList, SettingsPanel, DropdownMenu


class LayoutManager:
    """레이아웃 관리자 클래스"""
    
    def __init__(self):
        self.width = UIConstants.WINDOW_WIDTH
        self.height = UIConstants.WINDOW_HEIGHT
        self.file_list_width = UIConstants.FILE_LIST_WIDTH
        
        # 영역 계산
        self.top_bar_rect = (0, 0, self.width, UIConstants.TOP_BAR_HEIGHT)
        self.info_bar_rect = (0, UIConstants.TOP_BAR_HEIGHT, self.width, UIConstants.INFO_BAR_HEIGHT)
        self.file_list_rect = (0, UIConstants.TOP_BAR_HEIGHT + UIConstants.INFO_BAR_HEIGHT,
                               self.file_list_width, 
                               self.height - UIConstants.TOP_BAR_HEIGHT - UIConstants.INFO_BAR_HEIGHT - UIConstants.SETTINGS_PANEL_HEIGHT)
        self.image_area_rect = (self.file_list_width + UIConstants.PADDING * 2,
                                UIConstants.TOP_BAR_HEIGHT + UIConstants.INFO_BAR_HEIGHT + UIConstants.PADDING,
                                self.width - self.file_list_width - UIConstants.PADDING * 4,
                                self.height - UIConstants.TOP_BAR_HEIGHT - UIConstants.INFO_BAR_HEIGHT - UIConstants.SETTINGS_PANEL_HEIGHT - UIConstants.PADDING * 2)
        self.settings_panel_rect = (self.file_list_width + UIConstants.PADDING * 2,
                                   self.height - UIConstants.SETTINGS_PANEL_HEIGHT,
                                   self.width - self.file_list_width - UIConstants.PADDING * 4,
                                   UIConstants.SETTINGS_PANEL_HEIGHT)
    
    def create_tabs(self):
        """탭 생성"""
        tabs = {}
        tab_width = 80
        tab_height = UIConstants.TAB_HEIGHT
        start_x = UIConstants.PADDING
        start_y = UIConstants.PADDING
        
        for i, tab_name in enumerate(UIConstants.TABS):
            if tab_name == 'Geometric':
                tab_width = 100
            x = start_x + i * (tab_width + UIConstants.SPACING)
            tabs[tab_name] = Tab(x, start_y, tab_width, tab_height, tab_name)
        
        return tabs
    
    def create_file_list(self):
        """파일 리스트 생성"""
        x, y, w, h = self.file_list_rect
        return FileList(x, y, w, h)
    
    def create_settings_panel(self):
        """설정 패널 생성"""
        x, y, w, h = self.settings_panel_rect
        panel = SettingsPanel(x, y, w, h)
        
        # 버튼 및 라벨 위치 계산
        btn_y = y + 30
        btn_width = 110
        btn_height = 35
        trackbar_width = 180
        spacing = 15
        
        # Pixel 탭 버튼들
        btn_x = x + UIConstants.PADDING * 2
        panel.add_button('grayscale', Button(
            btn_x, btn_y, btn_width, btn_height, 'Grayscale'
        ))
        panel.add_button('invert', Button(
            btn_x + btn_width + spacing, btn_y, btn_width, btn_height, 'Invert'
        ))
        
        # Pixel 탭 트랙바 라벨
        trackbar_x = btn_x + (btn_width + spacing) * 2 + spacing
        panel.add_trackbar_label('brightness', trackbar_x, btn_y + 22, 
                                lambda: f'Brightness: {0}')
        panel.add_trackbar_label('contrast', 
                                trackbar_x + trackbar_width + spacing, 
                                btn_y + 22, lambda: f'Contrast: {100}')
        panel.add_trackbar_label('threshold',
                                trackbar_x + (trackbar_width + spacing) * 2,
                                btn_y + 22, lambda: f'Threshold: {127}')
        
        # Area 탭 트랙바 라벨
        panel.add_trackbar_label('blur', btn_x, btn_y + 22, lambda: f'Blur: {0}')
        panel.add_trackbar_label('canny_low',
                                btn_x + trackbar_width + spacing,
                                btn_y + 22, lambda: f'Canny Low: {50}')
        panel.add_trackbar_label('canny_high',
                                btn_x + (trackbar_width + spacing) * 2,
                                btn_y + 22, lambda: f'Canny High: {150}')
        panel.add_trackbar_label('sharpen',
                                btn_x + (trackbar_width + spacing) * 3,
                                btn_y + 22, lambda: f'Sharpen: {0}')
        
        # Geometric 탭 버튼 및 라벨
        panel.add_button('flip_h', Button(
            btn_x, btn_y, btn_width, btn_height, 'Flip H'
        ))
        panel.add_button('flip_v', Button(
            btn_x + btn_width + spacing, btn_y, btn_width, btn_height, 'Flip V'
        ))
        panel.add_trackbar_label('rotation', 
                                btn_x + (btn_width + spacing) * 2 + spacing,
                                btn_y + 22, lambda: f'Rotation: {0}°')
        panel.add_trackbar_label('resize_w',
                                btn_x + (btn_width + spacing) * 2 + spacing + trackbar_width + spacing,
                                btn_y + 22, lambda: f'Resize W: {100}%')
        panel.add_trackbar_label('resize_h',
                                btn_x + (btn_width + spacing) * 2 + spacing + (trackbar_width + spacing) * 2,
                                btn_y + 22, lambda: f'Resize H: {100}%')
        
        # RESET 버튼 (항상 오른쪽 끝)
        reset_btn = Button(self.width - 160, btn_y, 150, btn_height, 'RESET',
                          color=UIConstants.COLOR_RESET_BTN)
        panel.add_button('reset', reset_btn)
        
        return panel
    
    def create_dropdown_menu(self, tab_name, tab_x, tab_y):
        """드롭다운 메뉴 생성"""
        items = UIConstants.MENU_ITEMS.get(tab_name, [])
        menu_y = tab_y + UIConstants.TAB_HEIGHT
        return DropdownMenu(0, menu_y, items)

