from sqlalchemy import Column, String, DateTime
from base import Base
import datetime


class Sendmail(Base):
    """ Blood Pressure """

    __tablename__ = "send"

    mail_ID = Column(String(100), primary_key=True)
    address = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)


    def __init__(self, mail_ID, address):
        """ Initializes a blood pressure reading """
        self.mail_ID = mail_ID
        self.address = address
        self.date_created = datetime.datetime.now()


    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['mail_ID'] = self.mail_ID
        dict['address'] = self.address
        dict['date_created'] = self.date_created


        return dict