# coding=UTF-8

import requests
import re
from bs4 import BeautifulSoup as bf
import time
import random
import json

s = requests.session()

#检查账号是否需要滑块验证
def check_login():
    url_login_check = 'https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8'
    data = {'username': '15626724248',
            'ua': '121#eOllkGZ0bUwlVl2qxF/JlV+GecP44uiI8tOQxbHIeMC3OW1i73eblXtYOc8fD7jVlGgY+aBIDMpdyzaxEmD5VM/YOcffx5iIiHdm+zP5KllVO3rrE5DIll9YOc8fDujllwgYxaPIKM9lOQrJEmD5lwLYO78fK5i5R48r5lQVBIbvsbc9MtFPD0rWXVFbbZ3glWfopCibkZ0T83Smbgi0CeIAFtZFHOpznjxSRjLbCZeTM3tA3pFDkeHXmo60bZienqC9pCibCZ0T83BhbZs0keHaF9FbbZsbnjxSpXb0MqAWQtBlQqS0mARltoJHMEeqPyx+P2603CLP831hbZs0jQtAZnqwt5cI4/WZPwz5XgFk7bObblPYmmWxA8ylpHXKLOpZ9E58FglhTy4VCkDHQZ//nJShI5fAjv8FLvSedPY6S9VgS5hp5N4G+Bn5R+4MEOASwNh/+PiemcMeuHFghaAZivbFHE48p5RMjM8VGFQhO5S+IK2KQv5+D2M0pxdIlp9PlFFCRJGlfUjz78iGp8wn9J9btCB67pUUuWyCM+OuAVtrYL7dimYJGlR+m10io23YvgwRgSIiIhkVvoxcQIMq7lpXrDpbPUO/W6QBNNTmPpKw/XdTKdFopp+TNjMI2iHCtAqoOSNql0NvO5Wk9/XdaaYUQSKjzlzixap94lOjPRpuWWtfEApGWAwoMGLjRXbMm51cfGK4dFWBBkVNEQrZqiXZT5g8DCN03O2Ttuzvwt7Cxu3s0bRQyJzuMuQy+iIW/wSRwWe6YG2u8VDXeDGfu60TEA3yC2FNChVNwQ90VwaGtnia3QWGam3t97NX+/VW35+yR0Ivvr+yVrquziyoWJ6DEKTdsAbgfoQ/VjghBVCKqXL3IYLfZHWtkzDDM7MeBhu7PTo1yLT6VDKRjbWj6cd3Cs9sHkvkOgWrJ3tKef/sYpTH3F6+mTgRmfK6QYL8wp4XOJ9lvxdAB/YycQG0dV3KgLaxWaa5W9cSNDS93wEuI7J4lqYWmQxRnUTooWyweIAU/zlZg6vAFQT6Oh642HTyQxK3Aye7cqGXIJBW7WYYOJZuvTrozn0zxy8cSxhFHlo5xYA7Fxf1QHAcvSjbERAsLJn9HwkdPHmk4t2x88XOD91u6qK6stVrXpu/EUM/834wABRFexpPTpBQ7QLHYF1sdAxr8vKuuk3h2Z+H1m5pvl3j0i81qKAT0pSaPjNQkTZcIwldjMRJoOc4bxNFtIHw218y7DNBGyJSZOcjWC+iScg1gEGkiB0OCrY9FAX4bkax7NjhLF38cBC1klmrQPAATQ1iRuioIMsHc2BTi44o'
            }
    try:
        re_check = s.post(url_login_check , data=data , timeout = 10)
        
    except Exception as e:
        print(e)
    check = re_check.json()['needcode']
    print('是否有验证：', '是' if check else '否')
    return check

