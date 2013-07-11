<%inherit file="base.mako"/>
<div class="middle">
    <div class="box_search">
        <form action="/search_result">
            <div class="search">
                <input type="text" name='item' value="enter a product name"/>
            </div>
            <button class="btn_search btn btn-primary" type=submit>Search</button>
        </form>
        <a class="btn" href="/history">History search</a>
        <div class="clear"></div>
    </div>
</div>
${next.body()}