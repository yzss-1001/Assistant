import requests
print(f"请输入爬取图片内容：")
content = input()
cookies = {
    'BDIMGISLOGIN': '0',
    'winWH': '%5E6_601x799',
    'BAIDUID': '0A89A07C97C731F9DF4A64F21E775B87:FG=1',
    'BAIDUID_BFESS': '0A89A07C97C731F9DF4A64F21E775B87:FG=1',
    'Hm_lvt_246a5e7d3670cfba258184e42d902b31': '1728289959',
    'BIDUPSID': '0A89A07C97C731F9DF4A64F21E775B87',
    'PSTM': '1728889997',
    'ZFY': 'Ab:AiGgou7:AzATj5GTf9o4Gg5se2KjPXYQgK1BjitXDM:C',
    '__bid_n': '19298ef705c9216b2bad9f',
    'BDUSS': 'UxkSkw1cDdDbn5SUVg4dDJKcHhQei1KcWdEWUQ4Njh5YjB2ellodGE2aGw2bXRuRVFBQUFBJCQAAAAAAQAAAAEAAADxYZ0UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGVdRGdlXURnS',
    'BDUSS_BFESS': 'UxkSkw1cDdDbn5SUVg4dDJKcHhQei1KcWdEWUQ4Njh5YjB2ellodGE2aGw2bXRuRVFBQUFBJCQAAAAAAQAAAAEAAADxYZ0UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGVdRGdlXURnS',
    'H_PS_PSSID': '62325_62967_63144_63194_63210_63241_63254_63277_63325_63357_63385_63377_63186_63390_63404',
    'RT': '"z=1&dm=baidu.com&si=f142398a-fc55-4758-a24a-bce399b86858&ss=mbxtsml3&sl=1&tt=1y1&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=2r3"',
    'H_WISE_SIDS': '62325_63241_63357_63440_63509_63563_63584_63579_63619',
    'arialoadData': 'false',
    'BDRCVFR[tox4WRQ4-Km]': 'mk3SLVN4HKm',
    'userFrom': 'null',
    'BDRCVFR[-pGxjrCMryR]': 'mk3SLVN4HKm',
    'ab_sr': '1.0.1_NDcyNWQ5M2U1MDc0NDFmMWNiZGFmOTJiNmJmZGJkM2Q2N2FkM2E2ODhjNDcyNTQ0N2FkZjM5OGVkYTU0NjFkYTg3YmVjYzNhOWE0YWJkMmU1ZjBkZDhjN2Q1MzdjMGE3ZTI0ZTIxN2NjZjU3Mjc5N2IxMGMyNjZiNDNkZTc3NmIzMDgxZjBkNzg3MDc0NDJlYjFhYzg4NTY0OGMxZjA1YTdhZTQwYjdlOTQ2YWU0MjcwNTUxYTZiNTM4NzU4NTcxOTA2ZDJmNDlmNDMwNGU5OWM0OTMwMTY0ZTZhOWRhYmQ=',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=&st=-1&fm=index&fr=&hs=0&xthttps=111110&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%8D%95%E4%B8%AA%E4%BA%BA%E5%85%A8%E8%BA%AB',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'BDIMGISLOGIN=0; winWH=%5E6_601x799; BAIDUID=0A89A07C97C731F9DF4A64F21E775B87:FG=1; BAIDUID_BFESS=0A89A07C97C731F9DF4A64F21E775B87:FG=1; Hm_lvt_246a5e7d3670cfba258184e42d902b31=1728289959; BIDUPSID=0A89A07C97C731F9DF4A64F21E775B87; PSTM=1728889997; ZFY=Ab:AiGgou7:AzATj5GTf9o4Gg5se2KjPXYQgK1BjitXDM:C; __bid_n=19298ef705c9216b2bad9f; BDUSS=UxkSkw1cDdDbn5SUVg4dDJKcHhQei1KcWdEWUQ4Njh5YjB2ellodGE2aGw2bXRuRVFBQUFBJCQAAAAAAQAAAAEAAADxYZ0UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGVdRGdlXURnS; BDUSS_BFESS=UxkSkw1cDdDbn5SUVg4dDJKcHhQei1KcWdEWUQ4Njh5YjB2ellodGE2aGw2bXRuRVFBQUFBJCQAAAAAAQAAAAEAAADxYZ0UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGVdRGdlXURnS; H_PS_PSSID=62325_62967_63144_63194_63210_63241_63254_63277_63325_63357_63385_63377_63186_63390_63404; RT="z=1&dm=baidu.com&si=f142398a-fc55-4758-a24a-bce399b86858&ss=mbxtsml3&sl=1&tt=1y1&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=2r3"; H_WISE_SIDS=62325_63241_63357_63440_63509_63563_63584_63579_63619; arialoadData=false; BDRCVFR[tox4WRQ4-Km]=mk3SLVN4HKm; userFrom=null; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; ab_sr=1.0.1_NDcyNWQ5M2U1MDc0NDFmMWNiZGFmOTJiNmJmZGJkM2Q2N2FkM2E2ODhjNDcyNTQ0N2FkZjM5OGVkYTU0NjFkYTg3YmVjYzNhOWE0YWJkMmU1ZjBkZDhjN2Q1MzdjMGE3ZTI0ZTIxN2NjZjU3Mjc5N2IxMGMyNjZiNDNkZTc3NmIzMDgxZjBkNzg3MDc0NDJlYjFhYzg4NTY0OGMxZjA1YTdhZTQwYjdlOTQ2YWU0MjcwNTUxYTZiNTM4NzU4NTcxOTA2ZDJmNDlmNDMwNGU5OWM0OTMwMTY0ZTZhOWRhYmQ=',
}

params = {
    'tn': 'resultjson_com',
    'word': f'{content}',
    'ie': 'utf-8',
    'fp': 'result',
    'fr': '',
    'ala': '0',
    'applid': '8460812860137060907',
    'pn': '30',
    'rn': '100',
    'nojc': '0',
    'gsm': '1e',
    'newReq': '1',
}

response = requests.get('https://image.baidu.com/search/acjson', params=params, cookies=cookies, headers=headers)
dir_path = r'D:\python\end_of_term\ChatPhoto\photo\SVM_classification\fish'
items = response.json()['data']['images']
print(items)
for i in range(len(items) - 1):
    response = requests.get(items[i]['thumburl'])
    img_save_path = f"{dir_path}/new{i}.png"
    with open(img_save_path, 'wb') as file:
        file.write(response.content)