#登录验证获取st申请地址
def login_get_st():
    url_login = 'https://login.taobao.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Origin': 'https://login.taobao.com',
        'Connection': 'keep-alive',
        'Referer': 'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.201864-2.d1.5af911d90MrdPB&f=top&redirectURL=http%3A%2F%2Fwww.taobao.com%2F',
        'Cookie': '_uab_collina=157312683523771720583366; thw=cn; t=37233682d0732aef1734bba54a4f03f1; mt=ci=0_0; enc=oHkNrQPR2KbirX9QZbKRcsW0e%2BkbMxobBoLP%2BGq3IqCYfGT5e6XLtg7Fl52uLWoD66FLytHg3nZssL5wKnHFNg%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; cookie2=7f252b76e7a41e3be4d15868ffbb7a98; _tb_token_=ebfe3bb6dae33; XSRF-TOKEN=7e1b4bab-47be-4fb9-9105-d9b491d6e20a; isg=BI-P2u5wDkM9LAq-k8NXBguHHSNZHIbfD8bXCaGdLf4ScKtyqYb0J7gicmDrE7tO; l=dBQ-sTGnqZEfD8xSBOfNNuI8SO_tiIOVGkPzw4GX_ICP_UCW5cPFWZd5FOTXCn1VnsYXR3lHGSvJBPLTny4EhWrr2D_7XPQoRdLh.; cna=D/BKFnuSoRoCAXjn0PWhMVWf; v=0',
        'Upgrade-Insecure-Requests': '1'
    }
    data = {"TPL_username":"15626724248","TPL_password":"","ncoSig":"","ncoSessionid":"","ncoToken":"76aa57d1e72c61f22811c4d033cb98e60fa2e785","slideCodeShow":"false","useMobile":"false","lang":"zh_CN","loginsite":"0","newlogin":"0","TPL_redirect_url":"http://www.taobao.com/","from":"tbTop","fc":"default","style":"default","css_style":"","keyLogin":"false","qrLogin":"true","newMini":"false","newMini2":"false","tid":"","loginType":"3","minititle":"","minipara":"","pstrong":"","sign":"","need_sign":"","isIgnore":"","full_redirect":"","sub_jump":"","popid":"","callback":"","guf":"","not_duplite_str":"","need_user_id":"","poy":"","gvfdcname":"10","gvfdcre":"68747470733A2F2F7777772E74616F62616F2E636F6D2F","from_encoding":"","sub":"","TPL_password_2":"4ee7d9c577634389a95b3436bdb89a40387818a9b32d163e648e926859336cd20cd7626de2916d147d8a32b97507431365b2748028b760290d7ae25bde3a211ff35504b9fd4fc7452129722c7b8b4470e9fbfd8d939a12010ad0410914fe672a67a3bede6ca0d5e255bba80686527ff87033e4c36395702450b2324a02e6824f","loginASR":"1","loginASRSuc":"1","allp":"","oslanguage":"zh-CN","sr":"1536*864","osVer":"","naviVer":"firefox|70","osACN":"Mozilla","osAV":"5.0+(Windows)","osPF":"Win32","miserHardInfo":"","appkey":"00000000","nickLoginLink":"","mobileLoginLink":"https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.201864-2.d1.5af911d90MrdPB&f=top&redirectURL=http://www.taobao.com/&useMobile=true","showAssistantLink":"","um_token":"T0C725018B0F0CDDEEAD92F89CEEB02D9589E8A6E78DDBAC197A3DDE33F","ua":"121#AjmlkqjaorllVlhL+QsylV+Gec/fKJGV9l3Lxjm5dBXdTjBN9IDIll9YLaffKujllmQYxy2iaCllOQr5qwDIlw9mAOkL2zjVlwgy+aPIKMtAA3rnEkDIll9YOc8fDuj9lGgY+zpIDM9lOQrJEmDhllXYAQGMy63HLlS9D0g6bqRVpSCge69xYXb0CO3LzPBhbZseCeHXQtK0bZibnjYSRC9v1h+48u/YM2s0CNHLFwYF2XrDnnGKpCD0CZN883BhbZs0CeHXF960C6iDnnx9pXb0C6048u/mCbeVMYPVB9L0b4lQuiGdRg9lqXV98R12IPsjk+HXFhq9lf+TASYrvJCppPOLWZuG90gd4bpm2gvUCC8cnStyDKMRcX4FLByX0vaLUd9ECaSFfO2BKNMGlq+RIOmsgedPEyltbU0AUDO+Ay6bEMPHrUSMBMJq/cJVnq7FIEqScjRSN87bnxRduBguj0IoGnjpAYB5uKaca0YItI84VlBG5beNSrYy2/WH0zWD98fT+78TPONDegKMP2Mfk056sXGLTugf7bY/Yz9c7h7fEedZ2CZg9FG8neSa5h43bnUT7/IADtW6JfSGZV3zPTpmtMH9B/k9wG23OBeb0UzKrXxPCnlbx/aG79h0N9EDF8ok3hbQyVWNV01uoR4MZeiT78Qx3HkJEU1tjAJOqP0tCZYGPgvWJC/1nmghhKVbwbd0X1yO4jYgfWS7v/UZHgYMhXPAphUseTRw8SjHi6RjU1IcdV8KX/nUDbBKwOwNUmwBg5kJxuajtilgP0xUPBLNnvZ7+yqhy6CfiIPxvv3X1bD1RzVBJ9Wc8x3fRU7baU6YghBqgQenoFyDF2eCgwssJo7QWowlV7OaVCeZ6MvxgqesaEUYzHiXnMt8HpMQ/PErv4nAZhVRE2F9+y3PWMioLUfC6KA63yNbg0wKHWmmf0mejkbO2kJZ/BH/+cd/SOkla+dQRGyG+ldv5qycXG+2KCh/FZXUhiBoZ2FiFiJKdvRQ0GX6nXIS5HEqMrSBymOI+PSuefro6jD5lPH0J7EfWJ11P3TPDPzcn2qfltUX7Dci7DIiSfeHh30S71PrD/zkp3GHDo2V+nKHAe3AN+Ox5XSdj8ulJF6Iww=="}

    try:
        resp = s.post(url_login , headers = headers , data= data)
        ts_url = re.findall(r'<script src="(.*?)"></script>' , resp.text)
    except Exception as e:
        print('登录失败，原因：', e)
        return 0
    
    print('用户验证成功st申请地址为：', ts_url[0]) 
    # with open('token.txt' , 'w') as f:
        # f.write(ts_url[0])

    return ts_url[0]

