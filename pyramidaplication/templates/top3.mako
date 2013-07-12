<%inherit file="search.mako"/>
<div class="middle">
    <table cellpadding="0" celllspacing="0" border="0" class="list">
        % for item in top3.items():
        <tr>
            <td class="name_list">${item[0]}</td>
        </tr>
        % endfor
    </table>
</div>
