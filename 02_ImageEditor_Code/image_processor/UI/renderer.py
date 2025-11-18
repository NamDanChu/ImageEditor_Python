"""
UI 렌더러
모든 UI 요소를 그리는 책임을 가짐 (Single Responsibility)
"""

import cv2
import numpy as np
from .constants import UIConstants


class UIRenderer:
    """UI 렌더러 클래스"""
    
    def __init__(self, layout_manager):
        self.layout = layout_manager
    
    def create_canvas(self):
        """새 캔버스 생성"""
        return np.full((UIConstants.WINDOW_HEIGHT, UIConstants.WINDOW_WIDTH, 3),
                      UIConstants.COLOR_BG, dtype=np.uint8)
    
    def draw_top_bar(self, canvas):
        """상단 바 그리기"""
        x, y, w, h = self.layout.top_bar_rect
        cv2.rectangle(canvas, (x, y), (x + w, y + h), UIConstants.COLOR_PANEL, -1)
    
    def draw_info_bar(self, canvas, file_info):
        """정보 바 그리기"""
        x, y, w, h = self.layout.info_bar_rect
        cv2.rectangle(canvas, (x, y), (x + w, y + h), UIConstants.COLOR_PANEL_DARK, -1)
        cv2.putText(canvas, file_info, (x + UIConstants.PADDING, y + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_MEDIUM,
                   UIConstants.COLOR_TEXT, UIConstants.FONT_THICKNESS)
    
    def draw_tabs(self, canvas, tabs, active_tab):
        """탭들 그리기"""
        for tab_name, tab in tabs.items():
            tab.is_active = (tab_name == active_tab)
            tab.draw(canvas)
    
    def draw_file_list(self, canvas, file_list):
        """파일 리스트 그리기"""
        file_list.draw(canvas)
    
    def draw_dropdown_menu(self, canvas, dropdown_menu):
        """드롭다운 메뉴 그리기"""
        dropdown_menu.draw(canvas)
    
    def draw_settings_panel(self, canvas, settings_panel, current_tab):
        """설정 패널 그리기"""
        settings_panel.draw(canvas, current_tab)
    
    def draw_image(self, canvas, image):
        """이미지 그리기"""
        if image is None:
            return
        
        x, y, w, h = self.layout.image_area_rect
        
        # 이미지 크기 조정
        img_h, img_w = image.shape[:2]
        scale = min(w / img_w, h / img_h)
        
        if scale < 1.0:
            display_img = cv2.resize(image, None, fx=scale, fy=scale,
                                    interpolation=cv2.INTER_AREA)
        else:
            display_img = image.copy()
        
        # 그레이스케일을 컬러로 변환
        if len(display_img.shape) == 2:
            display_img = cv2.cvtColor(display_img, cv2.COLOR_GRAY2BGR)
        
        # 캔버스에 붙여넣기
        disp_h, disp_w = display_img.shape[:2]
        canvas[y:y + disp_h, x:x + disp_w] = display_img

