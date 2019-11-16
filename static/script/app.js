(function() {
  if (document.getElementById('annotate')) {
    var player = setupPlayer();
    setupInteractions(player);
    disallowEmptyAnnotation(player);
  }

  function setupPlayer() {
    var playerEl = document.getElementById('player');
    var playpauseEl = document.getElementById('playpause');
    var playpauseIcon = playpauseEl.querySelector('span');
    var resetEl = document.getElementById('reset');
    var progressBarEl = document.getElementById('progress-bar');
    var progressEl = document.getElementById('progress');

    var source = playerEl.getAttribute('data-source');
    var sound;
    var interface = new EventTarget();

    function togglePlay() {
      if (sound.playing()) {
        sound.pause();
      } else {
        sound.play();
      }
    }

    function seekToBeginning() {
      if (sound.duration() > 0) {
        sound.seek(0);
        updateProgressDisplay(0.0);
      }
    }

    function updateProgress() {
      var position = sound.seek() || 0;
      var duration = sound.duration();
      var percentDone = position / duration;
      if (!isNaN(percentDone)) {
        updateProgressDisplay(percentDone);
      }
      if (sound.playing()) {
        requestAnimationFrame(updateProgress);
      }
    }

    function updateProgressDisplay(percentDone) {
      percentDone = ((100 * percentDone) || 0) + '%';
      progressEl.style.width = percentDone;
    }

    function unloadSound() {
      sound.unload();
    }

    sound = new Howl({
      id: 'recording',
      src: [source],
      autoplay: true,
      onplayerror: function(soundId, message) {
        sound.pause();
        sound.once('unlock', function() {
          sound.play();
        });
      },
      onload: function() {
        if (!sound.playing()) {
          playpauseEl.focus();
        }
      },
      onplay: function() {
        playpauseIcon.className = 'icon-pause';
        interface.dispatchEvent(new Event('play'));
        requestAnimationFrame(updateProgress);
      },
      onpause: function() {
        playpauseIcon.className = 'icon-play';
      },
      onstop: function() {
        playpauseIcon.className = 'icon-play';
      },
      onend: function() {
        playpauseIcon.className = 'icon-play';
      },
    });

    playpauseEl.addEventListener('click', togglePlay);
    resetEl.addEventListener('click', seekToBeginning);

    progressBarEl.addEventListener('click', function(ev) {
      var clickX = ev.clientX;
      var bounds = progressBarEl.getBoundingClientRect();
      var left = bounds.left + window.scrollX;
      var right = bounds.right + window.scrollX;
      var pos = (clickX - left) / (right - left);
      if (sound.duration && pos >= 0 && pos <= 1) {
        var offset = Math.round(sound.duration() * pos);
        updateProgressDisplay(pos);
        sound.seek(offset);
      }
    });

    interface.togglePlay = togglePlay;
    interface.seekToBeginning = seekToBeginning;
    interface.unloadSound = unloadSound;
    return interface;
  }

  function setupInteractions(player) {
    var prevBtn = document.querySelector('#prev');
    var nextBtn = document.querySelector('#next');
    var textareaEl = document.querySelector('#annotation');

    document.addEventListener('keyup', function(ev) {
      var key = ev.key.toLowerCase();

      if (ev.target && ev.target.tagName == 'TEXTAREA') {
        if (key == 'escape') {
          nextBtn.focus();
        }
        return;
      }

      switch (key) {
        case '/': player.togglePlay(); break;
        case 'arrowleft':
          if (ev.shiftKey) {
            prevBtn.click();
          } else {
            player.seekToBeginning();
          }
          break;
        case 'arrowright':
          if (ev.shiftKey) {
            nextBtn.click();
          }
          break;
        case 't': textareaEl.focus(); break;
      }
    });

    // Automatically focus the text area any time we start playing.
    player.addEventListener('play', function() {
      textareaEl.focus();
    });
  }

  function disallowEmptyAnnotation(player) {
    var formEl = document.getElementById('annotation-form');
    var textareaEl = document.getElementById('annotation');
    var errorEl = document.getElementById('error-empty');

    formEl.onsubmit = function() {
      if (textareaEl.value.trim() == '') {
        errorEl.classList.remove('hidden');
        textareaEl.focus();
        return false;
      }
      // Kill the buffering sound before we try to submit.
      player.unloadSound();
    };
  }
})();
