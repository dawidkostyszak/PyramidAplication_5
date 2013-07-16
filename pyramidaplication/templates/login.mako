<%inherit file="base_login.mako"/>
<div class="middle">
    <div class="form_login">
        <div class="head_login">Login in</div>
        <form method="post" action="/login">
            % if error != {}:
                %for err in error.items():
                <p style="color: red">${err[1]}</p>
                %endfor
            %endif
            <input class="input_text" type="text" value="login" name="login"/>
            <input class="input_text" type="password" value="password" name="password"/>
            <button class="btn btn-primary" type=submit>Login</button>
        </form>
    </div>
</div>
