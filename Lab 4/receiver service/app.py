import connexion
import yaml
import logging
import logging.config
from connexion import NoContent
import requests

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def send_mail(body):
    logger.info(f"Received event sending mail with a unique ID of {body['mail_ID']}")

    headers = {'Content-Type': 'application/json'}

    r = requests.post(app_config['eventstore2']['url'], json=body, headers=headers)

    logger.info(f"Returned event sent mail response (ID: {r.text}) with status {r.status_code}")

    return r.text, r.status_code


def recieve_mail(body):
    logger.info(f"Received event recieve mail with a unique ID of {body['mail_ID']}")

    headers = {'Content-Type': 'application/json'}

    r = requests.post(app_config['eventstore1']['url'], json=body, headers=headers)

    logger.info(f"Returned event recieve mail response (ID: {r.text}) with status {r.status_code}")

    return r.text, r.status_code


app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("open_api.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)


