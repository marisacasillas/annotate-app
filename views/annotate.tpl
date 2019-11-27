% msg_comleted_today = _('Completed Today')
% msg_remaining = _('Remaining')
% msg_annotation = _('Annotation')
% msg_enter_annotation = _('Enter an annotation above')
% msg_next = _('Next')
% msg_prev = _('Previous')
% msg_exit = _('Exit')

% rebase('base.tpl', title=_("Annotate"))
<div class="panel" id="annotate">
  <table id="stats">
    <tr><td>{{stats['user_today']}}</td><td>{{msg_comleted_today}}</td></tr>
    <tr><td>{{stats['remaining']}}</td><td>{{msg_remaining}}</td></tr>
  </table>

  <p id="current">{{context['current'].name}}</p>

  <form method="post" id="annotation-form">
    <div id="player"
     data-source="/static/snippets/{{context['current'].name}}.mp3">
      <button type="button" id="playpause"><span class="icon-play"></span></button>
      <button type="button" id="reset"><span class="icon-first"></span></button>
      <div id="progress-bar"><div id="progress"></div></div>
    </div>

    <textarea id="annotation" name="annotation" placeholder="{{msg_annotation}}&hellip;"
     autofocus>{{context['current'].annotation}}</textarea>

    <p id="error-empty" class="error hidden"
     >{{msg_enter_annotation}}</p>

    <input type="submit" class="button" id="next" value="{{msg_next}}">
  </form>

  % if 'prev' in context:
    <a href="/annotate/{{context['prev'].id}}"
     class="button" id="prev">{{msg_prev}}</a>
  % end

  <a href="/logout" class="button" id="exit">{{msg_exit}}</a>
</div>
