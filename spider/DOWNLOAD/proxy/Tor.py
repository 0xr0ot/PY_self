# Method_1
import socks
import socket
import requests

socks.set_default_proxy(socks.SOCKS5,'localhost',9150)
socket.socket = socks.socksocket
print(requests.get('http://icanhazip.com').text)

# Method_2
from selenium import webdriver

service_args = ['--proxy=localhost:9150', '--proxy-type=socks5']
driver = webdriver.PhantomJS(executable_path='<path to PhantomJS>',service_args=service_args)
driver.get('http://icanhazip.com')
print(driver.page_source)
driver.close()
