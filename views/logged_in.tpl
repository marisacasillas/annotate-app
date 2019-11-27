% msg_complete_today = _('Completed Today')
% msg_complete_total = _('Completed Total')
% msg_remaining = _('Remaining')
% msg_begin = _('Begin Annotating')
% msg_exit = _('Exit')

% rebase('base.tpl', title=_('Work Summary'))
<div class="panel" id="logged-in">
  <span id="name">{{name.upper()}}</span>
  <table id="stats">
    <tr><td>{{stats['user_today']}}</td><td>{{msg_complete_today}}</td></tr>
    <tr><td>{{stats['user_complete']}}</td><td>{{msg_complete_total}}</td></tr>
    <tr><td>{{stats['remaining']}}</td><td>{{msg_remaining}}</td></tr>
  </table>
  <a href="/annotate" class="button" id="next">{{msg_begin}}</a>
  <a href="/logout" class="button" id="exit">{{msg_exit}}</a>
</div>
