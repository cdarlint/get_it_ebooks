# -*- encoding: utf8 -*-
# __author__ = 'cdarling'
import requests
from lxml import html
#r=requests.get('http://ctext.org/huangdi-neijing/shang-gu-tian-zhen-lun/zhs')
#h=html.fromstring(r.content)
#f=open('ctm_contents.html','rb')
#rc=f.read()
#f.close()

def parse_single_page(rc):
    h=html.fromstring(rc)
    x=h.xpath('//*[@id="content3"]//h2')
    # print(len(x))
    # print(x[0].text)
    tt=x[0].text
    x=h.xpath('//*[starts-with(@id,"n8")]/td[3]')
    print(len(x))
    g=[[v for v in x[u].itertext()][1] for u in range(len(x))]
    return [tt]+g

f=open('ctm_content_href.txt','rb')
content_list=f.readlines()
f.close()
f_out=open('ctm_full.txt','wb')
for url_txt in content_list:
    url_full='http://ctext.org/'+url_txt.decode('ascii').strip()
    print(url_full)
    r=requests.get(url_full)
    page=parse_single_page(r.content)
    page=[(v+'\r\n').encode('utf8') for v in page]
    f_out.writelines(page)
    f_out.flush()
f_out.close()