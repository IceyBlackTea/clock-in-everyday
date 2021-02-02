# encoding:utf-8
import requests
import time


default_request_payload = {
    "Temperature": None,  # null
    "RealProvince": "北京市",
    "RealCity": "北京市",
    "RealCounty": "东城区",
    "RealAddress": "1",
    "IsUnusual": "",
    "UnusualInfo": "",
    "IsTouch": "",
    "IsInsulated": "0",
    "IsSuspected": "0",
    "IsDiagnosis": "0",
    "tripinfolist": [
        {
            "aTripDate": "",
            "FromAdr": "",
            "ToAdr": "",
            "Number": "",
            "trippersoninfolist": []
        }
    ],
    "toucherinfolist": [],
    "dailyinfo": {
        "IsVia": "0",
        "DateTrip": ""
    },
    "IsInCampus": "",
    "IsViaHuBei": "",
    "IsViaWuHan": "0",
    "InsulatedAddress": "",
    "TouchInfo": "",
    "IsNormalTemperature": "",
    "Longitude": None,  # null
    "Latitude": None,  # null
}


def get_local_time():
    return time.strftime("%Y-%m-%d %H:%I:%S", time.localtime(time.time()))


def baidu_ocr(img_base64):
    # request_url = ''https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic' # 每日免费50000次,但是会有字母
    request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/numbers'  # 每日免费200次

    # 你的token
    access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    params = {"image": img_base64}

    request_url = request_url + "?access_token=" + access_token

    headers = {'content-type': 'application/x-www-form-urlencoded'}

    try:
        response = requests.post(request_url, data=params, headers=headers)

    except requests.exceptions.RequestException:
        raise Exception('申请OCR服务超时，网络环境异常')

    else:
        if response.json().__contains__('words_result'):
            return response.json()['words_result'][0]['words']

        else:
            if response.json()['error_code'] == 110 or \
                    response.json()['error_code'] == 111:
                raise Exception('申请OCR服务失败，Access token过期或无效')

            else:
                error_message = '申请OCR服务失败，' + response.json()['error_msg']
                raise Exception(error_message)


def get_access_token():
    #
    # 向授权服务地址https://aip.baidubce.com/oauth/2.0/token发送请求（推荐使用POST），并在URL中带上以下参数：
    #
    # grant_type： 必须参数，固定为client_credentials；
    # client_id： 必须参数，应用的API Key；
    # client_secret： 必须参数，应用的Secret Key；

    api_key = 'xxxxxxxxxx'

    secret_key = 'xxxxxxxxxx'

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}' \
        .format(api_key, secret_key)

    print(host)

    response = requests.get(host)

    if response:
        print(response.json())


def main():
    # get_access_token()
    pass


if __name__ == '__main__':
    main()
