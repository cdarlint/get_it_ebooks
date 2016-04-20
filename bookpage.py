import requests
from lxml import html
class bookpage:
    par = {'repost': '/html/body/table/tr/td/div/h4',
           'title': '//h1',
           'desc': '//span[@itemprop="description"]',
           'publisher': '//table//table//table[1]/tr[2]/td[2]',
           'author': '//table//table//table[1]/tr[3]/td[2]/b[2]',
           'isbn': '//table//table//table[1]/tr[4]/td[2]/b',
           'year': '//table//table//table[1]/tr[5]/td[2]/b',
           'pages': '//table//table//table[1]/tr[6]/td[2]/b',
           'lang': '//table//table//table[1]/tr[7]/td[2]/b',
           'size': '//table//table//table[1]/tr[8]/td[2]/b',
           'format': '//table//table//table[1]/tr[9]/td[2]/b',
           'link_down': '//table//table//table[1]/tr[11]/td[2]/a',
           'link_buy': '//table//table//table[1]/tr[13]/td[2]/a',
           'link_rel_1': '//table//table//table//table/tr[1]/td[1]/a[2]',
           'link_rel_2': '//table//table//table//table/tr[1]/td[2]/a[2]',
           'link_rel_3': '//table//table//table//table/tr[1]/td[3]/a[2]',}
    parkeys = par.keys()
    repost_detail_status = {'[repost]': 1, '[Early Release]': 2}
    def __init__(self,pageid):
        if isinstance(pageid,int):
            self.pageid=str(pageid)
        else:
            self.pageid=pageid
    def ppage(self):
        print(self.pageid)
        print(self.pageinfo)
    def req_page(self):
        nid=self.pageid
        r = requests.get('http://it-ebooks.info/book/' + nid + '/')
        if r.url.endswith('/404/'):
            self.pageinfo=None
            return None
        h = html.fromstring(r.content)
        info = {}
        for key in self.parkeys:
            # print(key)
            key_get = h.xpath(self.par[key])
            if len(key_get) >= 1:
                if key.startswith('link'):
                    info_cur = key_get[0].attrib['href']
                    if key.startswith('link_rel'):
                        info_cur = info_cur.split('/')[2]
                elif key == 'repost':
                    rp_text = key_get[0].text
                    if rp_text in self.repost_detail_status:
                        info_cur = self.repost_detail_status[rp_text]
                    else:
                        print('new repost status: ', rp_text)
                        info_cur = 99
                else:
                    info_cur = key_get[0].text_content()
                    if key.startswith('desc'):
                        info_cur = info_cur.replace('\r\n\r\n', '\r\n')
            else:
                if key == 'repost':
                    info_cur = 0
                elif key.startswith('link_rel'):
                    info_cur = ''
                else:
                    print(key)
                    print(self.par[key])
                    raise BaseException('no content')
            info.update({key: info_cur})
        info.update({'id': nid})
        sql_key = list(info.keys())
        self.pageinfo=info