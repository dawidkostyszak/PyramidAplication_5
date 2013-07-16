<%inherit file="search.mako"/>
<div class="middle">
    <table cellpadding="0" celllspacing="0" border="0" class="list">
        % for product in top:
        <tr>
            <td class="name_list">${product.name}</td>
            <td class="name_list">Szukane: ${product.popularity} razy</td>
        </tr>
        % endfor
    </table>
</div>
