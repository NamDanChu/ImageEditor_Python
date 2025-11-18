"""
UI 컴포넌트 클래스들
각 UI 요소를 독립적인 클래스로 구현 (Single Responsibility)
"""

import cv2
import numpy as np
from .constants import UIConstants


class Button:
    """버튼 컴포넌트"""
    
    def __init__(self, x, y, width, height, text, color=None, active_color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color or UIConstants.COLOR_BTN
        self.active_color = active_color or UIConstants.COLOR_BTN_ACTIVE
        self.is_active = False
    
    def contains(self, x, y):
        """포인트가 버튼 영역 내에 있는지 확인"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def draw(self, canvas):
        """버튼 그리기"""
        color = self.active_color if self.is_active else self.color
        cv2.rectangle(canvas, (self.x, self.y), 
                     (self.x + self.width, self.y + self.height), 
                     color, -1)
        cv2.rectangle(canvas, (self.x, self.y), 
                     (self.x + self.width, self.y + self.height), 
                     UIConstants.COLOR_BORDER, 1)
        
        # 텍스트 중앙 정렬
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, 
                                   UIConstants.FONT_SCALE_MEDIUM, 
                                   UIConstants.FONT_THICKNESS)[0]
        text_x = self.x + (self.width - text_size[0]) // 2
        text_y = self.y + (self.height + text_size[1]) // 2
        
        cv2.putText(canvas, self.text, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_MEDIUM,
                   UIConstants.COLOR_TEXT, UIConstants.FONT_THICKNESS)


class Tab:
    """탭 컴포넌트"""
    
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.is_active = False
    
    def contains(self, x, y):
        """포인트가 탭 영역 내에 있는지 확인"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def draw(self, canvas):
        """탭 그리기"""
        # 텍스트 그리기
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX,
                                   UIConstants.FONT_SCALE_LARGE,
                                   UIConstants.FONT_THICKNESS_BOLD)[0]
        text_x = self.x + (self.width - text_size[0]) // 2
        text_y = self.y + (self.height + text_size[1]) // 2
        
        cv2.putText(canvas, self.text, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_LARGE,
                   UIConstants.COLOR_TEXT, UIConstants.FONT_THICKNESS_BOLD)
        
        # 활성 탭 하이라이트
        if self.is_active:
            cv2.line(canvas, (self.x, self.y + self.height),
                    (self.x + self.width, self.y + self.height),
                    UIConstants.COLOR_HIGHLIGHT, 3)


