<%inherit file="search.mako"/>
<div class="main_box_left">
    <div class="name_product">
        % if error == None:
            Name product which you want compare: ${product.name}
        % else:
            ${error}
        % endif
    </div>
</div>
 % if error == None:
    <div class="main_box_right">
        <div class="compare_box">
            <img src="${request.static_path('pyramidaplication:static/img/logo_allegro.png')}" alt="logo_allegro"/>
            <a class="info" href=${product.a_url} target="_blank"><span>Click to see product on Allegro</span><div class="${'win price' if product.a_price < product.n_price else 'price'}">${'No product' if product.a_price == 0 else product.a_price} </div></a>
        </div>
        <div class="compare_box">
            <img src="${request.static_path('pyramidaplication:static/img/logo_nokaut.png')}" alt="logo_nokaut"/>
            <a class="info" href=${product.n_url} target="_blank"><span>Click to see product on Nokaut</span><div class="${'win price' if product.a_price > product.n_price else 'price'}">${'No product' if product.n_price == 0 else product.n_price}</div></a>
        </div>
    </div>
% endif