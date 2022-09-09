# retweet_bot

可用作个人微博内容转推到 rum 种子网络。请注意，核心的 xpaths 语法，本 repo 并未提供有效数值，仅作示例。

如何部署？

1、拷贝源码

```sh
git clone https://github.com/liujuanjuan1984/retweet_bot.git
cd retweet_bot 
```

2、安装依赖

```sh
pip install -r requirements.txt
```

安装与 chrome 版本一致的 chromedriver 并把可执行文件放在系统的 PATH 目录下

3、修改配置

参考 config_private_sample.py 更新相关字段

4、retweet 转推

首次执行或有新用户时，把转推的 users 作为参数传入 retweet_users 方法，会自动映射密钥，并生成（或更新）users_private.json ，之后重复执行时无需指定 users ，会自动读取本地配置。

```py
users = {
    "https://example.com/personal_homepage": {
    "name": "somebody",
    "url": "https://example.com/personal_homepage",
    },
}
```


