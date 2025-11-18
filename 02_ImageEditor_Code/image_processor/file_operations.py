"""
파일 작업 모듈
SOLID 원칙에 따라 파일 관련 작업을 모듈화
"""

import cv2
import os
import numpy as np
from typing import Optional, Tuple


class FileManager:
    """파일 관리자 클래스 (단일 책임: 파일 저장/로드 관리)"""
    
    def __init__(self):
        self.current_file_path: Optional[str] = None
        self.history: list = []  # 되돌리기/앞으로 돌리기를 위한 히스토리
        self.history_index: int = -1
        self.max_history_size: int = 50
    
    def set_current_file(self, file_path: str):
        """현재 파일 경로 설정"""
        self.current_file_path = file_path
    
    def get_current_file(self) -> Optional[str]:
        """현재 파일 경로 반환"""
        return self.current_file_path
    
    def add_to_history(self, image):
        """히스토리에 이미지 추가"""
        # 현재 인덱스 이후의 히스토리 제거 (새로운 작업 시)
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # 히스토리에 추가
        self.history.append(image.copy())
        self.history_index += 1
        
        # 히스토리 크기 제한
        if len(self.history) > self.max_history_size:
            self.history.pop(0)
            self.history_index -= 1
    
    def can_undo(self) -> bool:
        """되돌리기 가능 여부"""
        return self.history_index > 0
    
    def can_redo(self) -> bool:
        """앞으로 돌리기 가능 여부"""
        return self.history_index < len(self.history) - 1
    
    def get_undo_image(self):
        """되돌리기 이미지 반환"""
        if self.can_undo():
            self.history_index -= 1
            return self.history[self.history_index].copy()
        return None
    
    def get_redo_image(self):
        """앞으로 돌리기 이미지 반환"""
        if self.can_redo():
            self.history_index += 1
            return self.history[self.history_index].copy()
        return None


class FileSaver:
    """파일 저장 클래스 (단일 책임: 파일 저장)"""
    
    @staticmethod
    def save(image, file_path: str) -> bool:
        """이미지 저장
        
        Args:
            image: 저장할 이미지 (numpy array)
            file_path: 저장 경로
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            # 디렉토리가 없으면 생성
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # 이미지 저장
            success = cv2.imwrite(file_path, image)
            return success
        except Exception as e:
            print(f"파일 저장 오류: {e}")
            return False
    
    @staticmethod
    def save_as(image, default_path: str = None) -> Optional[str]:
        """다른 이름으로 저장
        
        Args:
            image: 저장할 이미지
            default_path: 기본 경로 (선택)
            
        Returns:
            Optional[str]: 저장된 파일 경로, 취소 시 None
        """
        from PyQt5.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "다른 이름으로 저장",
            default_path or "",
            "Image Files (*.jpg *.jpeg *.png *.bmp *.tiff);;All Files (*)"
        )
        
        if file_path:
            if FileSaver.save(image, file_path):
                return file_path
        return None


class FileLoader:
    """파일 로드 클래스 (단일 책임: 파일 로드)"""
    
    @staticmethod
    def load(file_path: str):
        """이미지 파일 로드
        
        Args:
            file_path: 로드할 파일 경로
            
        Returns:
            Optional[numpy.ndarray]: 로드된 이미지, 실패 시 None
        """
        try:
            image = cv2.imread(file_path)
            if image is None:
                print(f"이미지 로드 실패: {file_path}")
            return image
        except Exception as e:
            print(f"파일 로드 오류: {e}")
            return None
    
    @staticmethod
    def load_from_dialog(default_path: str = None) -> Tuple[Optional[str], Optional[np.ndarray]]:
        """파일 다이얼로그를 통한 이미지 로드
        
        Args:
            default_path: 기본 경로 (선택)
            
        Returns:
            Tuple[Optional[str], Optional[np.ndarray]]: (파일 경로, 이미지)
        """
        from PyQt5.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "이미지 불러오기",
            default_path or "",
            "Image Files (*.jpg *.jpeg *.png *.bmp *.tiff);;All Files (*)"
        )
        
        if file_path:
            image = FileLoader.load(file_path)
            return file_path, image
        
        return None, None


class HistoryManager:
    """히스토리 관리 클래스 (단일 책임: 되돌리기/앞으로 돌리기 관리)"""
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
    
    def undo(self):
        """되돌리기"""
        return self.file_manager.get_undo_image()
    
    def redo(self):
        """앞으로 돌리기"""
        return self.file_manager.get_redo_image()
    
    def can_undo(self) -> bool:
        """되돌리기 가능 여부"""
        return self.file_manager.can_undo()
    
    def can_redo(self) -> bool:
        """앞으로 돌리기 가능 여부"""
        return self.file_manager.can_redo()


class SettingsManager:
    """설정 관리 클래스 (단일 책임: 애플리케이션 설정 관리)"""
    
    def __init__(self):
        self.settings = {}
    
    def get_setting(self, key: str, default=None):
        """설정 값 가져오기"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value):
        """설정 값 설정"""
        self.settings[key] = value
    
    def show_settings_dialog(self):
        """설정 다이얼로그 표시"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(None, "설정", "설정 기능은 추후 구현 예정입니다.")


class ApplicationManager:
    """애플리케이션 관리 클래스 (단일 책임: 애플리케이션 종료 관리)"""
    
    @staticmethod
    def exit_application():
        """애플리케이션 종료"""
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()

