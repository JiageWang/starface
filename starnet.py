import os
import time
import random
import requests
from lxml import etree

first_num = random.randint(55, 62)
third_num = random.randint(0, 3200)
fourth_num = random.randint(0, 140)

os_type = [
    '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
    '(Macintosh; Intel Mac OS X 10_12_6)'
]

chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)


def get_ua():
    global os_type, chrome_version
    return ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                     '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                    )

headers_index = {
    "Host": "www.mingxing.com",
}
headers_img = {
    "Referer": "http://www.mingxing.com/ziliao/index.html",
}




root = 'starImages'
if not os.path.exists(root):
    os.makedirs(root)
s = requests.session()
for i in range(1, 194):
    url = r'http://www.mingxing.com/ziliao/index?&p={}'.format(i)
    headers_index['User-Agent'] = get_ua()
    response = s.get(url, headers=headers_index)
    html = etree.HTML(response.text)
    lis = html.xpath("//div[@class='page_starlist']//li")
    time.sleep(1)

    for li in lis:
        src = li.xpath(".//img/@src")[0]
        name = li.xpath(".//a/h3")[0].text.strip()
        print('Downloading {}'.format(name))

        headers_img['Referer'] = url
        headers_img['User-Agent'] = get_ua()
        img = s.get(src, headers=headers_img)
        folder = os.path.join(root, name)
        if not os.path.exists(folder):
            os.mkdir(folder)
        file = os.path.join(root, name, '{}.jpg'.format(name))
        with open(file, 'ab') as f:
            f.write(img.content)
        # time.sleep(0.2)
        img.close()
