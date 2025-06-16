from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# 主页路由 - 返回HTML页面
@app.route('/')
def login_and_register():  # 返回登录注册页面
    return render_template('test/login_register_test.html')


@app.route('/home')
def home():  # 返回主页面
    return render_template('test/index_test.html')


@app.route('/login', methods=['POST'])
def login():  # 登录信息后台处理
    data = request.get_json()
    username = data.get('username', 'Guest')
    password = data.get('password', 'Guest')
    print(f"登录：{username}")
    print(f"登录：{password}")
    with open('txt/user/user_information.txt', 'r+') as file:  # 检查登录信息在user_information中是否存在
        existing_content = file.read()
        sub_body = existing_content.split(';;')  # 多个用户信息
        login_user_body = f"\nusername:{username}\npassword:{password}"  # 构建登录信息体
        for i in sub_body:  # 遍历每一个信息体
            if login_user_body in i:  # 判断该登录信息体是否在user_information中存在
                sub02_body = i.split('\n')
                email = sub02_body[4][6:]  # 拆解取出对应email邮箱信息
                return jsonify({'success': True, 'message': '登录成功！', 'user': username,
                                'email': email, 'password': password})
        return jsonify({'success': False, 'message': '登录失败！'})


@app.route('/register', methods=['POST'])
def register():  # 注册信息后台处理
    data = request.get_json()
    username = data.get('username', 'Guest')
    password = data.get('password', 'Guest')
    email = data.get('email', 'Guest')
    print(f"注册：{username}")
    print(f"注册：{password}")
    print(f"注册：{email}")
    with open('txt/user/user_information.txt', 'r+') as file:  # 将注册信息存入user_information中，同时避免用户名信息重复。
        existing_content = file.read()
        existing_count = existing_content.count(';;')
        if f"username:{username}\n" not in existing_content:
            file.writelines(f"\nid:{existing_count + 1}\nusername:{username}\npassword:{password}\nemail:{email};;")
            return jsonify({'success': True, 'message': '注册成功！', 'user': username})
        else:
            return jsonify({'success': False, 'message': '用户名已存在请换一个名字！'})


# API路由 - 处理POST请求
@app.route('/userInput', methods=['POST'])
def get_userinput():  # 后台收集用户提问的内容
    # 获取前端发送的JSON数据
    data = request.get_json()
    userInput = data.get('name', 'Guest')
    # 处理数据并返回JSON响应
    print(f"用户提问内容：{userInput}")
    #  保存用户的提问
    if userInput != 'null':
        with open('txt/feedback/userInput.txt', 'r+', encoding='gbk') as file:
            existing_content = file.read()
            if userInput not in existing_content:   # 防止重复写入
                file.writelines(f"{userInput};;\n")
    else:
        print("已经过滤为空的提问")
    return jsonify({'message': userInput})


@app.route('/dislike_reply', methods=['POST'])
def get_dislike_reply():  # 后台收集用户不喜欢的回复内容
    data = request.get_json()
    dislike_data_list = data.get('name', 'Guest')
    dislike_data = dislike_data_list[-1]['content']
    print(f"被踩的回复内容：{dislike_data}")
    if dislike_data != 'null':
        with open('txt/feedback/dislike_reply.txt', 'r+', encoding='gbk') as file:
            existing_content = file.read()
            if dislike_data not in existing_content:  # 防止重复写入
                file.writelines(f"{dislike_data};;\n\n")
    else:
        print("已经过滤为空的点踩回复")
    return jsonify({'message': dislike_data})


@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    name = data.get('name', 'Guest')
    old_password = data.get('oldPassword', 'Guest')
    new_password = data.get('newPassword', 'Guest')
    print(f"修改密码：{name}（用户名）")
    print(f"修改密码：{new_password}（新密码）")
    old_user_body = f"\nusername:{name}\npassword:{old_password}"
    new_user_body = f"\nusername:{name}\npassword:{new_password}"
    # 读取文件内容
    with open('txt/user/user_information.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    # 执行替换
    new_content = content.replace(old_user_body, new_user_body)
    # 写回文件
    with open('txt/user/user_information.txt', 'w', encoding='utf-8') as file:
        file.writelines(new_content)
    return jsonify({'success': True, 'name': name})


@app.route('/delete_account', methods=['POST'])
def delete_account():
    data = request.get_json()
    name = data.get('name', 'Guest')
    print(f"注销账户：{name}（名称）")
    with open('txt/user/user_information.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    sub_body = content.split(';;')
    deleted_sub_body = []
    for i in sub_body:
        if 'username:test\n' not in i:
            deleted_sub_body.append(i)

    new_content = ";;".join(deleted_sub_body)

    with open('txt/user/user_information.txt', 'w', encoding='utf-8') as file:
        file.write(new_content)

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
