
import connexion
import yaml
import logging.config
import json
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from os import path


""" LOAD LOGGER YAML FILE """


with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())


""" PRE PROCESSING METHODS """


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()


def populate_stats():
    """ Periodically update stats """

    if not path.exists(app_config['datastore']['filename']):
        data = {}
        data['mail_ID'] = 0
        data['address'] = "123 Seaseme Street"
        data['last_updated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(app_config['datastore']['filename'], 'w') as f:
            json.dump(data, f)


    logger.info("Periodic processing has started")
    with open(app_config['datastore']['filename'], 'r') as file:
        current_stats = json.load(file)

    r_recieve = requests.get(app_config['eventstore']['url']+"/post-office/recievemail", params={'timestamp': current_stats['last_updated']})
    r_send = requests.get(app_config['eventstore']['url']+"/post-office/send", params={'timestamp': current_stats['last_updated']})

    if r_recieve.status_code == 200 or r_send.status_code == 200:
        logger.info(f"Received {len(r_recieve.content)} Mail ID events")
        logger.info(f"Received {len(r_send.content)} address events")
    else:
        logger.error("Bad Request I think")

    process_data(r_recieve.json(), r_send.json())

    logger.info("Periodic Processing has ended")


def process_data(recieve, send):
    """ Process the data before storing it in file """
    with open(app_config['datastore']['filename'], 'r') as json_file:
        old_stats = json.load(json_file)

    old_stats['incoming'] = len(recieve)
    old_stats['sending'] = len(send)
    old_stats['last_send'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(app_config['datastore']['filename'], 'w') as f:
        json.dump(old_stats, f)

    return old_stats


def get_stats():
    """ Returns the statistics """
    logger.info("Your request and my command has started")

    if not path.exists(app_config['datastore']['filename']):
        return "Statistics do not exist", 404
    else:
        with open(app_config['datastore']['filename'], 'r') as f:
            stats = json.load(f)

    logger.debug(stats)
    logger.info("Your request and my command has ended")

    return stats, 200


""" CREATING THE APP """


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)
