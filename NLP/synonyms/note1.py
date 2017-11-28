# coding:utf-8

import synonyms # V1.9 Error

sen1='直播斗鱼创始人力量平台五粮液致敬游戏用户量人物周刊'
sen2='直播斗鱼力量平台创始人游戏用户量人物周刊五粮液领域'

score =synonyms.compare(sen1,sen2,seg=True)
print(score)

print(synonyms.nearby('直播'))
