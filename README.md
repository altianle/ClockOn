# 自动打卡

**使用前准备：**

1 安装Chrome浏览器
    
    在设置-关于Chrome中找到版本号，记录下来以下载对应webdriver

2 安装webdriver与selenium

    selenium：pip install selenium
    webdriver：https://registry.npmmirror.com/binary.html?path=chromedriver/
    需要使用chrome的对应版本，解压后放在...\Google\Chrome\Application\ 文件目录下，并把该目录放在path环境变量中

3 在config.ini中修改账号、密码

4 运行 main.py

tip：进入具体打卡页面可能会出现需要重新定位的bug，此时需要手动重新定位。
