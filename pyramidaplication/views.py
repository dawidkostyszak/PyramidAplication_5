from pyramid.view import view_config
from allegro.lib import allegro_api, AllegroError
from nokaut.lib import nokaut_api, NokautError
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget, NO_PERMISSION_REQUIRED
from .models import DBSession, Product, User
from pyramid_simpleform import Form
from forms import RegistrationForm, LoginForm


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

    user_id = request.user.id
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
    form = Form(request, schema=LoginForm)

    if request.method == 'POST' and form.validate():
        login = form.data['login']
        password = form.data['password']

        user = DBSession.query(User).filter_by(
            login=login,
            password=password,
        ).first()

        if user:
            headers = remember(request, login)
            return HTTPFound(
                location='/',
                headers=headers,
            )

    return dict(
        error=form.errors,
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

    form = Form(request, schema=RegistrationForm)

    if request.method == 'POST' and form.validate():
        login = form.data['login']
        password = form.data['password']
        user = User(login=login, password=password)
        DBSession.add(user)
        return dict(
            message='Login registered successfully.',
            error=form.errors,
        )

    return dict(
        message=None,
        error=form.errors
    )


@view_config(
    route_name='history',
    renderer='pyramidaplication:templates/history.mako',
)
def history_view(request):

    user_id = request.user.id
    products = DBSession.query(Product).filter_by(user_id=user_id).all()

    return dict(history_search=products)


@view_config(
    route_name='top',
    renderer='pyramidaplication:templates/top.mako',
)
def top_view(request):

    top = DBSession.query(Product)\
                   .group_by(Product.popularity)\
                   .order_by(Product.popularity.desc())\
                   .limit(3)

    return dict(top=top)
