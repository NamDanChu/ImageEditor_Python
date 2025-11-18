"""
UI 상수 정의
모든 UI 관련 상수를 한 곳에 모아 관리
"""


class UIConstants:
    """UI 상수 클래스"""
    
    # 색상 정의 (BGR)
    COLOR_BG = (30, 30, 30)
    COLOR_PANEL = (50, 50, 50)
    COLOR_PANEL_DARK = (45, 45, 45)
    COLOR_TEXT = (220, 220, 220)
    COLOR_TEXT_DIM = (150, 150, 150)
    COLOR_HIGHLIGHT = (0, 150, 255)  # 활성 탭 하이라이트 (주황색)
    COLOR_BTN = (80, 80, 80)
    COLOR_BTN_ACTIVE = (0, 200, 0)  # 활성화된 버튼 (녹색)
    COLOR_BTN_HOVER = (100, 100, 100)
    COLOR_RESET_BTN = (180, 50, 40)  # 리셋 버튼 (빨간색)
    COLOR_FILE_SELECTED = (100, 150, 200)  # 선택된 파일 하이라이트 (파란색)
    COLOR_MENU_BG = (55, 55, 55)
    COLOR_BORDER = (150, 150, 150)
    
    # 창 크기
    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 900
    
    # 레이아웃 상수
    FILE_LIST_WIDTH = 250
    TOP_BAR_HEIGHT = 40
    INFO_BAR_HEIGHT = 30
    MENU_HEIGHT = 150
    SETTINGS_PANEL_HEIGHT = 180
    FILE_ITEM_HEIGHT = 25
    TAB_HEIGHT = 30
    
    # 간격
    PADDING = 10
    SPACING = 5
    BORDER_WIDTH = 2
    
    # 폰트
    FONT_SCALE_SMALL = 0.4
    FONT_SCALE_MEDIUM = 0.5
    FONT_SCALE_LARGE = 0.6
    FONT_THICKNESS = 1
    FONT_THICKNESS_BOLD = 2
    
    # 탭 정의 (File을 맨 앞으로)
    TABS = ['File', 'Pixel', 'Area', 'Geometric']
    
    # 메뉴 항목 (File을 맨 앞으로)
    MENU_ITEMS = {
        'File': ['Save', 'Save As', 'Load', 'Undo', 'Redo', 'Settings', 'Exit'],
        'Pixel': ['Brightness', 'Contrast', 'Threshold', 'Grayscale', 'Invert'],
        'Area': ['Blur', 'Canny Edge', 'Sharpen', 'Median Blur'],
        'Geometric': ['Rotation', 'Flip H', 'Flip V', 'Resize', 'Translate']
    }
    
    # 이미지 확장자
    IMAGE_EXTENSIONS = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff', 
                        '*.JPG', '*.JPEG', '*.PNG', '*.BMP', '*.GIF', '*.TIFF']

