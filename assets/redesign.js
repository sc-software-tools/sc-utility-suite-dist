(function () {
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 1. Cursor spotlight on showcase bands & app cards
  document.querySelectorAll('.showcase-band, .fluent-app-card').forEach(function (el) {
    el.addEventListener('mousemove', function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      el.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  // 2. Efficient IntersectionObserver for self-hosted preview videos (play only when visible, pause offscreen)
  if (!reduced && 'IntersectionObserver' in window) {
    var vidObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var frame = entry.target;
        var video = frame.querySelector('video');
        if (!video) return;
        if (entry.isIntersecting) {
          var playPromise = video.play();
          if (playPromise && playPromise.catch) playPromise.catch(function () {});
          frame.classList.add('video-active');
        } else {
          video.pause();
        }
      });
    }, { threshold: 0.35 });

    document.querySelectorAll('.device-frame[data-autoplay-view="true"]').forEach(function (frame) {
      vidObserver.observe(frame);
    });
  }

  // Hover-activate video preview on devices
  document.querySelectorAll('.device-frame').forEach(function (frame) {
    var video = frame.querySelector('video');
    if (!video || reduced) return;
    frame.addEventListener('mouseenter', function () {
      var p = video.play();
      if (p && p.catch) p.catch(function () {});
      frame.classList.add('video-active');
    });
    frame.addEventListener('mouseleave', function () {
      if (frame.getAttribute('data-autoplay-view') !== 'true') {
        video.pause();
        frame.classList.remove('video-active');
      }
    });
  });

  // 3. Scroll-reveal observer
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
