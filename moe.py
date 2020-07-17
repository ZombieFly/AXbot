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

moe_search = 'https://zh.moegirl.org/index.php?search='
moe_url = 'https://zh.moegirl.org/zh-cn/'
null_head = '<p class="mw-search-nonefound">\n'
null_tail = '</p>'
null_msg = ['找不到和查询相匹配的结果。']
output_null_msg = '[moe]呼喵？没有找到该条目呢'
msg_head = '[moe]搜索结果出来了喵：'
summary_head = '\n<p>'
summary_head2 = '<p><b>'
summary_tail = '\n</p>'
label_head = 'data-serp-pos="'
label_tail = '">'
title_tail = '</a>'

##################################################################################################
#                                                                                                #
#                                            函数声明                                            #
#                                                                                                #
##################################################################################################


#简介获取
def get_summary(final_res):
    data=re.compile(summary_head + '(.*?)' + summary_tail).findall(final_res)
    if not data:
        data = re.compile(summary_head2 + '(.*?)' + summary_tail).findall(final_res)
    for text in data:
        if '是' in text and '这是一个' not in text:
            return ''.join(re.sub(r"</?(.+?)>" or r"&(.*?);(.*?)&(.*?);","",text)).replace('&#160;',"")
    return ''

##################################################################################################
#                                                                                                #
#                                            main                                                #
#                                                                                                #
##################################################################################################
@on_command('moe',aliases=('萌百'),only_to_me=False)
async def moe(session: CommandSession):
    #获取参数
    #首次进入获取关键词
    #第二次进入获取用户输入标号
    msg=session.current_arg_text.strip()
    if session.is_first_run:
        #第一次进入会话
        await session.send(' ⏳')
        #获取搜索页
        final_url = moe_search + msg
        final_res = requests.get(final_url)
        final_res = final_res.text

        #无对应页面及相关结果处理
        pattern = re.compile(null_head+'(.*?)'+null_tail)
        data = pattern.findall(final_res)
        if data == null_msg:
            await session.send(output_null_msg)
        else:
            #判断是否为搜索页
            pattern = re.compile('搜索结果(.*?)百科全书')
            data = pattern.findall(final_res)
            print(data)
            if not data:
                #常规页面
                rurl = moe_url + quote(msg)
                await session.send(msg_head + rurl + '\n' + get_summary(final_res))
            else:
                #搜索页,生成搜索结果列表
                listx = ''
                #继承到下一次进入会话
                global titles
                global urls
                #获取搜索结果对应url
                urls = re.compile(r'\'><a href="/(.*?)"').findall(final_res)
                #获取搜搜结果标题名称
                titles = re.compile(label_head+'.*?'+label_tail+'(.*?)'+title_tail).findall(final_res)
                #格式化
                for title in titles:
                    listx = listx + str(titles.index(title)) + ':'  +  re.sub(r"</?(.+?)>" or r"&(.*?);(.*?)&(.*?);","",title) + '\n'

                output = listx.replace('\"', "").replace('{',"").replace('}',"").replace(',',"")
                #获取选择搜索结果标号
                session.get('msg', prompt='[moe]搜索到以下内容，输入对应数字查看结果，输入其他消息自动取消搜索\n'+output)

    else:
        #判断输入合法性
        try:
            int(msg)
        except ValueError:
            await session.send('取消搜索')
        else:
            await session.send(' ⏳')
            if int(msg) in range(len(titles)):
                #根据下标取url
                final_url = moe_url + titles[int(msg)]
                final_res = requests.get(final_url)
                final_res = final_res.text
                await session.send(msg_head + moe_url + urls[int(msg)] + '\n' + get_summary(final_res))
            else:
                #非范围内标号
                await session.send('取消搜索')

##################################################################################################
#                                                                                                #
#                                            解析器                                              #
#                                                                                                #
##################################################################################################

@moe.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
#    stripped_arg = session.current_arg_text.strip()
    session.state[session.current_key] = stripped_arg
