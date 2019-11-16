(function() {
  var smReady = function() {};
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
    var togglePlay;

    function updateProgressDisplay(percentDone) {
      percentDone = Math.round(100 * percentDone) + '%';
      progressEl.style.width = percentDone;
    }

    playpauseEl.addEventListener('click', function() {
      sound.togglePause();
    });

    resetEl.addEventListener('click', function() {
      if (sound.duration > 0) {
        sound.setPosition(0);
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

    smReady = function() {
      sound = soundManager.createSound({
        id: 'recording',
        url: source,
        autoPlay: true,
        onload: function() {
          duration = sound.duration;
        },
        onerror: function(code, description) {
          console.log(code, description);
          if (this.loaded) {
            this.stop();
          }
        },
        onplay: function() {
          playpauseEl.className = 'icon-pause';
        },
        onresume: function() {
          playpauseEl.className = 'icon-pause';
        },
        onpause: function() {
          playpauseEl.className = 'icon-play';
        },
        onfinish: function() {
          playpauseEl.className = 'icon-play';
        },
        whileplaying: function() {
          var percentDone = sound.position / sound.duration;
          if (!isNaN(percentDone)) {
            updateProgressDisplay(percentDone);
          }
        }
      });

      unloadSound = function() {
        sound.unload();
      }
    };

    if (window.soundManager) {
      soundManager.setup({
        url: 'static/swf/',
        onready: smReady
      });
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