#获取st码
def get_st():
    st_url = login_get_st()
    try:
        st_html = s.get(st_url)
    except Exception as e:
        print('获取st码失败，错误原因：' , e)
        return 0
    st = re.findall(r'"st":"(.*?)"', st_html.text)
    print('st获取成功，st为：',st[0])

    return st[0]

#使用st登录淘宝
def st_login():
    st = get_st()
    url = 'https://login.taobao.com/member/vst.htm?st={}'
    headers = {
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
        }
    try:
        t_html = s.get(url.format(st) , headers = headers)
    except Exception as e:
        print('用st码请求失败，原因', e)
    if t_html.status_code == 200:
        print('成功，正在跳转页面')
    
    return True

#爬取淑女连衣裙100页测试
def test():
    url = 'https://s.taobao.com/search?q=裙子&s={}'
    headers = {
            'Referer': 'https://taobao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            
        }
    num =0
    try:
        for i in range(99):
            print(r'>'*int(i/100) , end = '')
            page_url = url.format(num)
            num +=44
            html = s.get(page_url , headers = headers)
            time.sleep(random.randint(8 , 10))
            #获取信息
            name = re.findall(r'"raw_title":"(.*?)"' , html.text)   #商品名称
            price = re.findall(r'"view_price":"(.*?)"' , html.text) #价格
            loc = re.findall(r'"item_loc":"(.*?)"' , html.text)  #地点
            sales = re.findall(r'"view_sales":"(.*?)"' , html.text) #销量
            nick = re.findall(r'"nick":"(.*?)"', html.text)      #店铺名字
            print(name[i]) #空的话让它报错
            #保存信息
            with open(r'../data/test.csv' , 'a' , encoding='gbk') as f:
                for ii in range(len(name)):
                    f.write(','.join([name[ii] , price[ii] , loc[ii], sales[ii], nick[ii] , '\n'] )) 
                    # print(name[i] , price[i] , loc[i] , sales[i] , nick[i] ,'\n')
    except Exception as e:
        print('被抓啦','第{}页'.format(i))
        # print('休息150秒再继续')
        # time.sleep(150)
        # test(i , num)
        # s.cookies = use_cookie()

    # print(html.text)

def test2():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            
        }
    url = 'https://i.taobao.com/my_taobao.htm?spm=a1z0k.7386009.a210b.d1000352.265837deQH0zcv&tracelog=mytaobaonavindex&nekot=1470211439696'
    html = s.get(url , headers = headers)
    print(html.text)
##    name = re.find()

#保存cookies
def cookie_save():
    cookie = requests.utils.dict_from_cookiejar(s.cookies)
    with open('cookie.txt' , 'w') as f:
        json.dump(cookie , f)
    print('cookies保存成功！')

#使用cookie
def use_cookie():
    with open('cookie.txt' , 'r') as f:
        cookie = json.load(f)
        cookies = requests.utils.cookiejar_from_dict(cookie)
    return cookies
#s.cookies = use_cookie()

if __name__ == "__main__":

    # check_login()
    # login_get_st()
    # get_st()
    st_login()
    #s.cookie = use_cookie()
    test()
    test2()
    #cookie_save()
    
    
