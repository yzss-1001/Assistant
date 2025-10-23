import cv2

def capture_camera():
    # 0 表示默认摄像头，如果有多个摄像头可以尝试 1, 2, 等
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("按 'q' 键退出")

    while True:
        # 读取帧
        ret, frame = cap.read()

        if not ret:
            print("无法获取帧")
            break

        # 显示帧
        cv2.imshow('摄像头', frame)

        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_camera()