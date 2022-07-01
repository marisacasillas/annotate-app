% msg_comleted_today = _('Completed Today')
% msg_remaining = _('Remaining')
% msg_transcription = _('Transcription')
% msg_word = _('Word')
% msg_speaker = _('Speaker')
% msg_save = _('Save')
% msg_and = _('and')
% msg_exit = _('Exit')

% choice_labels = dict(
%   correct_utterance = _('Correct Utterance'),
%   word_present = _('Word Present'),
%   correct_wordform = _('Correct Wordform'),
%   correct_context = _('Correct Context'),
%   correct_speaker = _('Correct Speaker'),
%   addressee = _('Addressee'),
%   audio_usable = _('Usable Audio'),
%   audio_exclusion = _('Audio Exclusion Reason'),
%   onset_quality = _('Onset Missing Syllables'),
%   offset_quality = _('Offset Missing Syllables'),
%   checked = _('Checked'),
% )

% mode_values = dict(
%   skip_prev = _('Skip Previous'),
%   prev = _('Previous'),
%   next = _('Next'),
%   skip_next = _('Skip Next'),
% )

% curr = context['current']

% rebase('base.tpl', title=_("Annotate"))
<div class="panel" id="annotate">
  <div class="context">
    <div id="back-nav">
      <span><a href="/logout" class="nav" id="exit">{{msg_exit}}</a></span>
    </div>

    <div id="current">{{curr.name}}</div>

    <div id="stats">
      <span>{{stats['user_today']}} {{msg_comleted_today}}</span>
      <span>{{stats['remaining']}} {{msg_remaining}}</span>
    </div>
  </div>

  <div class="navigation">
    % include('frag/nav-link.tpl', tgt=context['skip_prev'], id='skip-prev', text=mode_values['skip_prev'])
    % include('frag/nav-link.tpl', tgt=context['prev'], id='prev', text=mode_values['prev'])
    % include('frag/nav-link.tpl', tgt=context['next'], id='next', text=mode_values['next'])
    % include('frag/nav-link.tpl', tgt=context['skip_next'], id='skip-next', text=mode_values['skip_next'])
  </div>

  <form method="post" id="annotation-form">
    <div id="player"
     data-source="/static/snippets/{{curr.name}}">
      <button type="button" id="playpause"><span class="icon-play"></span></button>
      <button type="button" id="reset"><span class="icon-first"></span></button>
      <div id="progress-bar"><div id="progress"></div></div>
    </div>

    % for i, choice in enumerate(choices):
      <div class="choice">
        <label>{{choice_labels[choice.id]}}:</label>
        <select name={{choice.id}}
          % if i == 0:
            autofocus
          % end
        >
        % for option in choice.options:
          <option value="{{option}}"
            % if option == str(getattr(curr, choice.id)):
              selected
            % end
          >{{option}}</option>
        % end
        </select>
      </div>
    % end

    <p id="transcription"><strong>{{msg_transcription}}:</strong> {{curr.transcription}}</p>
    <p id="word"><strong>{{msg_word}}:</strong> {{curr.word}}</p>
    <p id="speaker"><strong>{{msg_speaker}}:</strong> {{curr.speaker}}</p>

    <p>
      <input type="submit" class="button" id="save" value="{{msg_save}}">
      {{msg_and}}
      <select name={{modes.id}}>
        % for option in modes.options:
          <option value="{{option}}"
            % if option == mode:
              selected
            % end
          >{{mode_values[option]}}</option>
        % end
        </select>
      </select>
    </p>
  </form>
</div>
