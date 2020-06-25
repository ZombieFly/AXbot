from nonebot import on_command, CommandSession
from nonebot.message import unescape
from nonebot import on_natural_language, NLPSession, IntentCommand

import requests
import json
import chardet
import re
from pprint import pprint
import requests
import json
import chardet
import re
from pprint import pprint

from urllib.parse import quote, unquote, urlencode



@on_command('wiki',aliases=('维基'),only_to_me=False)
async def findv(session: CommandSession):
    msg=session.current_arg_text.strip()
    final_url = 'https://wiki.biligame.com/mc/'+msg	#在此处可更改为mc wiki官方源
    final_res = requests.get(final_url)
    final_res.encoding = chardet.detect(final_res.content)['encoding']
    final_res = final_res.text
    pattern = re.compile('lang="zh-Hans-CN">\n<p>(.*?)<a href=')
    data = pattern.findall(final_res)
    if data==['本页面目前没有内容。您可以在其他页面中']:
        await session.send('没有找到条目"'+msg+'"，但你可以尝试查看相关搜索结果：\n'+'https://searchwiki.biligame.com/mc/index.php?search='+quote(msg))
    else:
        pattern2 = re.compile('<p><b>(.*?)\n</p>\n<div')
        tell = pattern2.findall(final_res)

        pattern3 = re.compile('/mc(.*?)">阅读</a></li><li')
        tell1 = pattern3.findall(final_res)

        if tell==[]:
            pattern2 = re.compile('<p><b>(.*?)\n</p>')
            tell = pattern2.findall(final_res)
        tell = ''.join(tell)
        tell = re.sub(r"</?(.+?)>", "", tell)

        output='有关"'+msg+'"的搜索结果出来了喵：'+'https://wiki.biligame.com/mc'+''.join(tell1)+'\n'+tell
        await session.send(output)
