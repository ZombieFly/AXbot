# 如何使用AXbot？
AXbot是一个基于Nonebot开发的机器人，故在使用本机器人之前，你需要先安装并配置好Nonebot，及其前置配置。
随后将这些python文件放入你的``plugins``文件夹中，注意，此时你的放置nonebot主程序的文件夹结构应该大致如下<br>
nonebot  
&#160;├── awesome  
&#160;&#160;│└── plugins  
&#160;&#160;|&#160;&#160;&#160;&#160;&#160;&#160;&#160;├── mws.py  
&#160;&#160;│&#160;&#160;&#160;&#160;&#160;&#160;&#160;└── moe.py  
&#160;├── bot.py  
&#160;└── config.py  
# 模块功能
## mws.py:
  <中文Minecraft Wiki搜索引擎模块><br>
 	采用双源搜索：<br>
### 源站点：
minecraft-zh.gamepedia.com<br>
      使用语法：``gpwiki [搜索内容]``<br>
      实例：``gpwiki 末影龙``<br>
### bili镜像：
wiki.biligame.com/mc<br>
使用语法：``wiki [搜索内容]``<br>
      举例：``wiki 末影龙``<br>

## moe.py:
  <萌娘百科搜索引擎模块><br>
  站点：zh.moegirl.org<br>
    使用语法：``moe [搜索内容]``<br>
    举例：``moe 初音ミク``<br>
    二级命令处理：输入需要查看的搜索结果标号，自动返回对应页面url与简介（如果可以获得），发送其他消息自动关闭对话

