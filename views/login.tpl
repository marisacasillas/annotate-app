% msg_username = _('Username')
% msg_login = _('Login')
% msg_invalid_user = _("Enter a valid username")

% rebase('base.tpl', title=_("Login"))
<div id="login">
  <form method="post" autocomplete="off">
    <div id="login-panel">
      <input type="text" name="name" id="name"
       placeholder="{{msg_username}}" autofocus autocomplete="off">
      <input type="submit" class="button" value="{{msg_login}}">
      % invalid_name = get('invalid_name', None)
      % if invalid_name is not None:
        <p class="error">{{msg_invalid_user}}</p>
      % end
    </div>
  </form>
</div>
