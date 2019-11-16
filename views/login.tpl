% rebase('base.tpl', title="Entrar")
<div id="login">
  <form method="post" autocomplete="off">
    <div id="login-panel">
      <input type="text" name="name" id="name"
       placeholder="NOMBRE DE USUARIO" autofocus autocomplete="off">
      <input type="submit" class="button" value="ENTRAR">
      % invalid_name = get('invalid_name', None)
      % if invalid_name is not None:
        <p class="error">Entra un nobre de usuario valido</p>
      % end
    </div>
  </form>
</div>
