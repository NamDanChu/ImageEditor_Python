"""
영역 처리 (Area Processing) 모듈
주변 픽셀을 고려한 필터링 기반 이미지 처리 함수들
"""

import cv2
import numpy as np


def apply_blur(img, value):
    """가우시안 블러 적용
    value: 블러 강도 (0 ~ 20, 홀수만 유효)
    """
    if value <= 0:
        return img
    
    # 홀수로 변환
    kernel_size = value * 2 + 1
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def apply_canny(img, low_threshold, high_threshold):
    """캐니 엣지 검출
    low_threshold: 낮은 임계값
    high_threshold: 높은 임계값
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    edges = cv2.Canny(gray, low_threshold, high_threshold)
    
    # 원본이 컬러였으면 컬러로 변환
    if len(img.shape) == 3:
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return edges


def apply_median_blur(img, kernel_size):
    """미디언 블러 적용
    kernel_size: 커널 크기 (홀수, 3 이상)
    """
    if kernel_size < 3:
        return img
    
    # 홀수로 변환
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    return cv2.medianBlur(img, kernel_size)


def apply_sharpen(img, strength=1.0):
    """샤프닝 적용
    strength: 샤프닝 강도 (0.0 ~ 3.0)
    """
    if strength <= 0:
        return img
    
    # 샤프닝 커널
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]]) * strength
    
    # 커널 정규화
    kernel[1, 1] = 8 * strength + 1
    
    # 필터 적용
    sharpened = cv2.filter2D(img, -1, kernel)
    
    # 범위 제한
    return np.clip(sharpened, 0, 255).astype(np.uint8)


def apply_morphology(img, operation='open', kernel_size=5, iterations=1):
    """모폴로지 연산
    operation: 'erode', 'dilate', 'open', 'close', 'gradient', 'tophat', 'blackhat'
    kernel_size: 커널 크기 (홀수)
    iterations: 반복 횟수
    """
    if kernel_size < 3:
        kernel_size = 3
    
    # 홀수로 변환
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # 구조 요소 생성
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    # 연산 수행
    if operation == 'erode':
        return cv2.erode(img, kernel, iterations=iterations)
    elif operation == 'dilate':
        return cv2.dilate(img, kernel, iterations=iterations)
    elif operation == 'open':
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)
    elif operation == 'close':
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    elif operation == 'gradient':
        return cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel, iterations=iterations)
    elif operation == 'tophat':
        return cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel, iterations=iterations)
    elif operation == 'blackhat':
        return cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel, iterations=iterations)
    else:
        return img

