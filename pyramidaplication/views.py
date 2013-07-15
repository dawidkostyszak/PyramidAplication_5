from pyramid.view import (
    view_config,
)

from allegro.lib import (
    allegro_api,
    AllegroError,
)

from nokaut.lib import (
    nokaut_api,
    NokautError,
)

from pyramid.httpexceptions import (
    HTTPFound,
)

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    unauthenticated_userid,
    NO_PERMISSION_REQUIRED,
)

from .models import (
    DBSession,
    Product,
    User,
)

from pyramid_simpleform import Form
from forms import RegistrationForm


def get_user(request):
    user_id = unauthenticated_userid(request)

    if user_id is not None:
        return DBSession.query(User).filter_by(login=user_id)


@view_config(
    route_name='home',
    renderer='pyramidaplication:templates/main.mako',
)
def home_view(request):
    return {}


@view_config(
    route_name='search_result',
    renderer='pyramidaplication:templates/result.mako',
)
def search_result_view(request):

    if not request.user:
        return {'error': 'You need to login before search.'}

    data = request.GET.get('item')

    if not data:
        return {'error': 'Give a product name to compare'}

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

    response = dict(
        error=None,
        product=data,
        allegro_price_state=allegro_state,
        allegro_price=allegro_price,
        allegro_url=allegro_url,
        nokaut_price_state=nokaut_state,
        nokaut_price=nokaut_price,
        nokaut_url=nokaut_url,
    )

    user_id = request.user.first().id
    popularity = 1

    products = DBSession.query(Product).filter_by(name=data).all()
    for prod in products:
        prod.popularity += 1
        popularity = prod.popularity

    product = Product(
        name=data,
        a_price=allegro_price,
        a_url=allegro_url,
        n_price=nokaut_price,
        n_url=nokaut_url,
        popularity=popularity,
        user_id=user_id,
    )
    DBSession.add(product)

    return response


@view_config(
    route_name='login',
    renderer='pyramidaplication:templates/login.mako',
    permission=NO_PERMISSION_REQUIRED,
)
def login_view(request):
    error = None
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        user = DBSession.query(User).filter_by(
            login=login,
            password=password,
        ).first()

        if user:
            authenticated_userid(request)
            headers = remember(request, login)
            return HTTPFound(
                location='/',
                headers=headers,
            )
        error = 'Failed login'

    return dict(
        error=error,
    )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(
        location=('/login'),
        headers=headers,
    )


@view_config(
    route_name='register',
    renderer='pyramidaplication:templates/register.mako',
    permission=NO_PERMISSION_REQUIRED,
)
def register_view(request):
    message = None
    error = None

    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        conf_password = request.POST.get('confirm_password')

        if not login:
            error = 'Please add login.'
        elif not password:
            error = 'Please add password.'
        elif not conf_password:
            error = 'Please add confirm password.'

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

    return dict(
        message=message,
        error=error,
    )


@view_config(
    route_name='history',
    renderer='pyramidaplication:templates/history.mako',
)
def history_view(request):
    response = dict(
        history_search={},
        logged_in=authenticated_userid(request),
    )

    user_id = request.user.first().id
    products = DBSession.query(Product).filter_by(user_id=user_id).all()

    for product in products:
        if product.a_price < product.n_price:
            price = product.a_price
            url = product.a_url
        else:
            price = product.n_price
            url = product.n_url,
        response['history_search'][product.id] = (
            product.name,
            price,
            url[0],
        )
    return response


@view_config(
    route_name='top3',
    renderer='pyramidaplication:templates/top3.mako',
)
def top3_view(request):
    response = dict(
        top3={},
        logged_in=authenticated_userid(request),
    )

    products = DBSession.query(Product).order_by(
        Product.popularity.desc()).all()
    for product in products:
        response['top3'][product.name] = ''
        if len(response['top3']) == 3:
            break
    return response
