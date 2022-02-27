from lxml import etree
from random import randint
import requests


# 封装图片下载方法
def downloadImage(img_list, img_url, img_name, filePath):
    # 以UTF-8编码方式打开保存的网站内容,并解析为HTML文档
    do = etree.HTML(open(filePath, encoding='utf-8').read())
    # 定位需要获取数据的html标签,装入列表以便遍历输出
    list = do.xpath(img_list)
    for img_data in list:
        # 爬取图片地址和图片名称
        url = img_data[0].xpath(img_url)
        name = img_data[0].xpath(img_name)
        # 以Cookie方式请求连接(模拟用户请求,避免网站反爬),爬取图片
        img = requests.Session().get(url[0], headers=headers)
        # 以二进制流方式将下载的图片写入文件
        with open('./img/%s.png' % name[0], 'wb') as file:
            file.write(img.content)
        # 添加提示信息
        print('%s下载成功' % name[0])


# 封装批量拼装sql语句方法
def sqlSplicing(filePath, list_name, list_con, list_price):
    # 打开手动获取的动态资源网站文件并解析
    path = filePath
    text = open(path, encoding='utf-8').read()
    do = etree.HTML(text)
    # 为sql拼接变量赋值
    name = do.xpath(list_name)
    con = do.xpath(list_con)
    price = do.xpath(list_price)
    # 修改爬取到的初始车型信息格式
    t = "".join(con).replace(' ', '').replace('\n', "").replace('车辆详情>', ',').replace('|', ' ')
    # 重新转为列表以拼接sql文件
    content = t.split(',')
    sql = 'insert into car_info(c_name,c_content,c_price,c_image,c_number,type_id,c_date) values('
    for a, b, c in zip(name, content, price):
        # 拼接sql
        newsql = sql + '\'' + a + '\',' + '\'' + b + '\',' + c + ',\'' + a + '.jpg\'' + ',' + str(
            randint(1, 20)) + ',?,\'' + '2022-02-16\');\n'
        with open('./one.sql', 'a', encoding='utf-8') as file:
            file.write(newsql)
    print('sql文件保存成功')


# 方案一(失败,无法获取动态刷新的网站内容)
# 获取请求网站地址
yihaiUrl = 'https://booking.1hai.cn/Order/BrandStep1/?from=NavBrandIndex'
# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
# 以浏览器保存的Cookie方式请求连接(局限在无法获取动态刷新的网站内容)
r = requests.Session().get(yihaiUrl, headers=headers)

# 方案二(成功,但需手动到浏览器控制台复制html信息)
# 手动获取动态刷新网站内容
filePath = 'D:\PyProject\pythonProject1\clia\\yihaiSZ.txt'
# 定位需要获取数据的html标签,装入列表以便遍历输出
img_list = '//div[@class="wraplist"]//div[@class="det-carlist"]//div[@class="licar-picinfo"]'
# 定位需爬取的图片具体位置
img_url = './@data-original'
img_name = './@alt'
# 定位需要的车型信息
list_name = '//div[@class="wraplist"]//div[@class="det-carlist"]//li[@class="licar-namebox"]//div[@class="licar-nameinfo"]//p[@class="car-nameinfo"]//span//text()'
list_con = '//div[@class="wraplist"]//div[@class="det-carlist"]//li[@class="licar-namebox"]//div[@class="licar-nameinfo"]//p[@class="car-introinfo"]//text()'
list_price = '//div[@class="wraplist"]//div[@class="det-carlist"]//li[@class="licar-info"]//div[@class="condition1"]//div[@class="carprice"]//div[@class="current-price"]//em//text()'
# 保存图片和sql
downloadImage(img_list, img_url, img_name, filePath)
sqlSplicing(filePath, list_name, list_con, list_price)
