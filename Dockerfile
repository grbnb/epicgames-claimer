FROM ubuntu:18.04

LABEL maintainer="Luminoleon <luminoleon@outlook.com>"

ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Shanghai

COPY requirements.txt /

RUN apt update \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt install -y tzdata \
    && apt install -y python3 python3-pip \
    && apt install -y chromium-browser \
    && pip3 install --no-cache-dir -r requirements.txt \        
    && apt purge -y python3-pip \
    && apt autoremove -y \
    && apt install -y python3-idna \
    && apt clean \
    && apt autoclean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY *.py /

ENTRYPOINT [ "python3", "-u", "main.py", "-c", "chromium-browser" ]
