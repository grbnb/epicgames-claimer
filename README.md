# EpicGames Claimer

<!-- [START badges] -->

<!-- ![](https://img.shields.io/badge/language-python-3572A5.svg) ![](https://img.shields.io/github/license/luminoleon/epicgames-claimer.svg) ![](https://img.shields.io/github/last-commit/luminoleon/epicgames-claimer.svg) -->

<!-- [END badges] -->

###### [疑难解答](docs/troubleshooting.md) | [Docker](docs/README_DOCKER.md)

> 自动领取Epic游戏商城[每周免费游戏](https://www.epicgames.com/store/free-games)。

十分简单易用，使用过程中几乎不需要输入或修改任何参数。

如果你觉得本项目对你有帮助，请star本项目。

蓝奏云： <https://luminoleon.lanzoui.com/b02iby4lg> 密码:15k1

## 开始

### Windows

[下载](https://github.com/luminoleon/epicgames-claimer/releases)

Windows版本目前不支持自动更新。

#### Windows版本可选参数

见[Python版本可选参数](#python版本可选参数)

### Docker

* 基于Ubuntu
    
    ``` bash
    docker run -it luminoleon/epicgames-claimer
    ```

* 基于Alpine Linux

    ``` bash
    docker run -it luminoleon/epicgames-claimer:latest-alpine
    ```

使用方法见[README_DOCKER.md](docs/README_DOCKER.md)或[Docker hub页面](https://hub.docker.com/r/luminoleon/epicgames-claimer)。

### Python

要求Python >= 3.6。

#### 如何使用

1. 克隆/[下载](https://github.com/luminoleon/epicgames-claimer/releases)

    ``` bash
    git clone -b main https://github.com/luminoleon/epicgames-claimer.git
    cd epicgames-claimer
    ```

2. 安装Python模块

    ``` bash
    pip3 install -r requirements.txt
    ```

3. 安装依赖（仅Linux）

    ``` bash
    sudo sh install_dependencies.sh
    ```

4. 运行

    ``` bash
    python3 main.py
    ```

    <details>
    <summary>启用自动更新</summary>

    ```bash
    python3 main.py --auto-update
    ```

    </details>

    <details>
    <summary>不使用交互输入</summary>

    ```bash
    python3 main.py -u <你的邮箱> -p <你的密码>
    ```

    ```bash
    python3 main.py -u <你的邮箱> -p <你的密码> -t <双重验证代码>
    ```

    </details>

    <details>
    <summary>添加通知推送</summary>

    * server酱
        ```bash
        python3 main.py -ps <SendKey>
        ```

    * Bark
        ```bash
        python3 main.py -pbu <BarkPushUrl> -pbk <BarkDeviceKey>
        ```

	    非自建服务端无需-pbu参数，默认采用官方推送地址https://api.day.app/push

    * Telegram
        ```bash
        python3 main.py -ptt <TelegramBotToken> -pti <TelegramChatId>
        ```

    </details>

#### Python版本可选参数

| 参数                                   | 说明                                                       | 备注                                                                                                                                        |
| -------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `-n`, `--no-headless`                  | 显示浏览器的图形界面                                       |                                                                                                                                             |
| `-c`, `--chromium-path`                | 指定浏览器可执行文件路径                                   |                                                                                                                                             |
| `-r`, `--run-at`                       | 指定每日运行时间                                           | 格式：HH:MM，默认为当前时间                                                                                                                 |
| `-o`, `--once`                         | 运行一次领取过程后退出                                     | [参数`--once`或环境变量`ONCE`的具体含义，应在什么情况下使用](docs/troubleshooting.md#参数--once或环境变量once的具体含义应在什么情况下使用) |
| `-a`, `--auto-update`                  | 启用自动更新                                               | 运行`epicgames_claimer.exe`或`epicgames_claimer.py`此参数无效                                                                               |
| `-u`, `--username`                     | 设置用户名/邮箱                                            |                                                                                                                                             |
| `-p`, `--password`                     | 设置密码                                                   |                                                                                                                                             |
| `-t`, `--verification-code`            | 设置双重验证代码                                           |                                                                                                                                             |
| `--cookies`                            | 设置保存cookies信息文件路径                                | 用`get_cookies.py`或者`get_cookies.exe`获取                                                                                                 |
| `-l`, `--login`                        | 登录并创建User_Data后退出                                  | 需要在打开的浏览器里手动完成登录                                                                                                            |
| `-ps`, `--push-serverchan-sendkey`     | 设置Server酱SendKey                                        |                                                                                                                                             |
| `-pbu`, `--push-bark-url`              | 设置Bark服务端地址                                         | 默认: https://api.day.app/push                                                                                                              |
| `-pbk`, `--push-bark-device-key`       | 设置Bark的DeviceKey                                        |                                                                                                                                             |
| `-ptt`, `--push-telegram-bot-token`    | 设置Telegram bot token                                     |                                                                                                                                             |
| `-pti`, `--push-telegram-chat-id`      | 设置Telegram chat ID                                       |                                                                                                                                             |
| `-pwx`, `--push-wechat-qywx-am`        | 设置企业微信应用推送的QYWX_AM                              | 参考：http://note.youdao.com/s/HMiudGkb                                                                                                     |
| `-pda`, `--push-dingtalk-access-token` | 设置钉钉群聊机器人access token                             |                                                                                                                                             |
| `-pds`, `--push-dingtalk-secret`       | 设置钉钉群聊机器人secret                                   | 没有勾选加签则不需要此参数                                                                                                                  |
| `-ns`, `--no-startup-notification`     | 禁用脚本启动时推送一条通知                                 |                                                                                                                                             |
| `--push-when-owned-all`                | 当执行领取过程中发现全部可用周免游戏都已领取时推送一条通知 | 默认没有游戏被领取时不会推送通知                                                                                                            |
| `-v`, `--version`                      | 显示版本信息并退出                                         |                                                                                                                                             |

## 部署

**注意：由于Epic游戏商城限制了单个IP地址领取免费游戏的总量，所以使用公共IP领取游戏可能会失败。**

### 腾讯云函数

需要关闭双重验证。

目前不支持自动更新。

需要上传的文件：epicgames_claimer.py，requirements.txt

执行方法：epicgames_claimer.main_handler

推荐配置：内存1024MB，执行超时时间900秒

#### 环境变量

| 变量                       | 说明                                                                     | 备注                                    |
| -------------------------- | ------------------------------------------------------------------------ | --------------------------------------- |
| EMAIL                      | 设置用户名/邮箱                                                          |                                         |
| PASSWORD                   | 设置密码                                                                 |                                         |
| PUSH_SERVERCHAN_SENDKEY    | 设置Server酱SendKey                                                      |                                         |
| PUSH_BARK_URL              | 设置Bark服务端地址                                                       | 默认: https://api.day.app/push          |
| PUSH_BARK_DEVICE_KEY       | 设置Bark的DeviceKey                                                      |                                         |
| PUSH_TELEGRAM_BOT_TOKEN    | 设置Telegram bot token                                                   |                                         |
| PUSH_TELEGRAM_CHAT_ID      | 设置Telegram chat ID                                                     |                                         |
| PUSH_WECHAT_QYWX_AM        | 设置企业微信应用推送的QYWX_AM                                            | 参考：http://note.youdao.com/s/HMiudGkb |
| PUSH_DINGTALK_ACCESS_TOKEN | 设置钉钉群聊机器人access token                                           |                                         |
| PUSH_DINGTALK_SECRET       | 设置钉钉群聊机器人secret                                                 | 没有勾选加签则不需要此参数              |
| PUSH_WHEN_OWNED_ALL        | 设置为true时，当执行领取过程中发现全部可用周免游戏都已领取时推送一条通知 | 默认没有游戏被领取时不会推送通知        |

#### 如何安装python模块和浏览器

使用在线编辑器中的集成终端打开src目录，运行以下命令（点（`.`）是命令的一部分，请不要忽略它们）。

```bash
pip3 install -r requirements.txt -t .
mv bin/pyppeteer-install .
./pyppeteer-install
cp -r /root/.local/share/pyppeteer/local-chromium/*/chrome-linux .
```

运行完成后点击“部署”按钮使修改生效。

## 已知问题

Windows系统中途结束脚本可能导致浏览器进程留在后台。请检查任务管理器并手动结束浏览器进程。