class FileList:
    """파일 리스트 컴포넌트"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.files = []
        self.selected_index = -1
    
    def set_files(self, files):
        """파일 리스트 설정"""
        self.files = files
    
    def get_clicked_index(self, x, y):
        """클릭된 파일 인덱스 반환"""
        if not self.contains(x, y):
            return -1
        
        list_y_start = self.y + 35
        clicked_index = int((y - list_y_start) / UIConstants.FILE_ITEM_HEIGHT)
        if 0 <= clicked_index < len(self.files):
            return clicked_index
        return -1
    
    def contains(self, x, y):
        """포인트가 파일 리스트 영역 내에 있는지 확인"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def draw(self, canvas):
        """파일 리스트 그리기"""
        # 패널 배경
        cv2.rectangle(canvas, (self.x, self.y),
                     (self.x + self.width, self.y + self.height),
                     UIConstants.COLOR_PANEL, -1)
        
        # 제목
        cv2.putText(canvas, 'Image Files', (self.x + UIConstants.PADDING, self.y + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_LARGE,
                   UIConstants.COLOR_TEXT, UIConstants.FONT_THICKNESS)
        
        # 구분선
        cv2.line(canvas, (self.x, self.y + 30),
                (self.x + self.width, self.y + 30),
                UIConstants.COLOR_BORDER, 1)
        
        # 파일 리스트
        list_y_start = self.y + 35
        max_visible = (self.height - 35) // UIConstants.FILE_ITEM_HEIGHT
        
        # 중복 방지: 파일 리스트를 한 번만 그리기
        files_to_display = self.files[:max_visible] if len(self.files) > max_visible else self.files
        
        for i, file_name in enumerate(files_to_display):
            file_y = list_y_start + i * UIConstants.FILE_ITEM_HEIGHT
            
            # 선택된 파일 하이라이트
            if i == self.selected_index:
                cv2.rectangle(canvas, (self.x + UIConstants.SPACING, file_y - 20),
                            (self.x + self.width - UIConstants.SPACING, file_y + 5),
                            UIConstants.COLOR_FILE_SELECTED, -1)
            
            # 파일명 표시 (긴 파일명은 잘라내기)
            display_name = file_name
            if len(display_name) > 25:
                display_name = display_name[:22] + '...'
            
            cv2.putText(canvas, display_name,
                       (self.x + UIConstants.PADDING, file_y),
                       cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_SMALL,
                       UIConstants.COLOR_TEXT, UIConstants.FONT_THICKNESS)
        
        # 파일이 없을 때 메시지
        if len(self.files) == 0:
            msg_y = list_y_start + 20
            cv2.putText(canvas, 'No image files', 
                       (self.x + UIConstants.PADDING, msg_y),
                       cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_MEDIUM,
                       UIConstants.COLOR_TEXT_DIM, UIConstants.FONT_THICKNESS)
            cv2.putText(canvas, 'found in current', 
                       (self.x + UIConstants.PADDING, msg_y + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_MEDIUM,
                       UIConstants.COLOR_TEXT_DIM, UIConstants.FONT_THICKNESS)
            cv2.putText(canvas, 'directory', 
                       (self.x + UIConstants.PADDING, msg_y + 50),
                       cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_MEDIUM,
                       UIConstants.COLOR_TEXT_DIM, UIConstants.FONT_THICKNESS)


class DropdownMenu:
    """드롭다운 메뉴 컴포넌트"""
    
    def __init__(self, x, y, items):
        self.x = x
        self.y = y
        self.items = items
        self.is_visible = False
    
    def draw(self, canvas):
        """드롭다운 메뉴 그리기 (최상위 레이어)"""
        if not self.is_visible or not self.items:
            return
        
        menu_height = len(self.items) * 25 + 10
        menu_width = 300
        
        # 메뉴 배경 (반투명 효과를 위해 약간 밝게)
        cv2.rectangle(canvas, (self.x, self.y),
                     (self.x + menu_width, self.y + menu_height),
                     UIConstants.COLOR_MENU_BG, -1)
        cv2.rectangle(canvas, (self.x, self.y),
                     (self.x + menu_width, self.y + menu_height),
                     UIConstants.COLOR_HIGHLIGHT, 2)
        
        # 메뉴 항목
        y_offset = self.y + 20
        for item in self.items:
            cv2.putText(canvas, f"  {item}", (self.x + UIConstants.PADDING, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_SMALL,
                       UIConstants.COLOR_TEXT, UIConstants.FONT_THICKNESS)
            y_offset += 25


class SettingsPanel:
    """설정 패널 컴포넌트"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttons = {}
        self.trackbar_labels = {}
    
    def add_button(self, key, button):
        """버튼 추가"""
        self.buttons[key] = button
    
    def add_trackbar_label(self, key, x, y, text_getter):
        """트랙바 라벨 추가"""
        self.trackbar_labels[key] = {
            'x': x,
            'y': y,
            'text_getter': text_getter
        }
    
    def draw(self, canvas, current_tab):
        """설정 패널 그리기 (현재 탭에 맞게)"""
        # 패널 배경
        cv2.rectangle(canvas, (self.x, self.y),
                     (self.x + self.width, self.y + self.height),
                     UIConstants.COLOR_PANEL, -1)
        
        # 제목
        cv2.putText(canvas, 'Detailed Settings',
                   (self.x + UIConstants.PADDING, self.y + 15),
                   cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_LARGE,
                   UIConstants.COLOR_TEXT, UIConstants.FONT_THICKNESS)
        
        # 현재 탭에 맞는 버튼만 그리기
        if current_tab == 'Pixel':
            # Pixel 탭 버튼
            if 'grayscale' in self.buttons:
                self.buttons['grayscale'].draw(canvas)
            if 'invert' in self.buttons:
                self.buttons['invert'].draw(canvas)
            # Pixel 탭 트랙바 라벨
            for key in ['brightness', 'contrast', 'threshold']:
                if key in self.trackbar_labels:
                    label_info = self.trackbar_labels[key]
                    text = label_info['text_getter']()
                    cv2.putText(canvas, text,
                               (label_info['x'], label_info['y']),
                               cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_MEDIUM,
                               UIConstants.COLOR_TEXT, UIConstants.FONT_THICKNESS)
        
        elif current_tab == 'Area':
            # Area 탭 트랙바 라벨만
            for key in ['blur', 'canny_low', 'canny_high', 'sharpen']:
                if key in self.trackbar_labels:
                    label_info = self.trackbar_labels[key]
                    text = label_info['text_getter']()
                    cv2.putText(canvas, text,
                               (label_info['x'], label_info['y']),
                               cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_MEDIUM,
                               UIConstants.COLOR_TEXT, UIConstants.FONT_THICKNESS)
        
        elif current_tab == 'Geometric':
            # Geometric 탭 버튼
            if 'flip_h' in self.buttons:
                self.buttons['flip_h'].draw(canvas)
            if 'flip_v' in self.buttons:
                self.buttons['flip_v'].draw(canvas)
            # Geometric 탭 트랙바 라벨
            for key in ['rotation', 'resize_w', 'resize_h']:
                if key in self.trackbar_labels:
                    label_info = self.trackbar_labels[key]
                    text = label_info['text_getter']()
                    cv2.putText(canvas, text,
                               (label_info['x'], label_info['y']),
                               cv2.FONT_HERSHEY_SIMPLEX, UIConstants.FONT_SCALE_MEDIUM,
                               UIConstants.COLOR_TEXT, UIConstants.FONT_THICKNESS)
        
        # RESET 버튼은 항상 표시
        if 'reset' in self.buttons:
            self.buttons['reset'].draw(canvas)

