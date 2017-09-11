headers_get_tk = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'i.umeng.com',
    'Upgrade-Insecure-Requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
}

headers_login = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.8',
    'content-length': '111', #TODO
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://i.umeng.com',
    'referer': 'https://i.umeng.com/?',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest' #TODO
}

headers_get_csrf = {
    'Host': 'mobile.umeng.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',  # TODO
    'Upgrade-Insecure-Requests': '1',  # TODO
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://mobile.umeng.com/analytics',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

cookie_app = ''
cookie_channel = ''
