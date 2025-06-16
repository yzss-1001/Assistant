import base64
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import joblib


def base64_to_bgr(base64_str):
    # 移除可能的URI前缀（如"data:image/png;base64,"）
    if base64_str.startswith("data:image"):
        base64_str = base64_str.split(",")[1]

    # 1. Base64解码
    img_data = base64.b64decode(base64_str)

    # 2. 字节流转图像对象
    img = Image.open(BytesIO(img_data))

    # 3. 转换为三通道RGB
    if img.mode == 'RGBA':
        img = img.convert('RGB')  # 丢弃Alpha通道
    elif img.mode == 'L':
        img = img.convert('RGB')  # 灰度转RGB
    elif img.mode != 'RGB':
        img = img.convert('RGB')  # 其他格式转RGB

    rgb_array = np.array(img)
    bgr_image = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)

    return bgr_image  # 返回PIL Image对象


def change_to_hist(img):
    img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_CUBIC)  # 三次样条插值
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_normalization = (hist/255).flatten()  # 拉平为一维
    X = [hist_normalization]
    X = np.array(X)
    return X


def crop_to_24x24(bgr_image):
    h, w = bgr_image.shape[:2]

    # 计算中心裁剪的起始坐标
    start_y = max(0, (h - 24) // 2)
    start_x = max(0, (w - 24) // 2)

    # 执行裁剪
    cropped_img = bgr_image[start_y:start_y+24, start_x:start_x+24]

    # 如果图像尺寸小于24x24，填充到目标尺寸
    if cropped_img.shape[0] < 24 or cropped_img.shape[1] < 24:
        pad_y = (24 - cropped_img.shape[0]) // 2
        pad_x = (24 - cropped_img.shape[1]) // 2
        cropped_img = cv2.copyMakeBorder(
            cropped_img,
            pad_y,
            24 - cropped_img.shape[0] - pad_y,
            pad_x,
            24 - cropped_img.shape[1] - pad_x,
            cv2.BORDER_CONSTANT,
            value=[0, 0, 0]
        )

    return cropped_img


def predict_photo(pre_data):
    model_filename = 'D:/python/end_of_term/ChatPhoto/model/svm_identify_photo.pkl'
    loaded_model = joblib.load(model_filename)
    pre_result = loaded_model.predict(pre_data)
    class_name = ['狗', '人']
    return class_name[pre_result[0]]






