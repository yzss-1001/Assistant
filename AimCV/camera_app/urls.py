# camera_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('start_camera/', views.start_camera, name='start_camera'),
    path('stop_camera/', views.stop_camera, name='stop_camera'),
    path('take_snapshot/', views.take_snapshot, name='take_snapshot'),
    path('snapshot/<str:snapshot_key>/', views.get_snapshot, name='get_snapshot'),
    path('camera_status/', views.camera_status, name='camera_status'),

    # YOLOv10相关路由
    path('toggle_detection/', views.toggle_detection, name='toggle_detection'),
    path('set_detection/', views.set_detection, name='set_detection'),
    path('detection_status/', views.detection_status, name='detection_status'),

    # 新增的自动保存相关路由
    path('toggle_auto_save/', views.toggle_auto_save, name='toggle_auto_save'),
    path('set_auto_save/', views.set_auto_save, name='set_auto_save'),
    path('set_save_interval/', views.set_save_interval, name='set_save_interval'),
    path('get_detection_info/', views.get_detection_info, name='get_detection_info'),
]