FROM ubuntu:18.04

RUN \
    # 替换apt源
    echo "deb http://mirrors.ustc.edu.cn/ubuntu-ports/ bionic main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/ubuntu-ports/ bionic-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/ubuntu-ports/ bionic-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/ubuntu-ports/ bionic-security main restricted universe multiverse" >> /etc/apt/sources.list && \
    # 安装必要的软件
    apt update && \
    apt install tinyproxy ppp net-tools iputils-ping vim psmisc -y && \
    # 将设定路由和DNS的脚本写入/etc/ppp/ip-up脚本中 这个脚本会在每次拨号时自动运行
    echo "route del -net 0.0.0.0 eth0" >> /etc/ppp/ip-up && \
    echo "route add -net 0.0.0.0 ppp0" >> /etc/ppp/ip-up && \
    echo "echo 'nameserver 127.0.0.11' > /etc/resolv.conf" >> /etc/ppp/ip-up && \
    echo "echo 'options ndots:0' >> /etc/resolv.conf" >> /etc/ppp/ip-up && \
    echo "echo 'nameserver 223.5.5.5' >> /etc/resolv.conf" >> /etc/ppp/ip-up && \
    echo "echo 'nameserver 223.6.6.6' >> /etc/resolv.conf" >> /etc/ppp/ip-up && \
    # 安装被控端依赖包
    apt install python3 python3-pip -y && \
    # 安装被控端依赖包
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple flask redis requests && \
    # 清除apt缓存
    apt autoclean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home
COPY quectel-pppd.sh /home
COPY quectel-ppp-kill.sh /home
RUN chmod +x ./quectel-pppd.sh && chmod +x ./quectel-ppp-kill.sh
COPY server.py /home
COPY tinyproxy.conf /etc/tinyproxy/tinyproxy.conf

CMD python3 server.py
