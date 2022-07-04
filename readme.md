# clock-in-everyday

## Welcome

如果对你有帮助欢迎 Star ~

## Introduction

两种实现方式都可以使用，都使用了百度云OCR处理验证码图片

- `auto_clock_in.py` - 推荐：使用 `requests` 的 `get` 和 `post` 处理 `https`请求，配合 `utils.py` 使用 

- `auto_clock_in_with_selenium.py` - `selenium` 和 `webDriver` 实行浏览器自动化 (已删除，可以查看历史 commit)

## Environment

### Python

`requests`

```
pip3 install requests
```

### Baidu AI OCR

注册一个百度云账号，申请文字识别OCR服务，获取服务的 `api_key` 和 `secret_key`

不懂的话可以百度或者看 [百度云的文档](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu)

## Run

1. 修改 `_config.json` 内容，并重命名为 `config.json`
2. `python3 ./src/auto_clock_in.py`

### About `config.json`

#### `type_`

在校或在家，根据 `type_` 不同打卡信息不同.

根据其他参数，可选为`at_school` 或 `at_home`.

#### `send_mail`

是否发送邮件提醒，可选为 `true` 或 `false`.

#### `baidu_ocr_config`

调用百度云OCR的参数，`api_key` 与 `secret_key` 是必须的.

#### `sign_in_config`

登录用信息，包含 `id`, `pwd`.

- `id` : 学号
- `pwd` : 密码, 默认 base64 加密.

#### `clock_in_config`

打卡用信息，分为 `at_school`, `at_home` 两类.

需要修改的有: 

- `RealAddress`: 详细地址
- `RealCity`: 市区/县
- `RealProvince`: 省

#### `mail_config`

邮箱使用配置, 包含 `host`, `sender`, `auth`, `receivers`;

- `host`: 邮箱服务主机

- `sender` : 邮件发送方，需要与 `auth` 对应

- `auth` : 邮箱授权码，需要与 `sender` 对应，默认使用 base64 加密

- `receivers` : 邮件接收方，可以有多个，固为数组

## Others

原本只写了 selenium 自动化的，后来和同学一聊发觉页面登录时的 token 可以 get 直接拿，比原本想的还要简单...

所以补充一个只用 requests 的更简单的版本.

已改为 1 点自动打卡，并添加了邮箱提醒;

> 0 点打开后端有时候还认为是前一天...

有问题可以 issues ，如果页面或者接口变了和我说下...

> 2022.7 原本提示不能网页端打卡准备一直手动了，结果现在又可以了；重新检查网页发现加了些新的验证，简单改改自动打卡复活！
