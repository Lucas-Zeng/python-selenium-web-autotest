import json
import requests
from lib import log
#发钉钉消息的api
from config import dingdingConversation

def sendDingMsg(messageJson):
    url = dingdingConversation
    headers = {"Content-Type":"application/json"}
    data = makeDingMdMessage(messageJson)
    requests.request("POST", url, data=data, headers=headers)
    log('异常报告已发送至钉钉群');


def makeDingMdMessage(messageJson):
    title = messageJson['title'];
    lines = messageJson['lines'];
    msgtype = 'markdown';
    text = '';
    for line in lines:
        if line['type'] == 'text':
            if 'style' in line:
                text += line['style'] + ' ';
            if 'fontSize' in line:
                text += line['fontSize'] + ' ';
            if 'content' in line:
                text += line['content'] + ' ';
        elif line['type'] == 'img':
            if 'style' in line:
                text += line['style'] + ' ';
            if 'urls' in line and len(line['urls']) > 0:
                text += ''.join(['![screenshot](' + x + ')' for x in line['urls']])

        text += '\n';

    return json.dumps({
        "msgtype": msgtype,
        "markdown": {
            "title": title,
            "text": text
        }
    })


if __name__ == '__main__':
    messageJson = {
        'title': 'DSP管理后台监控',
        'lines': [{
            'type': 'text',
            'content': 'DSP管理后台监控',
            'fontSize': '#'
        }, {
            'type': 'text',
            'content': '登录页测试用例未通过',
            'style': '>',
            'fontSize': '###'
        },
        {
            'type': 'text',
            'content': '用例: ' + '用例1',
            'style': '>',
            'fontSize': '#####'
        },
        {
            'type': 'text',
            'content': '错误: ' + '错误1',
            'style': '>',
            'fontSize': '#####'
        },
        {
            'type': 'text',
            'content': ' ',
            'style': '>',
            'fontSize': '#####'
        },
        {
            'type': 'text',
            'content': '截图如下',
            'style': '>',
            'fontSize': '######'
        },
        {
            'type': 'img',
            'style': '>',
            'urls': ['https://kuaiyugo.oss-cn-shenzhen.aliyuncs.com/plat/DSP/test2/static_files/1.png']
        }
        ]
    };
    sendDingMsg(messageJson)