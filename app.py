from flask import Flask, request, render_template, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
import pytz
import logging
import os

from checkin import auto_checkin


"""
VENV: (pyschedule)
TODO
 -import test checkin method
 -run that
 -conf example: NFMIU4/NFO8SY
 -(it works without apscheduler)

 -try with AsyncIOScheduler?
"""


log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

flask_app = Flask(__name__)

# initialize scheduler with your preferred timezone
scheduler = AsyncIOScheduler({'apscheduler.timezone': 'America/Chicago'})

# add a custom jobstore to persist jobs across sessions (default is in-memory)
# scheduler.add_jobstore('sqlalchemy', url='sqlite:////tmp/schedule.db')
scheduler.start()

####### EXAMPLE CURL CALL
# curl -X POST http://127.0.0.1:5000/schedule-flight  -H 'content-type: application/json' -d '{"time":"2019-12-16T11:17","conf": "ABC123", "fname": "ford", "lname": "beezel"}'
# curl -X POST https://pyschedule.herokuapp.com/schedule-flight  -H 'content-type: application/json' -d '{"time":"2019-12-16T11:17","conf": "ABC123", "fname": "ford", "lname": "beezel"}'
#######

@flask_app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')


@flask_app.route('/schedule-flight', methods=['POST'])
def schedule_to_print():
    data = request.get_json()
    #get time to schedule and text to print from the json
    conf = data.get('conf')
    fname = data.get('fname')
    lname = data.get('lname')

    print('Check in details: {} {} {}'.format(conf, fname, lname))

    auto_checkin(conf, fname, lname)

    return 'Check in details: {} {} {}'.format(conf, fname, lname)


@flask_app.route('/schedule-flight-form', methods=['POST'])
def schedule_flight():
    data = request.form
    now = datetime.datetime.now()

    now_plus_5 = now + datetime.timedelta(minutes = 5)
    now_plus_5 = now_plus_5.replace(second=0, microsecond=0)
    #get time to schedule and text to print from the json
    conf = data.get('conf')
    fname = data.get('fname')
    lname = data.get('lname')

    print('Check in details: {} {} {}'.format(conf, fname, lname))
    job = scheduler.add_job(auto_checkin, trigger='date', next_run_time=str(now_plus_5),
                            args=[conf, fname, lname])
    return redirect(url_for('thanks'))

@flask_app.route('/thanks', methods=['GET'])
def thanks():
    return render_template('thanks.html')


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    flask_app.run(threaded=True, port=5000)
