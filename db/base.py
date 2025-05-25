from sqlalchemy.orm import declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()

def import_all_models():
    from apps.users.models import User 