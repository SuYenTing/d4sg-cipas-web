import requests
from apscheduler.schedulers.blocking import BlockingScheduler

# 防止睡眠
def DoNotSleep():
    url = "https://d4sg-cipas-web.herokuapp.com/"
    r = requests.get(url)
    return print('pinch')

# 開始建立排程任務
sched = BlockingScheduler()

# 防止自動休眠
sched.add_job(DoNotSleep, trigger='interval', id='doNotSleeps_job', minutes=15)

# 啟動排程
sched.start()