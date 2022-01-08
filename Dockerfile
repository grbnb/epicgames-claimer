FROM ubuntu:18.04

LABEL maintainer="Luminoleon <luminoleon@outlook.com>"

ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Shanghai

COPY requirements.txt /

RUN apt-get update \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get install -y --no-install-recommends tzdata chromium-browser \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-idna python3-setuptools python3-pkg-resources \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apt-get purge -y python3-pip python3-setuptools \
    && apt-get autoremove -y \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY *.py /

ENTRYPOINT [ "python3", "-u", "main.py", "-c", "chromium-browser" ]
