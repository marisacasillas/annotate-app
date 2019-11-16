% rebase('base.tpl', title="Sumario de trabajo")
<div class="panel" id="logged-in">
  <span id="name">{{name.upper()}}</span>
  <table id="stats">
    <tr><td>{{stats['user_today']}}</td><td>TERMINASTE HOY</td></tr>
    <tr><td>{{stats['user_complete']}}</td><td>HAS TERMINADO EN TOTAL</td></tr>
    <tr><td>{{stats['remaining']}}</td><td>A HACER</td></tr>
  </table>
  <a href="/annotate" class="button" id="next">EMPEZAR ANOTACIONES</a>
  <a href="/logout" class="button" id="exit">SALIR</a>
</div>
