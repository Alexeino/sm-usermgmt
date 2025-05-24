from db.session import Base
from db.mixins import TimeStampModelMixin


class User(TimeStampModelMixin, Base):
    pass