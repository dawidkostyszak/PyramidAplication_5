<%inherit file="search.mako"/>

<div class="middle">
    <table cellpadding="0" celllspacing="0" border="0" class="list">
        %for product in history_search:
        <tr>
            <td class="name_list">${product.name}</td>
            <td class="price_list">
                %if product.a_price > 0 and product.n_price > 0:
                    Lower price: ${product.a_price if product.a_price < product.n_price else product.n_price} zł
                %elif product.a_price == 0 and product.n_price > 0:
                    Lower price: ${product.n_price} zł
                %elif product.a_price > 0 and product.n_price == 0:
                    Lower price: ${product.a_price} zł
                %else:
                    No product
                %endif
            </td>
            <td class="price_list">Data: ${product.date}</td>
            <td class="price_list">Searched: ${product.popularity} times</td>
            <td class="more"><a class="link_more btn">Refresh</a></td>
        </tr>
        %endfor
    </table>
</div>
