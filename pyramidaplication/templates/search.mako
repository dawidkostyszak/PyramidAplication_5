<%inherit file="base.mako"/>
<div class="middle">
    <div class="box_search">
        <form action="/search_result">
            <div class="search">
                <input type="text" name='item' value="enter a product name"/>
            </div>
            <button class="btn_search btn btn-primary" type=submit>Search</button>
        </form>
        % if request.user:
            <a class="btn" href="/history">History search</a>
            <a class="btn" href="/top">Top 3 products</a>
        %endif
        <div class="clear"></div>
    </div>
</div>
${next.body()}