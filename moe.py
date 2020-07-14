from nonebot import on_command, CommandSession
from nonebot.message import unescape
from nonebot import on_natural_language, NLPSession, IntentCommand

import requests
import base64
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

moe_url = 'https://zh.moegirl.org/zh-cn/'
null_head = '</p><p><span style="font-size: x-large;">'
null_tail = '</span>'
null_msg = ['这个页面没有被找到']
output_null_msg = '呼喵？没有找到该条目呢'
msg_head = '搜索结果出来了喵：'
summary_head = '\n<p>'
summary_head2 = '<p><b>'
summary_tail = '\n</p>'

def main(msg):

    final_url = moe_url + msg
    final_res = requests.get(final_url)
    final_res = final_res.text
    
    pattern = re.compile(null_head+'(.*?)'+null_tail)
    data = pattern.findall(final_res)
    if data==null_msg:
        return output_null_msg
    else:
        rurl = moe_url + quote(msg)
        data=re.compile(summary_head + '(.*?)' + summary_tail).findall(final_res)
        if data == []:
            data = re.compile(summary_head2 + '(.*?)' + summary_tail).findall(final_res)
        for text in data:
            if '是' in text and '这是一个' not in text:
                return msg_head + ''.join(rurl)+ '\n' + re.sub(r"</?(.+?)>" or r"&(.*?);(.*?)&(.*?);","",text).replace('&#160;',' ')

@on_command('moe',aliases=('萌百'),only_to_me=False)
async def moe(session: CommandSession):
    msg=session.current_arg_text.strip()
    await session.send(main(msg))
