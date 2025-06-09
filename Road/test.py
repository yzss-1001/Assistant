with open('txt/user/user_information', 'r+') as file:  # 检查登录信息在user_information中是否存在
    existing_content = file.read()
    sub_body = existing_content.split(';;')  # 多个用户信息
    login_user_body = f"\nusername:test_01\npassword:test"
    for i in sub_body:
        if login_user_body in i:
            sub02_body = i.split('\n')
            email = sub02_body[4][6:]
            print(email)