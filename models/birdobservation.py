from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Initialize Db
Db = SQLAlchemy()


class BirdObservation(Db.Model):
    # Ref. to table
    __tablename__ = 'birds_heard'

    # Class fields match columns
    obs_id = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    ebird_code = Db.Column(Db.String(64), nullable=False)
    confidence = Db.Column(Db.Float, nullable=False)
    when_heard = Db.Column(Db.DateTime(timezone=True), nullable=False, default=func.now())
    device_id = Db.Column(Db.String(64), nullable=False)

    # toString
    def toString(self):
        return f'{self.obs_id} - #{self.ebird_code} ({self.confidence} {self.when_heard} {self.device_id}))'
