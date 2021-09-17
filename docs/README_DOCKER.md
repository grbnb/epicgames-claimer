# EpicGames Claimer

自动领取Epic游戏商城[每周免费游戏](https://www.epicgames.com/store/free-games)。

如果你觉得本项目对你有帮助，请star本项目。

## 快速开始

``` bash
docker run -it luminoleon/epicgames-claimer
```

登录成功后，可按下Ctrl + P + Q切换至后台运行。

## 一些示例

* 保存账号信息到本地目录(下次创建新的容器时就不需要重新登录了):

    ```bash
    docker run -it -v ~/epicgames_claimer/User_Data:/User_Data luminoleon/epicgames-claimer
    ```

* 修复容器内的时区问题:

    ```bash
    docker run -it -e TZ=<你的时区> luminoleon/epicgames-claimer
    ```

    [可用时区列表](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)

* 无交互式输入:

    ```bash
    docker run -d luminoleon/epicgames-claimer -u <你的邮箱> -p <你的密码>
    ```

    ```bash
    docker run -d luminoleon/epicgames-claimer -u <你的邮箱> -p <你的密码> -t <双重验证代码>
    ```

* 使用 docker-compose:

    首先创建`docker-compose.yml`文件，内容如下:

    ```yaml
    version: '3'

    services:

      epic-a:
          image: luminoleon/epicgames-claimer
          container_name: epic-a
          restart: unless-stopped
          environment:
            - TZ=Asia/Shanghai
            - AUTO_UPDATE=true
            - EMAIL=邮箱
            - PASSWORD=密码
      epic-b:
          image: luminoleon/epicgames-claimer
          container_name: epic-b
          restart: unless-stopped
          environment:
            - TZ=Asia/Shanghai
            - AUTO_UPDATE=true
            - EMAIL=另一个邮箱
            - PASSWORD=另一个密码
    ```

    然后执行命令:

    ```bash
    docker-compose up -d
    ```

## 环境变量

| 变量                    | 说明                  | 默认   | 备注                  |
| ----------------------- | -------------------- | ------ | -------------------- |
| TZ                      | 容器的时区, [可用时区列表](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) | Asia/Shanghai |  |
| RUN_AT                  | 指定每日运行时间      | 当前时间 | 格式：HH:MM          |
| ONCE                    | 运行一次领取过程后退出 | false   | true/false          |
| AUTO_UPDATE             | 启用自动更新          | false   | true/false          |
| EMAIL                   | 设置用户名/邮箱       |         |                     |
| PASSWORD                | 设置密码              |         |                     |
| VERIFICATION_CODE       | 设置双重验证代码      |         |                      |
| PUSH_SERVERCHAN_SENDKEY | 设置Server酱SendKey  |         |                      |

## 可选参数

注意：对应的环境变量存在时，参数的值会被对应环境变量的值覆盖。

使用方法: `docker run luminoleon/epicgames-claimer [-h] [-n] [-c CHROMIUM_PATH] [-r RUN_AT] [-o] [-a] [-u USERNAME] [-p PASSWORD] [-t VERIFICATION_CODE] [-ps PUSH_SERVERCHAN_SENDKEY]`

| 参数                               | 说明                     | 备注                      |
| ---------------------------------- | ----------------------- | ------------------------- |
| `-r`, `--run-at`                   | 指定每日运行时间         | 格式：HH:MM，默认为当前时间 |
| `-o`, `--once`                     | 运行一次领取过程后退出    |                           |
| `-a`, `--auto-update`              | 启用自动更新             |                           |
| `-u`, `--username`                 | 设置用户名/邮箱          |                           |
| `-p`, `--password`                 | 设置密码                 |                           |
| `-t`, `--verification-code`        | 设置双重验证代码          |                          |
| `-ps`, `--push-serverchan-sendkey` | 设置Server酱SendKey      |                          |
