"""
기하학 처리 (Geometric Processing) 모듈
이미지의 형태나 배치를 기하학적으로 변환하는 함수들
"""

import cv2
import numpy as np


def apply_rotation(img, angle):
    """이미지 회전
    angle: 회전 각도 (0 ~ 360)
    """
    if angle == 0:
        return img
    
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    
    # 회전 행렬 생성
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # 회전된 이미지 크기 계산
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    # 회전 행렬 조정 (중심 이동)
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]
    
    # 이미지 회전
    rotated = cv2.warpAffine(img, rotation_matrix, (new_w, new_h),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_CONSTANT,
                             borderValue=(0, 0, 0))
    
    return rotated


def apply_flip_horizontal(img):
    """좌우 대칭 (수평 뒤집기)"""
    return cv2.flip(img, 1)


def apply_flip_vertical(img):
    """상하 대칭 (수직 뒤집기)"""
    return cv2.flip(img, 0)


def apply_resize(img, width=None, height=None, scale=None, interpolation=cv2.INTER_LINEAR):
    """크기 조절
    width: 목표 너비 (픽셀)
    height: 목표 높이 (픽셀)
    scale: 스케일 팩터 (width, height가 None일 때 사용)
    interpolation: 보간 방법
    """
    h, w = img.shape[:2]
    
    if width is not None and height is not None:
        # 너비와 높이 모두 지정
        new_size = (int(width), int(height))
    elif width is not None:
        # 너비만 지정 (비율 유지)
        aspect_ratio = h / w
        new_size = (int(width), int(width * aspect_ratio))
    elif height is not None:
        # 높이만 지정 (비율 유지)
        aspect_ratio = w / h
        new_size = (int(height * aspect_ratio), int(height))
    elif scale is not None:
        # 스케일 팩터 사용
        new_size = (int(w * scale), int(h * scale))
    else:
        return img
    
    return cv2.resize(img, new_size, interpolation=interpolation)


def apply_translate(img, tx, ty):
    """이미지 이동
    tx: x축 이동량 (픽셀, 양수: 오른쪽, 음수: 왼쪽)
    ty: y축 이동량 (픽셀, 양수: 아래, 음수: 위)
    """
    if tx == 0 and ty == 0:
        return img
    
    h, w = img.shape[:2]
    
    # 이동 행렬 생성
    M = np.float32([[1, 0, tx],
                    [0, 1, ty]])
    
    # 이동 적용
    translated = cv2.warpAffine(img, M, (w, h),
                                flags=cv2.INTER_LINEAR,
                                borderMode=cv2.BORDER_CONSTANT,
                                borderValue=(0, 0, 0))
    
    return translated


def apply_crop(img, x, y, width, height):
    """이미지 자르기
    x, y: 시작 좌표 (픽셀)
    width: 자를 너비 (픽셀)
    height: 자를 높이 (픽셀)
    """
    h, w = img.shape[:2]
    
    # 범위 검증
    x = max(0, min(x, w - 1))
    y = max(0, min(y, h - 1))
    width = max(1, min(width, w - x))
    height = max(1, min(height, h - y))
    
    return img[y:y+height, x:x+width].copy()


def apply_affine_transform(img, src_points, dst_points):
    """어파인 변환
    src_points: 원본 이미지의 3개 점 좌표 (numpy array, shape: (3, 2))
    dst_points: 변환 후 이미지의 3개 점 좌표 (numpy array, shape: (3, 2))
    """
    if src_points.shape != (3, 2) or dst_points.shape != (3, 2):
        raise ValueError("src_points and dst_points must be (3, 2) arrays")
    
    # 어파인 변환 행렬 계산
    M = cv2.getAffineTransform(src_points.astype(np.float32),
                                dst_points.astype(np.float32))
    
    h, w = img.shape[:2]
    
    # 변환 적용
    transformed = cv2.warpAffine(img, M, (w, h),
                                 flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_CONSTANT,
                                 borderValue=(0, 0, 0))
    
    return transformed

