---
title: 云服务器上使用Docker部署代理
date: 2025-08-08 22:17:50
---
#### 参考链接
- [Docker配置文件](https://github.com/metacubex/metacubexd)
- [ghcr.io代理](https://docker.aityp.com/)
- [地址文件下载](https://github.com/Loyalsoldier/geoip/releases/tag/202508070023)

#### 部署过程
创建docker-compose.yml文件
```yml
version: '3'

services:
  metacubexd:
    container_name: metacubexd
    image: ghcr.io/metacubex/metacubexd # 此处仅配置docker镜像不能加速，可以使用ghcr.io代理
    restart: always
    ports:
      - '80:80'

  # optional
  meta:
    container_name: meta
    image: docker.io/metacubex/mihomo:Alpha
    restart: always
    pid: host
    ipc: host
    network_mode: host
    cap_add:
      - ALL
    volumes:
      - ./config.yaml:/root/.config/mihomo
      - /dev/net/tun:/dev/net/tun
```

mihomo内核缺少MMDB文件启动时会报错, 需要自行下载放到config文件夹:
```shell
clash_core_meta  | time="2025-08-08T08:11:01.716765387Z" level=info msg="Start initial configuration in progress"
clash_core_meta  | time="2025-08-08T08:11:01.764156792Z" level=info msg="Geodata Loader mode: memconservative"
clash_core_meta  | time="2025-08-08T08:11:01.764196046Z" level=info msg="Geosite Matcher implementation: succinct"
clash_core_meta  | time="2025-08-08T08:11:01.777027228Z" level=warning msg="MMDB invalid, remove and download"
clash_core_meta  | time="2025-08-08T08:12:31.783026266Z" level=error msg="can't initial GeoIP: can't download MMDB: context deadline exceeded"
```

打开暴露的端口进入连接页面，后端地址位公网ip+9090端口，secret为设置的密钥
![连接页面](https://pub-3809a824eb8b4c2ebf27716c5f100aa2.r2.dev/Snipaste_2025-08-08_20-25-00.png)

登录成功
![登录成功](https://pub-3809a824eb8b4c2ebf27716c5f100aa2.r2.dev/Snipaste_2025-08-08_20-25-15.png)