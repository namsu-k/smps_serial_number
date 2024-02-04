import cv2
import os
import numpy as np


def qr_scan(image_path, box_start_number):
    result = ""

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    _, otsu = cv2.threshold(binary_image, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    qr_detector = cv2.QRCodeDetector()
    data, pts, qr_code = qr_detector.detectAndDecode(otsu)

    if data:
        serial_range = str(data).split()[1]

        result = f"{box_start_number}. {serial_range}"
    else:
        result = f"{box_start_number}. 인식 불가"

    box_start_number += 1

    return result
