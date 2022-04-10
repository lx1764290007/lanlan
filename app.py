from router.Home import *
from model.Sign import auto_add_record
from task.New_Record import job_every_day

job_every_day(auto_add_record)

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    app.run()
