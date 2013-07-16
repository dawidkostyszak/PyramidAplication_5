from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Authenticated, Allow
from sqlalchemy import engine_from_config
from .views import logout
from .utils import get_user
from .models import DBSession, Base


class Root(object):
    __acl__ = [
        (Allow, Authenticated, 'view'),
    ]

    def __init__(self, request):
        self.request = request


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy('sosecret')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings,
        root_factory=Root,
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('view')
    config.add_forbidden_view(view=logout)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_request_method(get_user, 'user', reify=True)
    config.add_route('home', '/')
    config.add_route('search_result', '/search_result')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    config.add_route('history', '/history')
    config.add_route('top', '/top')
    config.scan()
    return config.make_wsgi_app()
