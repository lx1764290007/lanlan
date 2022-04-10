# -*- coding:utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler


def job_every_day(fn):
     sched = BackgroundScheduler()
     sched.add_job(fn, 'cron', hour=6, timezone='Asia/Shanghai')
     sched.start()