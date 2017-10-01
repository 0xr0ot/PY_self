#coding:utf-8

import re
import requests
from urllib.parse import quote
import execjs


class google():
    def get_tkk(self):
        self.host = 'https://translate.google.cn'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        res = requests.get(self.host, headers=self.headers)

        RE_TKK = re.compile(r'''TKK=eval\(\'\(\(function\(\)\{(.+?)\}\)\(\)\)\'\);''')
        code = RE_TKK.search(res.text).group(0).encode().decode('unicode-escape')
        #print(code)
        runjs = execjs.get()
        tkk = runjs.eval(code[10:-3])
        return tkk


    # def rshift(self,val, n):
    #     """python port for '>>>'(right shift with padding)
    #     """
    #     return (val % 0x100000000) >> n


    def _xr(self, a, b):
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if 'a' <= d else int(d)
            #d = google.rshift(self,a, d) if '+' == b[c + 1] else a << d
            d = (a % 0x100000000) >> d if '+' == b[c + 1] else a << d
            a = a + d & 4294967295 if '+' == b[c] else a ^ d

            c += 3
        return a


    def acquire(self, text, tkk):#引用, thanks "ssut".
        #tkk = google.get_tkk(self)
        b = tkk if tkk != '0' else ''
        d = b.split('.')
        b = int(d[0]) if len(d) > 1 else 0

        # assume e means char code array
        e = []
        g = 0
        size = len(text)
        for i, char in enumerate(text):
            l = ord(char)
            # just append if l is less than 128(ascii: DEL)
            if l < 128:
                e.append(l)
            # append calculated value if l is less than 2048
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    # append calculated value if l matches special condition
                    if (l & 64512) == 55296 and g + 1 < size and \
                                            ord(text[g + 1]) & 64512 == 56320:
                        g += 1
                        l = 65536 + ((l & 1023) << 10) + ord(text[g]) & 1023
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                        e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
        a = b
        for i, value in enumerate(e):
            a += value
            a = self._xr(a, '+-a^+6')
        a = self._xr(a, '+-3^+b+-f')
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:  # pragma: nocover
            a = (a & 2147483647) + 2147483648

        a %= 1000000  # int(1E6)
        return '{}.{}'.format(a, a ^ b)


    def translate(self,eng_txt,TK,aim='EN_to_CN'):
        QQ = quote(eng_txt)
        if aim == 'EN_to_CN':
            url = ('https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md'
                  + '&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=bh&ssel=0&tsel=0&kc=1&tk=' + str(TK) + '&q=' + QQ)
        elif aim == 'CN_to_EN':
            ruler = '&sl=zh-CN&tl=en'
            url = ('https://translate.google.cn/translate_a/single?client=t'+ruler+'&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md'
                  + '&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=bh&ssel=0&tsel=0&kc=1&tk=' + str(TK) + '&q=' + QQ)
        else:
            print('作者(UlionTse): 出错了吧，只提供英汉翻译! 翻译模式"aim"只有"EN_to_CN" or "CN_to_EN"两种,如果有必要，请自行添加和修改代码。')
            url = ''

        headers = {'Accept': '*/*',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'accept-encoding': 'gzip, deflate, sdch, br',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
                   'dnt': '1',
                   'referer': 'https://translate.google.cn/',
                   'x-client-data': 'CJK2yQEIprbJAQjEtskBCPqcygEIqZ3KAQ=='
            }
        session = requests.Session()
        res = session.get(url, headers=headers)
        data = res.json()
        
        result = ''
        for dt in data[0]:
            if dt[0]:
                result += dt[0]
        session.close()
        return result


def main(text,aim='EN_to_CN'):
    api = google()
    tkk = api.get_tkk()
    TK = api.acquire(text,tkk)
    result = api.translate(text,TK,aim=aim)
    print(result)


if __name__ == '__main__':
    #text = input(r'''Need translate EN_to_CN: ''')
    text1 = 'Hello, I\'m UlionTse. Today I repaired the question which translate first sentence only.'
    text2 = '2017年10月1日完善了代码。哈哈，你知道1+2=？'
    main(text1)
    main(text2,aim="CN_to_E")#please repair the "aim".
#END
