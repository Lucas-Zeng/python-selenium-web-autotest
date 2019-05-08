import subprocess
import time
from lib import log

def run_test_case_by_subprocess():
    log('测试开始');
    p = subprocess.Popen('python3 index.py',shell=True)
    p.wait()
    log('测试结束\n\n');

while True:
    run_test_case_by_subprocess()
    #每5分钟跑一次测试
    time.sleep(60*5)
    # time.sleep(3)
