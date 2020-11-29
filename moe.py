from nonebot import on_command, CommandSession
from nonebot.message import unescape
from nonebot import on_natural_language, NLPSession, IntentCommand

import os
import random
from urllib.request import urlretrieve

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

moe_search = 'https://zh.moegirl.org.cn/index.php?search='
moe_url = 'https://zh.moegirl.org.cn/zh-cn/'
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
url_head = '\‘><a\shref="/'
url_tail = '"'
loading = '⏳Loading……'


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

#获取图片
def get_img(final_res):
    pd = '/File:'
    
    #人物类
    img_url = ''.join(re.compile('itemprop="photo"><a href="(.*?)"').findall(final_res))
    if pd not in img_url:
        #音乐类
        print('pass 1')
        img_url = ''.join(re.compile('<td colspan="1"><a href="(.*?)"').findall(final_res))
        if pd not in img_url:
            #部分游戏类
            print('pass 2')
            img_url = ''.join(re.compile('<td colspan="0"><a href="(.*?)"').findall(final_res))  
            if pd not in img_url:
                #番剧类
                print('pass 3')
                img_url = ''.join(re.compile('<td colspan="2"><a href="(.*?)"').findall(final_res))
                if pd not in img_url:
                    #物品类
                    print('pass 4')
                    img_url = ''.join(re.compile('<td colspan="2" align="center"><a href="(.*?)"').findall(final_res))
                    if pd not in img_url:
                        print('pass 5')
                        return ''

    #获取文件页
    img_url = 'https://zh.moegirl.org.cn' + img_url
    final_url = img_url
    final_res = requests.get(final_url)
    final_res = final_res.text

    #解析真实文件url
    img_url = ''.join(re.compile('id="file"><a href="(.*?)">').findall(final_res))
    print('img_url:'+img_url)

    file_path = '/home/ubuntu/nonebot/awesome/plugins/img/'+str(random.randint(0,1000))+'img.png'
    os.makedirs('/home/ubuntu/nonebot/awesome/plugins/img/', exist_ok=True)
    urlretrieve(img_url, file_path)
    return file_path

#生成发送文本
def sqawn_msg(rurl, final_res, reply, cq_img=None):
    if cq_img != None:
        txt =  reply + msg_head + '\n' + rurl + '\n' + cq_img + get_summary(final_res)
    #去除文末回车
        return txt[:-1]
    else:
        txt =  reply+ msg_head + '\n' + rurl + '\n' + get_summary(final_res)
        return txt[:-1]
##################################################################################################
#                                                                                                #
#                                            main                                                #
#                                                                                                #
##################################################################################################
@on_command('moe',aliases=('萌百'),only_to_me=False)
async def moe(session: CommandSession):
    print('start')
    msg=session.current_arg_text.strip()
    if session.is_first_run:
        await session.send(loading)
#        global msg
#        msg=session.current_arg_text.strip()
        print('第一次进入')
    #获取搜索页
        final_url = moe_search + msg
        final_res = requests.get(final_url)
        final_res = final_res.text

    #无结果处理
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
                img_path = get_img(final_res)
                reply = '[CQ:reply,id='+ str(session.ctx['user_id'])+']'
                if not img_path:
                    await session.send(sqawn_msg(rurl, final_res, reply))
                else:
                    await session.send(sqawn_msg(rurl, final_res, reply, '[CQ:image,file='+img_path+']'))
                    try:
                        os.remove(img_path)
                        print('已清除图片缓存')
                    except:
                        pass
            else:
                #搜索页,生成搜索结果列表
                listx = ''
#                global titles
                global urls

                urls = re.compile(r'\'><a href="/(.*?)"').findall(final_res)
                print('urls:'+''.join(urls))
                titles = re.compile(label_head+'.*?'+label_tail+'(.*?)'+title_tail).findall(final_res)
                for title in titles:
                    listx = listx + str(titles.index(title)) + ':'  +  re.sub(r"</?(.+?)>" or r"&(.*?);(.*?)&(.*?);","",title) + '\n'

                output = listx.replace('\"', "").replace('{',"").replace('}',"").replace(',',"")
                session.get('msg', prompt='[moe]搜索到以下内容，输入对应数字查看结果，输入其他消息自动取消搜索\n'+output)
    
    else:
        print(msg)
        try:
            int(msg)
        except ValueError:
            await session.send('取消搜索')
        else:
            await session.send(loading)
            if int(msg) in range(len(urls)):
                print('进入if')
                rurl = moe_url + urls[int(msg)]
                final_res = requests.get(rurl)
                final_res = final_res.text
                img_path = get_img(final_res)
                reply = '[CQ:reply,id='+ str(session.ctx['user_id'])+']'
                if not img_path:
                    await session.send(sqawn_msg(rurl, final_res, reply))
                else:
                    await session.send(sqawn_msg(rurl, final_res, reply, '[CQ:image,file='+img_path+']'))
                    try:
                        os.remove(img_path)
                        print('已清除图片缓存')
                    except:
                        pass
            else:
                await session.send('取消搜索')

##################################################################################################
#                                                                                                #
#                                            解析器                                              #
#                                                                                                #
##################################################################################################

@moe.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.state[session.current_key] = stripped_arg

