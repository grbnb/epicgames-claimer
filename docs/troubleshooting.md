# 疑难解答

* [Browser closed unexpectedly](#browser-closed-unexpectedly)
* [运行Python脚本在小内存或ARM设备上](#运行python脚本在小内存或arm设备上)
* [Debian 10运行出现RequestsDependencyWarning](#debian-10运行出现requestsdependencywarning)

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
