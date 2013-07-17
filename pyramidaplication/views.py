from pyramid.view import view_config
from allegro.lib import allegro_api, AllegroError
from nokaut.lib import nokaut_api, NokautError
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget, NO_PERMISSION_REQUIRED
from .models import DBSession, Product, User
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from forms import RegistrationForm, LoginForm
import datetime


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

    name = request.GET.get('item')

    if not name:
        return {'error': 'Give a product name to compare'}

    date = datetime.date.today()
    user_id = request.user.id
    error = None
    product_exists = DBSession.query(Product)\
                              .filter(
                                  Product.name == name,
                                  Product.user_id == user_id,
                              ).first()

    if product_exists:
        if (date - product_exists.date).days < 2:
            product_exists.popularity += 1
            return dict(
                product=product_exists,
                error=error,
            )

    try:
        allegro_price, allegro_url = allegro_api(name)
    except AllegroError:
        allegro_price = 0
        allegro_url = ''

    try:
        nokaut_price, nokaut_url = nokaut_api(
            name,
            request.registry.settings.get('nokaut_key')
        )
    except NokautError:
        nokaut_price = 0
        nokaut_url = ''

    popularity = 1

    prod = DBSession.query(Product)\
                    .filter(
                        Product.name == name,
                        Product.user_id == user_id
                    ).first()

    if prod:
        popularity = prod.popularity + 1

    product = Product(
        name=name,
        a_price=allegro_price,
        a_url=allegro_url,
        n_price=nokaut_price,
        n_url=nokaut_url,
        popularity=popularity,
        user_id=user_id,
        date=date,
    )
    DBSession.add(product)

    return dict(
        product=product,
        error=error,
    )


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
            headers = remember(request, user.id)
            return HTTPFound(
                location='/',
                headers=headers,
            )

    return dict(renderer=FormRenderer(form))


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(
        location='/login',
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

        user = DBSession.query(User).filter_by(
            login=login,
            password=password,
        ).first()

        headers = remember(request, user.id)
        return HTTPFound(
            location='/',
            headers=headers,
        )
    return dict(renderer=FormRenderer(form))


@view_config(
    route_name='history',
    renderer='pyramidaplication:templates/history.mako',
)
def history_view(request):

    user_id = request.user.id
    products = DBSession.query(Product)\
                        .filter_by(user_id=user_id)\
                        .order_by(Product.date.desc())\
                        .all()

    return dict(history_search=products)


@view_config(
    route_name='top',
    renderer='pyramidaplication:templates/top.mako',
)
def top_view(request):

    top = DBSession.query(Product)\
                   .order_by(Product.popularity.desc())\
                   .limit(3)

    return dict(top=top)
