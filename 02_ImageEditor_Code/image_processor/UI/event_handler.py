"""
이벤트 핸들러
마우스 및 키보드 이벤트 처리 (Single Responsibility)
"""

import cv2
from .constants import UIConstants


class EventHandler:
    """이벤트 핸들러 클래스"""
    
    def __init__(self, layout_manager, tabs, file_list, settings_panel, dropdown_menu):
        self.layout = layout_manager
        self.tabs = tabs
        self.file_list = file_list
        self.settings_panel = settings_panel
        self.dropdown_menu = dropdown_menu
        
        self.current_tab = 'Pixel'
        self.menu_visible = False
        self.callbacks = {}
    
    def register_callback(self, event_type, callback):
        """콜백 함수 등록"""
        self.callbacks[event_type] = callback
    
    def handle_mouse(self, event, x, y, flags, param):
        """마우스 이벤트 처리"""
        if event == cv2.EVENT_LBUTTONDOWN:
            # 탭 클릭 확인
            clicked_tab = None
            for tab_name, tab in self.tabs.items():
                if tab.contains(x, y):
                    clicked_tab = tab_name
                    break
            
            if clicked_tab:
                if self.current_tab == clicked_tab:
                    self.menu_visible = not self.menu_visible
                else:
                    self.current_tab = clicked_tab
                    self.menu_visible = True
                    self.dropdown_menu.items = UIConstants.MENU_ITEMS.get(clicked_tab, [])
                    self.dropdown_menu.x = self.tabs[clicked_tab].x
                if 'tab_clicked' in self.callbacks:
                    self.callbacks['tab_clicked'](clicked_tab)
            else:
                # 탭 외부 클릭 시 메뉴 닫기
                if y > UIConstants.TOP_BAR_HEIGHT:
                    self.menu_visible = False
            
            # 파일 리스트 클릭
            file_index = self.file_list.get_clicked_index(x, y)
            if file_index >= 0:
                self.file_list.selected_index = file_index
                if 'file_clicked' in self.callbacks:
                    self.callbacks['file_clicked'](file_index)
            
            # 설정 패널 버튼 클릭
            for key, button in self.settings_panel.buttons.items():
                if button.contains(x, y):
                    if 'button_clicked' in self.callbacks:
                        self.callbacks['button_clicked'](key)
                    break
    
    def get_current_tab(self):
        """현재 활성 탭 반환"""
        return self.current_tab
    
    def is_menu_visible(self):
        """메뉴 표시 여부 반환"""
        return self.menu_visible
    
    def update_button_state(self, key, is_active):
        """버튼 상태 업데이트"""
        if key in self.settings_panel.buttons:
            self.settings_panel.buttons[key].is_active = is_active
    
    def update_trackbar_labels(self, trackbar_values):
        """트랙바 라벨 업데이트"""
        def make_getter(key, value):
            """클로저를 사용하여 값 저장"""
            if key == 'brightness':
                return lambda: f'Brightness: {value}'
            elif key == 'contrast':
                return lambda: f'Contrast: {value}'
            elif key == 'threshold':
                return lambda: f'Threshold: {value}'
            elif key == 'blur':
                return lambda: f'Blur: {value}'
            elif key == 'canny_low':
                return lambda: f'Canny Low: {value}'
            elif key == 'canny_high':
                return lambda: f'Canny High: {value}'
            elif key == 'sharpen':
                return lambda: f'Sharpen: {value}'
            elif key == 'rotation':
                return lambda: f'Rotation: {value}°'
            elif key == 'resize_w':
                return lambda: f'Resize W: {value}%'
            elif key == 'resize_h':
                return lambda: f'Resize H: {value}%'
            return lambda: f'{key}: {value}'
        
        for key, label_info in self.settings_panel.trackbar_labels.items():
            if key in trackbar_values:
                value = trackbar_values[key]
                label_info['text_getter'] = make_getter(key, value)

