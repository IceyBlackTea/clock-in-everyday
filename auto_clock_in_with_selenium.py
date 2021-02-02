# encoding:utf-8
import base64
import requests
import time

# 使用chromium edge浏览器
from msedge.selenium_tools import Edge, EdgeOptions

# 如果你使用其他浏览器
# from selenium import webdriver

# 你的信息
stu = {
    'id': 'xxxxxxxxx',
    'pwd': 'xxxxxxxxx',
    'location': '北京市/北京市/北京市',
    'detail': '北京市'
}


def set_browser():
    options = EdgeOptions()
    options.use_chromium = True

    # 浏览器路径
    options.binary_location = r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"

    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # webDriver路径
    driver = Edge(executable_path=r'E:\edgedriver_win64\msedgedriver.exe', options=options)

    return driver


def baidu_ocr(img_base64):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

    # 你的token
    access_token = 'xxxxx'

    params = {"image": img_base64, "language_type": "CHN_ENG"}

    request_url = request_url + "?access_token=" + access_token

    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.post(request_url, data=params, headers=headers, )

    if response:
        # print(response.json())
        return response.json()['words_result'][0]['words']


def sign_in(browser):
    browser.get(r'https://fangkong.hnu.edu.cn/app/')

    browser.find_element_by_class_name('lgoin-background').click()

    # 图片异步加载需要时间
    time.sleep(1)

    imgs = browser.find_elements_by_tag_name('img')

    if len(imgs) != 4:
        print('error: img was not loaded!')

    img_url = imgs[3].get_attribute('src')
    url_content = requests.get(img_url).content
    img_base64 = base64.b64encode(url_content)

    word = baidu_ocr(img_base64)

    # 错了直接改下省的慢
    word = word.replace('o', '0')
    word = word.replace('了', '3')

    if len(word) != 4:
        raise ValueError('ocr result error')

    word = str(int(word))

    print('ocr result: ' + word)

    inputs = browser.find_elements_by_tag_name('input')

    inputs[0].send_keys(stu['id'])

    inputs[1].send_keys(stu['pwd'])

    inputs[2].send_keys(word)

    button = browser.find_elements_by_tag_name('button')[0]

    button.click()


def location_click(browser, column_num, row_num):
    js = 'document.querySelector("#app > div > div.van-popup.van-popup--bottom > ' \
         'div > div.van-picker__columns > div:nth-child(' + str(column_num + 1) + ') > ' \
         'ul > li:nth-child(' + str(row_num + 1) + ')").click()'

    browser.execute_script(js)


def clock_in(browser):
    loc_inputs = browser.find_elements_by_xpath("//div[@class='van-cell__value']")

    loc_inputs[0].click()

    time.sleep(1)

    locations = stu['location'].split('/')

    loc_columns = browser.find_elements_by_xpath("//div[@class='van-picker-column']")

    for i in range(3):
        loc_column = loc_columns[i].find_elements_by_css_selector('div > ul > li')
        for index in range(len(loc_column)):
            if loc_column[index].get_attribute('innerHTML') == locations[i]:
                location_click(browser, i, index)
                time.sleep(0.1)
                break

    confirm_button = browser.find_elements_by_class_name('van-picker__confirm')[0]
    confirm_button.click()

    detail_input = loc_inputs[1].find_elements_by_tag_name('input')[0]

    detail_input.send_keys(stu['detail'])

    radio_groups = browser.find_element_by_xpath('//div[@role="radiogroup"]')

    # 如果不是默认的填写，需要手动输入其他内容
    flags = ['no', 'yes', 'no', 'no', 'no']

    for i in range(5):
        index = 0
        if flags[i] == 'no':
            index = 1

        radio_groups.find_elements_by_xpath('//div[@role="radio"]')[i * 2 + index].click()

    clock_in_button = browser.find_elements_by_tag_name('button')[3]

    clock_in_button.click()


def automatic(browser):
    sign_in(browser)

    time.sleep(2)

    clock_in(browser)


def main():
    while True:
        try:
            browser = set_browser()
            automatic(browser)

        except Exception:
            print('打卡失败，重启')

        else:
            break

        finally:
            browser.quit()


if __name__ == '__main__':
    main()
