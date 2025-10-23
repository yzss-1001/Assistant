from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import time
import json
from .utlis.camera import camera_manager
from .models import Userinfo

def index(request):
    """主页面"""
    return render(request, 'camera_app/index.html')


def video_feed(request):
    """视频流视图"""

    def generate_frames():
        while True:
            frame = camera_manager.get_frame()
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.03)  # 控制帧率

    return StreamingHttpResponse(
        generate_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


@require_http_methods(["POST"])
@csrf_exempt
def start_camera(request):
    """启动摄像头"""
    try:
        data = json.loads(request.body)
        camera_index = data.get('camera_index', 0)

        if camera_manager.start_camera(camera_index):
            return JsonResponse({'status': 'success', 'message': '摄像头启动成功'})
        else:
            return JsonResponse({'status': 'error', 'message': '无法启动摄像头'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def stop_camera(request):
    """停止摄像头"""
    try:
        camera_manager.stop_camera()
        return JsonResponse({'status': 'success', 'message': '摄像头已停止'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def take_snapshot(request):
    """拍摄快照"""
    try:
        snapshot_key = camera_manager.take_snapshot()
        if snapshot_key:
            return JsonResponse({
                'status': 'success',
                'message': '快照拍摄成功',
                'snapshot_key': snapshot_key
            })
        else:
            return JsonResponse({'status': 'error', 'message': '无法拍摄快照'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def get_snapshot(request, snapshot_key):
    """获取快照图片"""
    frame = camera_manager.get_snapshot(snapshot_key)
    if frame:
        return HttpResponse(frame, content_type='image/jpeg')
    else:
        return HttpResponse('快照不存在或已过期', status=404)


@require_http_methods(["GET"])
def camera_status(request):
    """获取摄像头状态"""
    status = {
        'is_running': camera_manager.is_running,
        'has_frame': camera_manager.get_frame() is not None
    }
    return JsonResponse(status)




@require_http_methods(["POST"])
@csrf_exempt
def toggle_detection(request):
    """切换目标检测功能"""
    try:
        enabled = camera_manager.toggle_detection()
        status = "开启" if enabled else "关闭"
        return JsonResponse({
            'status': 'success',
            'message': f'目标检测已{status}',
            'detection_enabled': enabled
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_http_methods(["POST"])
@csrf_exempt
def set_detection(request):
    """设置目标检测状态"""
    try:
        data = json.loads(request.body)
        enabled = data.get('enabled', False)

        camera_manager.set_detection(enabled)
        status = "开启" if enabled else "关闭"
        return JsonResponse({
            'status': 'success',
            'message': f'目标检测已{status}',
            'detection_enabled': enabled
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_http_methods(["GET"])
def detection_status(request):
    """获取目标检测状态"""
    try:
        status = camera_manager.get_detection_info()
        return JsonResponse({
            'status': 'success',
            'data': status
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# 在 views.py 中添加以下视图函数

@require_http_methods(["POST"])
@csrf_exempt
def toggle_auto_save(request):
    """切换自动保存功能"""
    try:
        enabled = camera_manager.toggle_auto_save()
        status = "开启" if enabled else "关闭"
        return JsonResponse({
            'status': 'success',
            'message': f'自动保存已{status}',
            'auto_save_enabled': enabled
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_http_methods(["POST"])
@csrf_exempt
def set_auto_save(request):
    """设置自动保存状态"""
    try:
        data = json.loads(request.body)
        enabled = data.get('enabled', False)

        camera_manager.set_auto_save(enabled)
        status = "开启" if enabled else "关闭"
        return JsonResponse({
            'status': 'success',
            'message': f'自动保存已{status}',
            'auto_save_enabled': enabled
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_http_methods(["POST"])
@csrf_exempt
def set_save_interval(request):
    """设置保存间隔"""
    try:
        data = json.loads(request.body)
        interval = data.get('interval', 2)

        if interval < 1:
            return JsonResponse({'status': 'error', 'message': '保存间隔不能小于1秒'})

        new_interval = camera_manager.set_save_interval(interval)
        return JsonResponse({
            'status': 'success',
            'message': f'保存间隔已设置为{new_interval}秒',
            'save_interval': new_interval
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_http_methods(["GET"])
def get_detection_info(request):
    """获取检测详细信息"""
    try:
        info = camera_manager.get_detection_info()
        info['saved_images_count'] = camera_manager.get_saved_images_count()
        return JsonResponse({
            'status': 'success',
            'data': info
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})



####以下为登录注册视图####
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user_exists = Userinfo.objects.filter(username=username, password=password).exists()  # 检测数据库中是否有这个用户存在
        if user_exists:
            data = {
                "success": True,
                "message": "登录成功"
            }
            return JsonResponse(data)
        else:
            data = {
                "success": False,
                "message": "登录失败"
            }
            return JsonResponse(data)

    else:
        return render(request, "user_login.html")


def register(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        if gender == 'male':
            gender = '男'
        else:
            gender = '女'
        print(firstName)
        print(lastName)
        print(email)
        print(phone)
        print(password)
        print(gender)
        #  这里向mysql添加用户数据
        userinfo = Userinfo.objects.create(username=lastName + firstName, password=password, email=email,
                                           phone=phone, gender=gender)
        # 验证返回实列是否与添加一致
        if userinfo:
            addSuccess = True
        else:
            addSuccess = False

        if addSuccess:
            data = {
                "success": True,
                "message": "注册成功",
                "redirect_url": "http://localhost:8000/",
                "username": userinfo.username
            }
            return JsonResponse(data)
        else:
            data = {
                "success": False,
                "message": "注册失败"
            }
            return JsonResponse(data)

    else:
        return render(request, "user_register.html")
