<%inherit file="search.mako"/>
<div class="main_box_left">
    <div class="name_product">
        Name product which you want compare: ${product}
    </div>
</div>
<div class="main_box_right">
    <div class="compare_box">
        <img src="${request.static_path('pyramidaplication:static/img/logo_allegro.png')}" alt="logo_allegro"/>
        <a class="info" href=${allegro_url} target="_blank"><span>Click to see product on Allegro</span><div class="${allegro_price_state}">${allegro_price} </div></a>
    </div>
    <div class="compare_box">
        <img src="${request.static_path('pyramidaplication:static/img/logo_nokaut.png')}" alt="logo_nokaut"/>
        <a class="info" href=${nokaut_url} target="_blank"><span>Click to see product on Nokaut</span><div class="${nokaut_price_state}">${nokaut_price}</div></a>
    </div>
</div>