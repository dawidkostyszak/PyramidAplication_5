from pyramid.view import view_config
from allegro.lib import allegro_api, AllegroError
from nokaut.lib import nokaut_api, NokautError
from pyramid.httpexceptions import HTTPFound

from .models import (
    DBSession,
    Product,
    User,
)


@view_config(
    route_name='home',
    renderer='pyramidaplication:templates/main.mako'
)
def home_view(request):
    return {}


@view_config(
    route_name='search_result',
    renderer='pyramidaplication:templates/result.mako'
)
def search_result_view(request):

    data = request.GET.get('item')

    if not data:
        return {'error': 'no data'}

    allegro_state = nokaut_state = 'price'

    try:
        allegro_price, allegro_url = allegro_api(data)
    except AllegroError:
        allegro_state = 'price'
        allegro_price = 'No product'
        allegro_url = ''

    try:
        nokaut_price, nokaut_url = nokaut_api(
            data,
            request.registry.settings.get('nokaut_key')
        )
    except NokautError:
        nokaut_state = 'price'
        nokaut_price = 'No product'
        nokaut_url = ''

    if nokaut_price != allegro_price:
        if allegro_price < nokaut_price:
            allegro_state = 'price win'
        else:
            nokaut_state = 'price win'

    response = {
        'error': None,
        'product': data,
        'allegro_price_state': allegro_state,
        'allegro_price': allegro_price,
        'allegro_url': allegro_url,
        'nokaut_price_state': nokaut_state,
        'nokaut_price': nokaut_price,
        'nokaut_url': nokaut_url,
    }

    product = Product(
        name=data,
        a_price=allegro_price,
        a_url=allegro_url,
        n_price=nokaut_price,
        n_url=nokaut_url,
    )
    DBSession.add(product)

    return response


@view_config(
    route_name='login',
    renderer='pyramidaplication:templates/login.mako'
)
def login_view(request):
    return {}


@view_config(route_name='register',
             renderer='pyramidaplication:templates/register.mako')
def register_view(request):
    message = None
    error = None

    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        conf_password = request.POST.get('confirm_password')
        #import ipdb; ipdb.set_trace()

        if not login:
            error = 'Please add login'
        elif not password:
            error = 'Please add password'
        elif not conf_password:
            error = 'Please add confirm password'

        if error:
            return {'message': message, 'error': error}

        log = DBSession.query(User).filter_by(login=login).first()

        if log:
            error = 'Login already in use please try another.'
        elif len(password) < 8:
            error = 'Password to short. Need 8 characters.'
        elif password != conf_password:
            error = 'Confirm password is different than password.'
        else:
            message = 'Login registered successfully.'
            user = User(login=login, password=password)
            DBSession.add(user)

    return {'message': message, 'error': error}


@view_config(
    route_name='history',
    renderer='pyramidaplication:templates/history.mako'
)
def history_view(request):
    response = {'history_search': {}}
    products = DBSession.query(Product).filter_by().all()
    for product in products:
        response['history_search'][product.id] = (
            product.name,
            product.a_price,
            product.a_url,
            product.n_price,
            product.n_url
        )
    return response


@view_config(
    route_name='top3',
    renderer='pyramidaplication:templates/history.mako'
)
def top3_view(request):
    return {}
