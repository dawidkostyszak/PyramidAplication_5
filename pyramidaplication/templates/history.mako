<%inherit file="search.mako"/>

<div class="middle">
    <table cellpadding="0" celllspacing="0" border="0" class="list">
        %for product in history_search:
        <tr>
            <td class="name_list">${product.name}</td>
            %if product.a_price < product.n_price:
                <td class="price_list">Najniższa cena: ${product.a_price} zł</td>
                <td class="more"><a href=${product.a_url} target="_blank" class="link_more btn">Zobacz</a></td>
            %else:
                <td class="price_list">Najniższa cena: ${product.n_price} zł</td>
                <td class="more"><a href=${product.n_url} target="_blank" class="link_more btn">Zobacz</a></td>
            %endif
        </tr>
        %endfor
    </table>
</div>
