import requests
from lxml import etree
import base64
def encode_to_base64(input_string):
    # 将字符串编码为字节
    byte_string = input_string.encode('utf-8')

    # 使用base64编码
    base64_bytes = base64.b64encode(byte_string)

    # 将编码结果转换为字符串
    base64_string = base64_bytes.decode('utf-8')

    return base64_string

def delete_http(x):
    x = x.replace("http://", "")
    x = x.replace("https://", "")
    return x
def check_gov(http):
    if "gov" in http:
        return True
page = 1
# proxy_ip = "http://ip:port"
# proxies = {"http":proxy_ip}
num = int(input("爬取页数，最多6页，请输入页数："))
fofa_search = input("fofa语法：")
select_code = int(input("输入1为去除http头，输入2保留http头,清输入选择："))
fofa_search = encode_to_base64(fofa_search)
print(F"fofabase64_encode::{fofa_search}")
name = input("输入文件名：")
while page<=num :
    url = F"https://fofa.info/result?qbase64={fofa_search}&page={page}&page_size=10"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        # "Cookie":"cookie"
    }
    resp = requests.get(url=url, headers=headers)
    html = etree.HTML(resp.text)
    result = html.xpath("/html//span[@class='hsxa-host']/a/@href")
    if len(result)>0:
        with open(name, "a", encoding="UTF-8") as f:
            for item in result:
                if check_gov(item):
                    print("去除gov成功")
                elif select_code == 1:
                    item = delete_http(item)
                    f.write(item)
                    f.write("\n")
                else:
                    f.write(item)
                    f.write("\n")
        print(F"下载第{page}页成功")
    else:
        print(F"第{page}页数据长度{len(result)},下载失败,原因可能是cookie过期,ip被ban")
    page += 1
print(F"下载完成")
resp.close()



