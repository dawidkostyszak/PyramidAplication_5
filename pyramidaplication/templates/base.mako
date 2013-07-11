<!DOCTYPE HTML>
<html>
<head>
    <title>Compare products prices between Nokaut and Allegro</title>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
    <link rel="stylesheet" href="${request.static_url('pyramidaplication:static/css/style.css')}" type="text/css" media="screen" charset="utf-8" />
</head>
<body>
    <div id="container">
        <div class="main_box">
            <div class="head">
                <div class="logo_img"><a href="/"><img src="${request.static_url('pyramidaplication:static/img/logo.png')}" alt="logo"></a></div>
                <div class="logo_txt">
                    Compare products
                    <div class="logo_txt_small">We will help you find and compare products</div>
                </div>
                <div class="box_login">
                    <a class="btn btn-success" href="/register">Register</a>
                    <a class="btn" href="/login">Login</a>
                </div>
            </div>
            ${next.body()}
        </div>
        <div class="footer">
            <img src="${request.static_url('pyramidaplication:static/img/logo_stx.png')}" alt="logo_stx"/>
        </div>
    </div>
    <script type="text/javascript" src="js/jquery-1.8.3.min.js"></script>
    <script type="text/javascript">
    $(document).ready(function() {
        var btn_search = $('.search input');
        btn_search.focus(function() {
            $(this).attr('value','');
        });
    });
    </script>
</body>
</html>