"""
화소 처리 (Pixel Processing) 모듈
픽셀 단위의 연산을 통한 이미지 처리 함수들
"""

import cv2
import numpy as np


def to_grayscale(image):
    """
    컬러 이미지를 그레이스케일 이미지로 변환합니다.
    """
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def apply_grayscale(img):
    """그레이스케일 변환 (별칭)"""
    return to_grayscale(img)


def apply_brightness(img, value):
    """밝기 조절
    value: -100 ~ 100 범위 (0이 원본)
    """
    # -100 ~ 100을 0 ~ 200으로 변환
    adjusted = np.clip(img.astype(np.int16) + (value - 100), 0, 255)
    return adjusted.astype(np.uint8)


def apply_contrast(img, value):
    """명암 조절
    value: 0 ~ 200 범위 (100이 원본)
    """
    factor = value / 100.0
    adjusted = np.clip(img.astype(np.float32) * factor, 0, 255)
    return adjusted.astype(np.uint8)


def apply_invert(img):
    """이미지 반전 (색상 반전)"""
    return cv2.bitwise_not(img)


def apply_threshold(img, value):
    """이진화 처리
    value: 임계값 (0 ~ 255)
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    _, binary = cv2.threshold(gray, value, 255, cv2.THRESH_BINARY)
    
    # 원본이 컬러였으면 컬러로 변환
    if len(img.shape) == 3:
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    return binary


def apply_gamma(img, gamma):
    """감마 보정
    gamma: 감마 값 (0.1 ~ 3.0, 1.0이 원본)
    """
    if gamma == 1.0:
        return img
    
    # 감마 보정을 위한 LUT 생성
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    
    # LUT 적용
    return cv2.LUT(img, table)


def apply_histogram_equalization(img):
    """히스토그램 평활화
    명암 대비를 극대화하여 이미지를 선명하게 만듭니다.
    """
    if len(img.shape) == 3:
        # 컬러 이미지: YUV로 변환 후 Y 채널만 평활화
        yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
        return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    else:
        # 그레이스케일 이미지
        return cv2.equalizeHist(img)

