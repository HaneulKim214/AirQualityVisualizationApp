from app import db
# should run this function in app.py under __name__

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def update_aqi():
    """
    Every 24 hours, update aqi, time column for each city with api_received response
    """
    query = db.select([Aqi.id, Aqi.City])
    result = db.engine.execute(query).fetchall()
    for each_city in result:
        current_city = each_city[1]
        current_id = each_city[0]
        aqi_response = get_aqi(current_city)
        returned_aqi_data = aqi_response['data']['aqi']
        returned_time = aqi_response['data']['time']['s']

        update_this = Aqi.query.filter_by(id=current_id).first()
        update_this.Aqi = returned_aqi_data
        update_this.time = returned_time
        db.session.commit()

    pass





def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
def testing_schedule():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=5)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    # atexit.register(lambda: scheduler.shutdown())
    pass
print_date_time()
# testing_schedule()