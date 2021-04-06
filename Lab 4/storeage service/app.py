import connexion
import datetime
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sendmail import Sendmail
from recievemail import Recievemail
import logging
import logging.config
import yaml


with open('app_conf.yml', 'r') as f:
    db_conf = yaml.safe_load(f.read())


with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


DB_ENGINE = create_engine(f"mysql+pymysql://{db_conf['datastore']['user']}:{db_conf['datastore']['password']}"
                          f"@{db_conf['datastore']['hostname']}:{db_conf['datastore']['port']}/"
                          f"{db_conf['datastore']['db']}")
DB_SESSION = sessionmaker(bind=DB_ENGINE)


# Your functions here
def recieve_mail(body):
    """ Receives a blood pressure reading """

    session = DB_SESSION()

    rm = Recievemail(body['mail_ID'],
                       body['address'])

    session.add(rm)

    session.commit()
    session.close()
    # logg message confirming databse insertion

    return NoContent, 201

def get_recieve_mail(timestamp):


    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    readings = session.query(Recievemail).filter(Recievemail.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings: results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for recieved mail readings after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200

def send_mail(body):
    """ Receives a heart rate (pulse) reading """

    session = DB_SESSION()

    sm = Sendmail(body['mail_ID'],
                   body['address'])

    session.add(sm)

    session.commit()
    session.close()
    # logg message confirming databse insertion

    return NoContent, 201

def get_send_mail(timestamp):


    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    readings = session.query(Sendmail).filter(Sendmail.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings: results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for sent mail readings after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200


app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("open_api.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8090)


