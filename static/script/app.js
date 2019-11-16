(function() {
  var unloadSound = function() {};

  if (document.getElementById('annotate')) {
    setupPlayer();
    disallowEmptyAnnotation();
  }

  function setupPlayer() {
    var playerEl = document.getElementById('player');
    var playpauseEl = document.getElementById('playpause');
    var resetEl = document.getElementById('reset');
    var progressBarEl = document.getElementById('progress-bar');
    var progressEl = document.getElementById('progress');

    var source = playerEl.getAttribute('data-source');
    var sound = {};

    function updateProgressDisplay(percentDone) {
      percentDone = ((100 * percentDone) || 0) + '%';
      progressEl.style.width = percentDone;
    }

    playpauseEl.addEventListener('click', function() {
      if (sound.playing()) {
        sound.pause();
      } else {
        sound.play();
      }
    });

    resetEl.addEventListener('click', function() {
      if (sound.duration() > 0) {
        sound.seek(0);
        updateProgressDisplay(0.0);
      }
    });

    progressBarEl.addEventListener('click', function(ev) {
      var clickX = ev.clientX;
      var bounds = progressBarEl.getBoundingClientRect();
      var left = bounds.left + window.scrollX;
      var right = bounds.right + window.scrollX;
      var pos = (clickX - left) / (right - left);
      if (sound.duration && pos >= 0 && pos <= 1) {
        var offset = Math.round(sound.duration * pos);
        updateProgressDisplay(pos);
        sound.setPosition(offset);
      }
    });

    setupSound = function() {
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
          playpauseEl.className = 'icon-pause';
          requestAnimationFrame(updateProgress);
        },
        onpause: function() {
          playpauseEl.className = 'icon-play';
        },
        onstop: function() {
          playpauseEl.className = 'icon-play';
        },
        onend: function() {
          playpauseEl.className = 'icon-play';
        },
      });

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

      unloadSound = function() {
        sound.unload();
      }
    };

    if (window.Howl) {
      setupSound();
    }
  }

  function disallowEmptyAnnotation() {
    var formEl = document.getElementById('annotation-form');
    var textareaEl = document.getElementById('annotation');
    var errorEl = document.getElementById('error-empty');

    formEl.onsubmit = function() {
      if (textareaEl.value.trim() == '') {
        errorEl.classList.remove('hidden');
        return false;
      }
      // Kill the buffering sound before we try to submit.
      unloadSound();
    };
  }
})();
