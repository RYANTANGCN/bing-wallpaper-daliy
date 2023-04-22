import requests
import telegram
import logging
import time
import configparser

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("info.log"),
        logging.StreamHandler()
    ]
)

file = 'config.ini'

# 创建配置文件对象
con = configparser.ConfigParser()

# 读取文件
con.read(file, encoding='utf-8')

# 获取所有section
config = dict(con.items('default'))
location = config['download_location']

base_url = "https://www.bing.com/"
download_url = "https://www.bing.com/hpwp/"
api_url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1612409408851&pid=hp&FORM=BEHPTB&uhd=1" \
          "&uhdwidth=3840&uhdheight=2160 "

r = requests.get(api_url)
image = r.json()["images"][0]
copyright = image["copyright"]
startdate = image["startdate"]
title = image['title']
wallpaper_file_name = startdate + '_' + title.replace(" ", "_") + '.jpeg'
logging.info('file_name:%s', wallpaper_file_name)

# 获取hash
hsh = image["hsh"]
# 获得图片预览链接
img_pc_url = base_url + image["url"]
# 获取原图下载地址
img_pc_download_url = download_url + hsh
# 拼接本地下载地址
imgPcLocation = location + hsh
# Markdown内容
caption = '[' + copyright + '](' + img_pc_url + ')'

logging.info('img_pc_url:%s', img_pc_url)
logging.info('img_pc_download_url:%s', img_pc_download_url)

# 开始请求下载图片
img_response = requests.get(img_pc_url)
img_pc = img_response.content
# 获得文件名
filename = "BingWallpaper-" + time.strftime("%Y-%m-%d", time.localtime()) + ".jpg"
img_pc_location = location + wallpaper_file_name

# 保存到本地
with open(img_pc_location, 'wb+') as img:
    img.write(img_pc)

with open(location + 'pc.jpg', 'wb+') as img:
    img.write(img_pc)

# 发送到telegram
telegram.send_photo(img_pc_location, caption)
# Telegram.sendDocument(imgMbLocation)
# Telegram.send_message(imgPcUrl, copyright)
# Telegram.sendDocument(imgPcLocation)

logging.info("success!")
