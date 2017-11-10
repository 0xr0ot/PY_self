#coding:utf-8

import os
from NetEaseMusicApi import interact_select_song
import requests
import itchat

KEY = 'abcded5c8a101f4ca9bee7e7ba3ace0ddf'

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReply = 'I received: ' + msg['Text']
    reply = get_response(msg['Text'])
    return reply or defaultReply


# with open('stop.mp3', 'w') as f: pass
# def close_music():
#     os.startfile('stop.mp3')
# 
# @itchat.msg_register(itchat.content.TEXT)
# def music_player(msg):
#     if msg['ToUserName'] != 'filehelper': return
#     if msg['Text'] == u'关闭':
#         close_music()
#         itchat.send(u'音乐已关闭', 'filehelper')
#     if msg['Text'] == u'帮助':
#         itchat.send(u'帮助信息', 'filehelper')
#     else:
#         itchat.send(interact_select_song(msg['Text']), 'filehelper')



if __name__ == '__main__':
    itchat.auto_login(hotReload=True)#热启动
    itchat.run()
