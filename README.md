# 4G代理服务器搭建【Docker版】

#### 温馨提示

如需用于生产环境，请参考本搭建方式的思路、结合自身业务环境调整。

本项目为「**NightTeam** 」成员 **Loco** 的原创文章《[Docker竟然还能这么玩？商业级4G代理搭建实战！](https://mp.weixin.qq.com/s/YHLko6nw3AcPEaU_H15esQ)》配套内容，如有相关问题，可在公众号「**NightTeam** 」上发消息联系，也可发送邮件至 contact@nightteam.cn，我们会尽快回复你。

欢迎关注微信公众号「**NightTeam** 」，更多高质量原创文章都在这里。

![扫码关注公众号](https://i.loli.net/2019/09/18/hyxgIA2i5B3d6Ol.jpg)

#### 使用方法

运行 `run.sh` 即可启动

内部启动流程：

1. `generate_docker_compose.py` 检测 ttyUSB 设备
2. 使用 `ls /dev/ttyUSB*` 命令获取 ttyUSB设备列表
3. 计算出 ttyUSB 设备的数量和每个 ttyUSB 设备的第四个通信接口
4. 使用 `jinja2` 的模板生成器，生成一个 `docker-compose` 文件
5. 使用 `docker-compose up -d` 命令启动“集群”
6. `master` 和 `replica` 容器启动
7. `replica` 容器向集群内的 Redis 中写入一个自身容器名的值
8. `replica` 容器运行拨号脚本，拨号成功后启动 TinyProxy，并向 Redis 中写入一个启动成功的信息
9. `replica` 容器调用 `master` 容器的刷新 Squid 配置文件接口
10. `master` 容器收到刷新 Squid 配置请求后，将已启动成功的 `replica` 容器的代理服务器地址写入 Squid 配置文件中
11. 刷新完配置文件后，就可以使用了

#### 免责声明

本项目仅为实现基本功能的样例，不对长时间运行的稳定性、可靠性做任何保证，**对使用本项目的思路、代码、内容后产生的任何后果概不负责**，请勿用于违法用途。