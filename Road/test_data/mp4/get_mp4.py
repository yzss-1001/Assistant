import requests
import re
img_save_path = 'D:\\python\\end_of_term\\Road\\test_data\\mp4\\video_01.mp4'
response = requests.get('https://vdept3.bdstatic.com/mda-nkkmagje4pgss0xg/cae_h264/1669284196692735827/mda-nkkmagje4pgss0xg.mp4?v_from_s=hkapp-haokan-hbf&auth_key=1748353797-0-0-74a6f8e3e1f4f3f0ba4dfaff939d7ec4&bcevod_channel=searchbox_feed&cr=0&cd=0&pd=1&pt=3&logid=2997346185&vid=16752726211656942488&klogid=2997346185&abtest=')
content = response.content
print(content)
with open(img_save_path,'wb')as file:
    file.write(content)

