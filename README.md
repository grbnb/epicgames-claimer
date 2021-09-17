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

<!-- 注意：Windows版本目前不支持自动更新。 -->

#### Windows版本可选参数

| 参数                               | 说明                     | 备注                      |
| ---------------------------------- | ----------------------- | ------------------------- |
| `-n`, `--no-headless`              | 显示浏览器的图形界面      |                           |
| `-c`, `--chromium-path`            | 指定浏览器可执行文件路径  |                           |
| `-r`, `--run-at`                   | 指定每日运行时间         | 格式：HH:MM，默认为当前时间 |
| `-o`, `--once`                     | 运行一次领取过程后退出    |                           |
| `-u`, `--username`                 | 设置用户名/邮箱          |                           |
| `-p`, `--password`                 | 设置密码                 |                           |
| `-t`, `--verification-code`        | 设置双重验证代码          |                          |
| `-ps`, `--push-serverchan-sendkey` | 设置Server酱SendKey      |                          |

### Docker

``` bash
docker run -it luminoleon/epicgames-claimer
```

更多使用方法见[Docker hub页面](https://hub.docker.com/r/luminoleon/epicgames-claimer)。

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

    <!--
    <details>
    <summary>启用自动更新</summary>

    ```bash
    python3 main.py --auto-update
    ```

    </details>
    -->

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
    <summary>添加Server酱通知推送</summary>

    ```bash
    python3 main.py -ps <SendKey>
    ```

    </details>

#### Python版本可选参数

| 参数                               | 说明                     | 备注                      |
| ---------------------------------- | ----------------------- | ------------------------- |
| `-n`, `--no-headless`              | 显示浏览器的图形界面      |                           |
| `-c`, `--chromium-path`            | 指定浏览器可执行文件路径  |                           |
| `-r`, `--run-at`                   | 指定每日运行时间         | 格式：HH:MM，默认为当前时间 |
| `-o`, `--once`                     | 运行一次领取过程后退出    |                           |
| `-u`, `--username`                 | 设置用户名/邮箱          |                           |
| `-p`, `--password`                 | 设置密码                 |                           |
| `-t`, `--verification-code`        | 设置双重验证代码          |                          |
| `-ps`, `--push-serverchan-sendkey` | 设置Server酱SendKey      |                          |
<!-- | `-a`, `--auto-update`              | 启用自动更新             |                           | -->

## 已知问题

Windows系统中途结束脚本可能导致浏览器进程留在后台。请检查任务管理器并手动结束浏览器进程。
