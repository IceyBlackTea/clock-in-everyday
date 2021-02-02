# encoding:utf-8
import base64
import json
import requests
import sys
import time

from requests import utils

import utils

info = {
    'id': 'xxxxxxxxxxxx',
    'pwd': 'xxxxxxxxxxx',
    'location': 'xxx/xxx/xxx',
    'detail': 'xxx',
    'temperature': '36.5'  # 离校时不需要
}


def get_token():
    try:
        response = requests.get('https://fangkong.hnu.edu.cn/api/v1/account/getimgvcode')

    except requests.exceptions.RequestException:
        raise Exception('获取登录token超时，网络环境异常')

    else:
        res_json = response.json()
        if res_json['code'] == 0 and res_json['msg'] == '成功':
            return res_json['data']['Token']

        else:
            raise Exception('获取登录token失败 ' + res_json['msg'])


def get_img_code():
    token = get_token()

    img_url = 'https://fangkong.hnu.edu.cn/imagevcode?token={0}'.format(token)

    try:
        response = requests.get(img_url)

    except requests.exceptions.RequestException as e:
        raise Exception('获取验证码图片超时，网络环境异常')
    else:
        url_content = response.content
        img_base64 = base64.b64encode(url_content)

        try:
            var_code = utils.baidu_ocr(img_base64)
            return token, var_code

        except Exception as e:
            # 这个怕访问次数太多了扣钱，所以错误了就停了~
            print(e)
            sys.exit(-1)


def sign_in():
    token, var_code = get_img_code()

    sign_in_dict = {
        'Code': info['id'],
        'Password': info['pwd'],
        'Token': token,
        'VerCode': var_code,
        'WechatUserinfoCode': ''
    }

    sign_in_headers = {
        'Content-Type': 'application/json;charset=UTF-8',

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.96 Safari/537.36 '
                      'Edg/88.0.705.56'
    }

    try:
        response = requests.post('https://fangkong.hnu.edu.cn/api/v1/account/sign_in',
                                 headers=sign_in_headers,
                                 data=json.dumps(sign_in_dict))

    except requests.exceptions.RequestException:
        raise Exception('连接超时，网络环境异常')

    else:
        res_json = response.json()
        if res_json['code'] == 0 and res_json['msg'] == '成功':
            cookies = requests.utils.dict_from_cookiejar(response.cookies)

            timestamp = str(int(time.time()))

            clock_in_headers = {
                'Accept': 'application/json, text/plain, */*',

                'Accept-Encoding': 'gzip, deflate, br',

                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',

                'Connection': 'keep-alive',

                'Host': 'fangkong.hnu.edu.cn',

                'Content-Type': 'application/json;charset=UTF-8',

                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/88.0.4324.96 Safari/537.36 '
                              'Edg/88.0.705.56',

                'Sec-Fetch-Site': 'same-origin',

                'Sec-Fetch-Mode': 'cors',

                'Sec-Fetch-Dest': 'empty',

                'Origin': 'https://fangkong.hnu.edu.cn',

                'Referer': 'https://fangkong.hnu.edu.cn/app/',

                'Cookie': "Hm_lvt_d7e34467518a35dd690511f2596a570e=" + timestamp + ";"
                          "TOKEN=" + cookies["TOKEN"] + ";"
                          ".ASPXAUTH=" + cookies[".ASPXAUTH"]
            }

            print(utils.get_local_time(), '登录成功')

            return clock_in_headers

        else:
            raise Exception('登录失败 ' + res_json['msg'])


def clock_in(type, clock_in_headers):
    # type 留着返校后，补充另一种打卡

    clock_in_dict = utils.default_request_payload

    locations = info['location'].split('/')

    clock_in_dict['RealProvince'] = locations[0]
    clock_in_dict['RealCity'] = locations[1]
    clock_in_dict['RealCounty'] = locations[2]
    clock_in_dict['RealAddress'] = info['detail']

    clock_in_dict['IsInCampus'] = "0"  # 在校
    clock_in_dict['IsNormalTemperature'] = "1"  # 体温
    clock_in_dict['IsViaHuBei'] = "0"  # 中高风险地区
    clock_in_dict['IsViaWuHan'] = "0"  # 中高风险地区
    clock_in_dict['IsUnusual'] = "0"  # 不良反应
    clock_in_dict['IsTouch'] = "0"  # 接触高危人员

    try:
        response = requests.post('https://fangkong.hnu.edu.cn/api/v1/clock_inlog/add',
                                 headers=clock_in_headers,
                                 data=json.dumps(clock_in_dict))

    except requests.exceptions.RequestException:
        raise Exception('连接超时，网络环境异常')

    else:
        res_json = response.json()
        if res_json['code'] == 0 and res_json['msg'] == '成功':

            print(utils.get_local_time(), '签到成功')

            return True

        else:
            raise Exception('签到失败 ' + res_json['msg'])


def main():
    while True:
        try:
            headers = sign_in()

        except Exception as e:
            print(utils.get_local_time(), e)
            print('一秒后重试...')
            time.sleep(1)

        else:
            try:
                clock_in('atHome', headers)

            except Exception as e:
                print(utils.get_local_time(), e)
                print('一秒后重试...')
                time.sleep(1)

            else:
                break


if __name__ == '__main__':
    main()
