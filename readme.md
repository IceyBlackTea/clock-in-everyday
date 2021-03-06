# 自动打卡
## 声明

本项目代码开源，仅供 Python 与前端学习，不支持其他用途

作者本人与代码使用者无关，不承担任何责任

如果对你有帮助欢迎 Star~

## 简要介绍
两种实现方式都可以使用，都使用了百度云OCR处理验证码图片

+ auto_clock_in.py - 推荐：使用 requests 的 get 和 post 处理 https，配合 utils.py 使用 

+ auto_clock_in_with_selenium.py - selenium 和 webDriver 实行浏览器自动化


## 使用环境

### python
requests

selenium >= 3.141

pip install selenium

> 如果是 chromium 内核的新版 edge 浏览器还需要 msedge.selenium_tools
>
> pip install msedge-selenium-tools selenium==3.141

### webDriver
推荐chromium 内核或其他现代浏览器。

根据你的浏览器内核去下载对应的 webDriver。

如：

我的 chromium edge 的内核是 88.0.705.56 版本：
![chromium-kernel-version](./assets/chromium%20kernel%20version.png)

前往 [官方下载地址](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/#downloads)
下载对应版webDriver：
![edge-webdriver-download](./assets/edge%20webdriver%20download.png)

下载好后解压即可

其他浏览器类似，百度下就能找到，一般有国内镜像站

### 百度云OCR
注册一个百度云账号，申请文字识别OCR服务，获取服务的 api_key 和 secret_key

不懂的话可以百度或者看 [百度云的文档](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu)

get_access_token.py 中填写 api_key 和 secret_key 后，运行获取临时的token（会过期，一般30天）

## 运行

1. 使用 utils.py 中的 get_access_token() 或者其他途径获取 access token

2. 修改相关参数：access token，打卡相关信息，webDriver路径等。

3. 运行&等待

> ocr识别有可能错误，网络不通畅、页面加载过慢也可能导致错误
>
> 错误后会自动重启。

## 其他
原本只写了 selenium 自动化的，后来和同学一聊发觉页面登录时的 token 可以 get 直接拿，比原本想的还要简单...

所以补充一个只用 requests 的更简单的版本

扩展的话可以弄成隔24小时自动执行或者脚本定点执行

有问题可以 issues ，如果页面或者接口变了和我说下...
