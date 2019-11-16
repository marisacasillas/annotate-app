% rebase('base.tpl', title="Anotar")
<div class="panel" id="annotate">
  <table id="stats">
    <tr><td>{{stats['user_today']}}</td><td>TERMINASTE HOY</td></tr>
    <tr><td>{{stats['remaining']}}</td><td>A HACER</td></tr>
  </table>

  <p id="current">{{context['current'].name}}</p>

  <form method="post" id="annotation-form">
    <div id="player"
     data-source="/static/snippets/{{context['current'].name}}.mp3">
      <span id="playpause" class="icon-play"></span>
      <span id="reset" class="icon-first"></span>
      <div id="progress-bar"><div id="progress"></div></div>
    </div>

    <textarea id="annotation" name="annotation" placeholder="Anotación..."
     autofocus>{{context['current'].annotation}}</textarea>

    <p id="error-empty" class="error hidden"
     >Tecla una anotación arriba</p>

    <input type="submit" class="button" id="next" value="PRÓXIMO">
  </form>

  % if 'prev' in context:
    <a href="/annotate/{{context['prev'].id}}"
     class="button" id="prev">ÚLTIMO</a>
  % end

  <a href="/logout" class="button" id="exit">SALIR</a>
</div>
