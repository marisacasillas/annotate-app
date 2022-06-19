% if tgt is not None:
  <a href="/annotate/{{tgt.id}}?mode={{mode}}" class="nav" id="{{id}}">{{text}}</a>
% else:
  <a href="javascript:void(0)" style="display:hidden;pointer-events:none"></a>
% end
