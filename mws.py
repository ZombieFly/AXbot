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



bili_url = 'https://wiki.biligame.com/mc/'
bili_null_head = 'lang="zh-Hans-CN">\n<p>'
bili_null_tail = '<a href='
bili_null_msg = ['本页面目前没有内容。您可以在其他页面中']

gpd_url = 'https://minecraft-zh.gamepedia.com/'
gpd_null_head = 'action=edit">'
gpd_null_tail = '</a>，<b>请注意</b>：'
gpd_null_msg = ['创建本页面']
gpd_output_first = '此模式下需要数十秒的时间请求数据，请耐心等待'

null_msg = '呼喵？没有找到该条目呢'
msg_head = '搜索结果出来了喵：'
summary_head = '</div>\n<p><b>'
summary_head2 = '</table>\n<p><b>'
summary_tail = '\n</p>\n'


#bili镜像

def bili(msg):
    final_url = bili_url+msg
    final_res = requests.get(final_url)
    final_res.encoding = chardet.detect(final_res.content)['encoding']
    final_res = final_res.text

    pattern = re.compile(bili_null_head + '(.*?)' + bili_null_tail)
    data = pattern.findall(final_res)

    #判断是否有该页面
    if data==bili_null_msg:
        print(null_msg)
    else:
        #获取简介
        bl_summary = re.sub(r"</?(.+?)>", "", ''.join(re.compile(summary_head + '(.*?)' + summary_tail).findall(final_res)))
        if bl_summary == '':
            bl_summary = re.sub(r"</?(.+?)>", "", ''.join(re.compile(summary_head2 + '(.*?)' + summary_tail).findall(final_res)))
        #获取url
        bltail_url = re.compile('/mc/(.*?)">阅读</a></li><li').findall(final_res)  
        #拼接最后消息
        return msg_head + bili_url + ''.join(bltail_url) + '\n' + bl_summary



#源站点

def gpd(msg):
    final_url = gpd_url + msg
    final_res = requests.get(final_url)
    final_res.encoding = chardet.detect(final_res.content)['encoding']
    final_res = final_res.text
    
    pattern = re.compile(gpd_null_head+'(.*?)'+gpd_null_tail)
    data = pattern.findall(final_res)
    
    if data==gpd_null_msg:
        print(null_msg)
    else:

        gpd_summary = re.sub(r"</?(.+?)>", "", ''.join(re.compile(summary_head + '(.*?)' + summary_tail).findall(final_res)))
        if gpd_summary == []:
            gpd_summary = re.sub(r"</?(.+?)>", "", ''.join(re.compile(summary_head2 + '(.*?)' + summary_tail).findall(final_res)))
        
        gpd_rurl = re.compile('<meta property="og:url" content="(.*?)"/>').findall(final_res)  
        
        return msg_head + ''.join(gpd_rurl) + '\n' + gpd_summary

#获取参数
def process_pt(msg):
    pattern = re.compile('(.*?)!')
    parameter = pattern.findall(msg)
    if parameter != [] and parameter[0]=='':
        parameter = parameter[1:]
    return parameter

@on_command('wiki',aliases=('维基'),only_to_me=False)
async def findv(session: CommandSession):
    msg=session.current_arg_text.strip()
    if 'gp' in process_pt(msg):
        await session.send(output)
        output='[gp]'+gpd(re.sub(r"(.+?)!", "", msg))
    else:
        output=bili(msg)
    await session.send(output)
