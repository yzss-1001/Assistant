with open('txt/user/user_information.txt', 'r', encoding='utf-8') as file:
    content = file.read()
sub_body = content.split(';;')
deleted_sub_body = []
for i in sub_body:
    if 'username:test\n' not in i:
        deleted_sub_body.append(i)

new_content = ";;".join(deleted_sub_body)
print(new_content)
with open('txt/user/user_information_test.txt', 'w', encoding='utf-8') as file:
    file.write(new_content)