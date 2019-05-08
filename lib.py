import time;

def log(words):
    print(time.strftime('[%Y年%m月%d日%H时%M分%S秒] ' + words, time.localtime()))