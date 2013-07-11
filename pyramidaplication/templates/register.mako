<%inherit file="base_login.mako"/>
<div class="middle">
    <div class="form_login">
        <div class="head_login">Register</div>
        <form action="/login">
            <input class="input_text" type="text" value="login"/>
            <input class="input_text" type="password" value="password"/>
            <input class="input_text" type="password" value="confirm_password"/>
            <button class="btn btn-primary" type=submit>Register</button>
        </form>
    </div>
</div>
