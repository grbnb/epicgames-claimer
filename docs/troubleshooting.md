# 疑难解答

- [疑难解答](#疑难解答)
  - [Browser closed unexpectedly](#browser-closed-unexpectedly)
  - [运行Python脚本在小内存或ARM设备上](#运行python脚本在小内存或arm设备上)
  - [Debian 10运行出现RequestsDependencyWarning](#debian-10运行出现requestsdependencywarning)
  - [参数`--once`或环境变量`ONCE`的具体含义，应在什么情况下使用](#参数--once或环境变量once的具体含义应在什么情况下使用)
  - [Docker容器频繁重启和执行领取过程](#docker容器频繁重启和执行领取过程)

## Browser closed unexpectedly

你可以尝试使用Google Chrome替代默认的Chromium浏览器。这或许可以解决问题（参考[Chrome headless doesn't launch on UNIX](https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#chrome-headless-doesnt-launch-on-unix)）。

1. 安装Google Chrome (AMD64)

    * Debian (e.g. Ubuntu)

        ``` bash
        curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        sudo apt install -y ./google-chrome-stable_current_amd64.deb
        rm google-chrome-stable_current_amd64.deb
        ```

    * CentOS

        ``` bash
        curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
        sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
        rm -I google-chrome-stable_current_x86_64.rpm
        ```

2. 设置浏览器可执行文件

    ``` bash
    python3 main.py --chromium-path /usr/bin/google-chrome
    ```

## 运行Python脚本在小内存或ARM设备上

1. 安装Chromium

    * Debian (e.g. Ubuntu)

        ``` bash
        sudo apt install chromium-browser
        ```

    * CentOS

        ``` bash
        sudo yum install -y epel-release
        sudo yum install -y chromium
        ```

2. 设置浏览器可执行文件

    ``` bash
    python3 main.py --chromium-path chromium-browser
    ```

## Debian 10运行出现RequestsDependencyWarning

requests模块对urllib3和chardet有版本要求。安装正确版本的urllib3和chardet可以解决此问题。

解决方法：

```bash
pip3 install urllib3==1.21.1 chardet==3.0.2
```

## 参数`--once`或环境变量`ONCE`的具体含义，应在什么情况下使用

当添加`--once`参数或者设置环境变量`ONCE=true`时，脚本或容器将在执行一次领取过程后退出，并且不会再次运行。不加该参数或设置此环境变量为`false`时，脚本或容器会在启动时执行一次领取过程，之后脚本不会退出，而是占用极少资源保持调度器持续运行，之后脚本或容器就会在固定的时间执行领取过程。

如果需要测试运行效果，或是通过其他方式实现定时运行，则需要添加参数`--once`，或设置环境变量`ONCE=true`。

## Docker容器频繁重启和执行领取过程

在设置容器环境变量`ONCE=true`时，不要将容器参数`--restart`设为`always`或者`unless-stop`。因为前者会使容器运行一次领取过程后停止，后者会在容器停止运行后重新启动容器，而容器在每次启动后都会立即执行一次领取过程，导致持续占用硬件资源。
