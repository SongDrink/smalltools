from bs4 import BeautifulSoup
import urllib3
import re
import time
pic_path = 'D:/Users/Drink/Pictures/Camera Roll/'
url = "https://wallhaven.cc/hot?page="
http = urllib3.PoolManager()

name = 1

for i in range(0,20):
    # 建立和wallhaven的连接
    contents = http.request('GET',url + str(name))
    print("content 获取成功\n")
    data = contents.data

    # 建立解析式soup
    soup = BeautifulSoup(data,'lxml')
    print("soup 建立成功过\n")

    # 从pic_list中寻找图片链接
    pic_list = soup.find_all('li')

    # 待处理
    print("全局url 成功")
    for _ in range(20,len(pic_list)):
        a = pic_list[_]
        try:
            b = re.search('href=".{0,100}"',str(a)).group().split('"')
            url_pic = b[1]
            pic_download = http.request('GET', url_pic)
            # print(pic_download.data)
            soup_pic = BeautifulSoup(pic_download.data,'lxml')

            download_url_list = soup_pic.find_all('div',class_="scrollbox")
            download_url_full = str(download_url_list)
            download_url = re.search('data-cfsrc=".{0,100}"',download_url_full)
            try:
                true_pic_url = download_url.group().split('"')[1]
                pic_name = true_pic_url.split('/')[-1]
                r = http.request('GET', true_pic_url, preload_content=False)
                path = pic_path + pic_name
                with open(path, 'wb') as out:
                    out.write(r.data)
                print(path," 保存成功")
                r.release_conn()
            except:
                pass
            time.sleep(2)
        except:
            pass
    print("第",name,"页 下载完成")
    name += 1
print('保存完成')
