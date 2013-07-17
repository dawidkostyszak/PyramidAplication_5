from pyramid.security import unauthenticated_userid
from .models import DBSession, User


def get_user(request):
    user_id = unauthenticated_userid(request)
    if user_id is not None:
        return DBSession.query(User).filter(User.id == user_id).first()