(function () {
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 1. Cursor spotlight on showcase bands & app cards
  if (!reduced) {
    document.querySelectorAll('.showcase-band, .fluent-app-card').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  // 2. Viewport-aware autoplay for hero background videos & hero platform video
  var bgVideos = document.querySelectorAll('.hero-bg-video video, .app-hero-bg video');
  if (reduced) {
    bgVideos.forEach(function (v) { v.pause(); });
  } else if ('IntersectionObserver' in window) {
    var bgObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var v = entry.target;
        if (entry.isIntersecting) {
          var p = v.play();
          if (p && p.catch) p.catch(function () {});
        } else {
          v.pause();
        }
      });
    }, { threshold: 0.05 });
    bgVideos.forEach(function (v) { bgObserver.observe(v); });
  }

  // On app pages, feature the Live Demo video above the fold when motion is allowed
  var heroPlatVid = document.getElementById('hero-platform-vid');
  var liveDemoBtn = document.querySelector('.plat-btn[data-mode="video"]');
  if (heroPlatVid && liveDemoBtn && !reduced) {
    liveDemoBtn.click();
    if ('IntersectionObserver' in window) {
      var platObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (heroPlatVid.hidden) return;
          if (entry.isIntersecting) {
            var p = heroPlatVid.play();
            if (p && p.catch) p.catch(function () {});
          } else {
            heroPlatVid.pause();
          }
        });
      }, { threshold: 0.1 });
      platObserver.observe(heroPlatVid);
    }
  }

  // 3. Hover + Tap-to-preview video on showcase device frames
  document.querySelectorAll('.device-frame').forEach(function (frame) {
    var video = frame.querySelector('video');
    if (!video || reduced) return;

    function startPreview() {
      var p = video.play();
      if (p && p.catch) p.catch(function () {});
      frame.classList.add('video-active');
    }
    function stopPreview() {
      video.pause();
      frame.classList.remove('video-active');
    }

    frame.addEventListener('mouseenter', startPreview);
    frame.addEventListener('mouseleave', stopPreview);

    // Touch/click toggle on the frame itself (without hijacking Watch Trailer & Short button)
    frame.addEventListener('click', function (e) {
      if (e.target.closest('.device-play-fab') || e.target.closest('a')) return;
      if (frame.classList.contains('video-active')) {
        stopPreview();
      } else {
        startPreview();
      }
    });
  });

  // 4. Scroll-reveal observer
  if (!reduced && 'IntersectionObserver' in window) {
    var revObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-visible');
          revObserver.unobserve(en.target);
        }
      });
    }, { threshold: 0.08 });
    document.querySelectorAll('.reveal-up').forEach(function (el) { revObserver.observe(el); });
  } else {
    document.querySelectorAll('.reveal-up').forEach(function (el) { el.classList.add('is-visible'); });
  }
})();
