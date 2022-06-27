(function() {
  if (document.getElementById('annotate')) {
    var player = setupPlayer();
    setupInteractions(player);
    setupSubmit(player);
  }

  function setupPlayer() {
    var $player = document.getElementById('player');
    var $playpause = document.getElementById('playpause');
    var playpauseIcon = $playpause.querySelector('span');
    var $reset = document.getElementById('reset');
    var $progressBar = document.getElementById('progress-bar');
    var $progress = document.getElementById('progress');

    var source = $player.getAttribute('data-source');
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
      $progress.style.width = percentDone;
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

    $playpause.addEventListener('click', togglePlay);
    $reset.addEventListener('click', seekToBeginning);

    $progressBar.addEventListener('click', function(ev) {
      var clickX = ev.clientX;
      var bounds = $progressBar.getBoundingClientRect();
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
    var $prev = document.querySelector('#prev');
    var $save = document.querySelector('#save');
    var $usable = document.querySelector('[name="audio_usable"]')
    var $exclusion = document.querySelector('[name="audio_exclusion"]')
    var $present = document.querySelector('[name="word_present"]')
    var $wordform = document.querySelector('[name="correct_wordform"]')
    var $speaker = document.querySelector('[name="correct_speaker"]')
    var $addressee = document.querySelector('[name="addressee"]')
    var $checked = document.querySelector('[name="checked"]')

    function focus(el) {
      if (el.focus) {
        el.focus();
      }
    }

    document.addEventListener('keyup', function(ev) {
      var key = ev.key.toLowerCase();
      switch (key) {
        case '/': player.togglePlay(); break;
        case 'u': focus($usable); break;
        case 'e': focus($exclusion); break;
        case 'p': focus($present); break;
        case 'w': focus($wordform); break;
        case 's': focus($speaker); break;
        case 'a': focus($addressee); break;
        case 'c': focus($checked); break;
        case 'arrowleft':
          if (ev.shiftKey) {
            $prev.click();
          } else {
            player.seekToBeginning();
          }
          break;
        case 'enter':
          if (ev.ctrlKey) {
            $save.click();
          }
          break;
      }
    });
  }

  function setupSubmit(player) {
    var $form = document.getElementById('annotation-form');
    $form.onsubmit = function() {
      // Kill the buffering sound before we try to submit.
      player.unloadSound();
    };
  }
})();
