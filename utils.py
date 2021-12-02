# encoding:utf-8
import requests
import base64
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def get_access_token(api_key, secret_key):
    host = 'https://aip.baidubce.com/oauth/2.0/token?' \
        'grant_type=client_credentials&client_id={0}&client_secret={1}' \
        .format(api_key, secret_key)

    response = requests.get(host)

    if response:
        return response.json()['access_token']

    else:
        raise Exception('get access tokon faild')
    

def baidu_ocr(config, img_base64):
    request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
    # request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/numbers'

    access_token = get_access_token(config['api_key'], config['secret_key'])

    params = {"image": img_base64}

    request_url = request_url + "?access_token=" + access_token

    headers = {'content-type': 'application/x-www-form-urlencoded'}

    try:
        response = requests.post(request_url, data=params, headers=headers)

    except requests.exceptions.RequestException:
        error_message = 'access for OCR service out of time, network error.'
        raise Exception(error_message)

    else:
        data = response.json()
        
        if data.__contains__('words_result'):
            return data['words_result'][0]['words']

        else:
            try:
                if data['error_code'] == 110 or \
                        data['error_code'] == 111:
                    error_message = 'access for OCR service failed,'\
                        'Access token out of time or invalid.'
                        
                    raise Exception(error_message)

                else:
                    error_message = 'access for OCR service failed.'
                    raise Exception(error_message)

            except Exception:
                raise Exception('open api daily request limit reached')


def get_login_token():
    try:
        response = requests.get('https://fangkong.hnu.edu.cn/api/v1/account/getimgvcode')

    except requests.exceptions.RequestException:
        raise Exception('get access token out of time，network error')

    else:
        res_json = response.json()

        if res_json['code'] == 0:
            return res_json['data']['Token']

        else:
            raise Exception('get login token error.')


def get_token_var_code(config):
    token = get_login_token()

    img_url = 'https://fangkong.hnu.edu.cn/imagevcode?token={0}'.format(token)

    try:
        response = requests.get(img_url)

    except requests.exceptions.RequestException as e:
        raise Exception('get var img out of time, network error')

    else:
        url_content = response.content
        img_base64 = base64.b64encode(url_content)

        try:
            var_code = baidu_ocr(config, img_base64)

            return token, var_code

        except Exception as e:
            raise(e)
            # sys.exit(-1)


def sign_in(baidu_ocr_config, sign_in_config):
    token, var_code = get_token_var_code(baidu_ocr_config)

    sign_in_url = 'https://fangkong.hnu.edu.cn/api/v1/account/login'

    sign_in_data = {
        'Code': sign_in_config['id'],
        'Password': base64.b64decode(sign_in_config['pwd']).decode("utf-8"),
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
        response = requests.post(sign_in_url,
                                 headers=sign_in_headers,
                                 data=json.dumps(sign_in_data))

    except requests.exceptions.RequestException:
        raise Exception('can\'t fetch the login url，network error')

    else:
        res_json = response.json()

        if res_json['code'] == 0:
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

            print(get_local_time(), 'login succeeded.')

            return clock_in_headers

        else:
            if res_json['code'] == 1002:
                raise Exception('login failed: the var code was wrong.')

            else:
                raise Exception('login failed: other reason.')


def clock_in(clock_in_config, clock_in_headers):
    clock_in_url = 'https://fangkong.hnu.edu.cn/api/v1/clockinlog/add'

    try:
        response = requests.post(clock_in_url,
                                 headers=clock_in_headers,
                                 data=json.dumps(clock_in_config))

    except requests.exceptions.RequestException:
        raise Exception('can\'t fetch the clockin url, network error.')

    else:
        res_json = response.json()

        if res_json['code'] == 0:
            print(get_local_time(), 'clock in succeeded.')

            return True
        
        elif res_json['code'] == 1:
            print(get_local_time(), 'already clocked in today!')

            return True

        else:
            raise Exception('clockin failed: other reason')


def send_mail(mail_config, subject, content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = Header("no-reply@everyday.clock.in", 'utf-8')  
    message['To'] =  Header("time to sleep!", 'utf-8')

    try:
        smtp_mail = smtplib.SMTP_SSL(mail_config['host'], 465) 

        smtp_mail.login(mail_config['sender'], 
                        base64.b64decode(mail_config['auth']).decode("utf-8"))
 
        smtp_mail.sendmail(mail_config['sender'], 
                        mail_config['receivers'],
                        message.as_string())

        smtp_mail.quit()
        
    except smtplib.SMTPException:
        print(get_local_time(), 'Mail send failed!')

    else:
        print(get_local_time(), 'Mail send succeeded!')


def get_config():
    try:
        with open('./config.json','r',encoding='utf8') as fp:
            config = json.load(fp)

    except Exception:
        print('Please check config file.')
        print('Stoppend by error.')
        exit(-1)

    else:
        return config


def get_local_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def get_local_hour():
    return time.localtime(time.time()).tm_hour


def wait_until_next_hour():
    now = time.localtime(time.time())
    wait_seconds = (60 - now.tm_min) * 60 - now.tm_sec

    print(get_local_time(), 'wait for the next hour after', str(wait_seconds) + 's')
    time.sleep(wait_seconds)


def print_logs(content):
    print(get_local_time(), content)


def handle_error(error):
    print_logs(error)
    print_logs('retry in 5 second...')

    time.sleep(5)


def main():
    # get_access_token()
    pass


if __name__ == '__main__':
    main()

