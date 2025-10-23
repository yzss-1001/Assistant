import cv2
import threading
import time
import numpy as np
import os
from django.core.cache import cache
from ultralytics import YOLO
import torch
from datetime import datetime

class CameraManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(CameraManager, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.camera = None
        self.is_running = False
        self.last_frame = None
        self.frame_lock = threading.Lock()
        self.thread = None

        # YOLOv10模型相关
        self.yolo_model = None
        self.detection_enabled = False
        self.model_lock = threading.Lock()

        # 目标检测保存相关
        self.auto_save_enabled = False
        self.last_save_time = 0
        self.save_interval = 2  # 保存间隔（秒）
        self.save_directory = "detected_objects"
        self.detection_count = 0

        # 创建保存目录
        self._create_save_directory()

        # 初始化YOLOv10模型
        self._load_yolo_model()

    def _create_save_directory(self):
        """创建保存检测目标的目录"""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            print(f"创建保存目录: {self.save_directory}")

    def _load_yolo_model(self):
        """加载YOLOv10模型"""
        try:
            # 使用预训练的YOLOv10模型
            self.yolo_model = YOLO('weight/yolov10n.pt')
            print("YOLOv10模型加载成功")
        except Exception as e:
            print(f"YOLOv10模型加载失败: {e}")
            self.yolo_model = None

    def start_camera(self, camera_index=0):
        """启动摄像头"""
        if self.is_running:
            return True

        try:
            self.camera = cv2.VideoCapture(camera_index)
            if not self.camera.isOpened():
                return False

            self.is_running = True
            self.thread = threading.Thread(target=self._update_frame, daemon=True)
            self.thread.start()
            return True
        except Exception as e:
            print(f"启动摄像头失败: {e}")
            return False

    def _update_frame(self):
        """更新帧的线程函数"""
        while self.is_running:
            try:
                if self.camera and self.camera.isOpened():
                    ret, frame = self.camera.read()
                    if ret:
                        # 调整帧大小以提高性能
                        frame = cv2.resize(frame, (640, 480))

                        # 如果检测功能开启且模型已加载，进行目标检测
                        if self.detection_enabled and self.yolo_model is not None:
                            frame, has_objects = self._detect_objects(frame)

                            # 如果检测到目标且自动保存开启，保存画面
                            if has_objects and self.auto_save_enabled:
                                self._save_detected_frame(frame)
                        else:
                            has_objects = False

                        # 编码为 JPEG
                        ret, jpeg = cv2.imencode('.jpg', frame,
                                                 [cv2.IMWRITE_JPEG_QUALITY, 80])
                        if ret:
                            with self.frame_lock:
                                self.last_frame = jpeg.tobytes()
                time.sleep(0.03)  # 约 30 FPS
            except Exception as e:
                print(f"更新帧失败: {e}")
                time.sleep(1)

    def _detect_objects(self, frame):
        """使用YOLOv10进行目标检测"""
        try:
            # 使用YOLOv10进行推理
            results = self.yolo_model(frame, verbose=False)

            # 检查是否检测到目标
            has_objects = len(results[0].boxes) > 0 if results[0].boxes is not None else False

            # 在帧上绘制检测结果
            annotated_frame = results[0].plot()

            return annotated_frame, has_objects

        except Exception as e:
            print(f"目标检测失败: {e}")
            return frame, False

    def _save_detected_frame(self, frame):
        """保存检测到目标的画面"""
        current_time = time.time()

        # 检查是否达到保存间隔
        if current_time - self.last_save_time >= self.save_interval:
            try:
                # 生成文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"detected_{timestamp}_{self.detection_count:04d}.jpg"
                filepath = os.path.join(self.save_directory, filename)

                # 保存图片
                cv2.imwrite(filepath, frame)
                self.detection_count += 1
                self.last_save_time = current_time

                print(f"检测到目标，已保存: {filepath}")

            except Exception as e:
                print(f"保存检测画面失败: {e}")

    def get_frame(self):
        """获取当前帧"""
        with self.frame_lock:
            if self.last_frame is None:
                return None
            return self.last_frame

    def stop_camera(self):
        """停止摄像头"""
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        if self.camera:
            self.camera.release()
        self.camera = None
        self.last_frame = None

    def take_snapshot(self):
        """拍摄快照"""
        frame = self.get_frame()
        if frame:
            # 保存到缓存，10分钟过期
            snapshot_key = f"snapshot_{int(time.time())}"
            cache.set(snapshot_key, frame, 600)
            return snapshot_key
        return None

    def get_snapshot(self, key):
        """获取快照"""
        return cache.get(key)

    def toggle_detection(self):
        """切换目标检测功能"""
        with self.model_lock:
            self.detection_enabled = not self.detection_enabled
        return self.detection_enabled

    def set_detection(self, enabled):
        """设置目标检测状态"""
        with self.model_lock:
            self.detection_enabled = enabled
        return self.detection_enabled

    def toggle_auto_save(self):
        """切换自动保存功能"""
        self.auto_save_enabled = not self.auto_save_enabled
        status = "开启" if self.auto_save_enabled else "关闭"
        print(f"自动保存功能已{status}")
        return self.auto_save_enabled

    def set_auto_save(self, enabled):
        """设置自动保存状态"""
        self.auto_save_enabled = enabled
        status = "开启" if enabled else "关闭"
        print(f"自动保存功能已{status}")
        return self.auto_save_enabled

    def set_save_interval(self, interval):
        """设置保存间隔（秒）"""
        self.save_interval = max(1, interval)  # 最小间隔1秒
        return self.save_interval

    def get_detection_status(self):
        """获取检测状态"""
        return self.detection_enabled

    def get_auto_save_status(self):
        """获取自动保存状态"""
        return self.auto_save_enabled

    def get_detection_info(self):
        """获取检测相关信息"""
        return {
            'detection_enabled': self.detection_enabled,
            'auto_save_enabled': self.auto_save_enabled,
            'save_interval': self.save_interval,
            'detection_count': self.detection_count,
            'model_loaded': self.yolo_model is not None
        }

    def get_saved_images_count(self):
        """获取已保存图片数量"""
        try:
            if os.path.exists(self.save_directory):
                images = [f for f in os.listdir(self.save_directory) if f.endswith(('.jpg', '.jpeg', '.png'))]
                return len(images)
            return 0
        except Exception as e:
            print(f"获取保存图片数量失败: {e}")
            return 0


# 全局摄像头管理器实例
camera_manager = CameraManager()