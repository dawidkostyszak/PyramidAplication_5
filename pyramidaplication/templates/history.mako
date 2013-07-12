<%inherit file="search.mako"/>
<div class="middle">
    <table cellpadding="0" celllspacing="0" border="0" class="list">
        % for item in history_search.items():
        <tr>
            <td class="name_list">${item[1][0]}</td>
            <td class="price_list">Najniższa cena: ${item[1][1]} zł</td>
            <td class="more"><a href=${item[1][2]} target="_blank" class="link_more btn">Zobacz</a></td>
        </tr>
        % endfor
    </table>
</div>
