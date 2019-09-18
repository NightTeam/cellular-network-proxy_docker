FROM ubuntu:18.04

RUN \
    # 替换apt源
    echo "deb http://mirrors.ustc.edu.cn/ubuntu-ports/ bionic main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/ubuntu-ports/ bionic-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/ubuntu-ports/ bionic-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/ubuntu-ports/ bionic-security main restricted universe multiverse" >> /etc/apt/sources.list && \
    # 安装必要的软件
    apt update && \
    apt install squid python3.7 python3-pip gcc net-tools wvdial iputils-ping vim psmisc curl -y && \
    # 更换python的pip源为阿里云源
    python3.7 -m pip install pip -U && \
    python3.7 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    # 安装主控端依赖包
    python3.7 -m pip install aredis aiohttp quart && \
    # 清除apt缓存
    apt autoclean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home
COPY server.py /home
COPY squid.conf /home/squid.conf.example

CMD squid && python3.7 server.py
