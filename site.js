/* Progressive enhancement: navigation and downloads work without JavaScript. */
(() => {
  "use strict";

  const menu = document.querySelector(".mobile-menu");
  if (menu) {
    menu.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => { menu.open = false; });
    });
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && menu.open) {
        menu.open = false;
        menu.querySelector("summary").focus();
      }
    });
    document.addEventListener("click", event => {
      if (menu.open && !menu.contains(event.target)) menu.open = false;
    });
  }

  const showcase = document.querySelector(".hero-showcase");
  if (showcase) {
    const choices = [...showcase.querySelectorAll("[data-featured-app]")];
    const rotation = showcase.querySelector(".showcase-rotation");
    const controls = showcase.querySelector(".showcase-controls");
    const preview = showcase.querySelector(".preview-link");
    const screenshot = preview?.querySelector("img");
    const caption = showcase.querySelector(".showcase-caption");
    const meet = showcase.querySelector(".showcase-meet");
    const label = showcase.querySelector(".showcase-position");
    const name = showcase.querySelector(".showcase-name");
    const announcement = showcase.querySelector(".showcase-announcement");
    const progress = showcase.querySelector(".showcase-progress span");
    const previous = showcase.querySelector(".showcase-previous");
    const next = showcase.querySelector(".showcase-next");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const interval = 7000;
    let selected = choices.findIndex(choice => choice.getAttribute("aria-pressed") === "true");
    let paused = reducedMotion.matches;
    let hovered = false;
    let visible = true;
    let timer;
    let remaining = interval;
    let started = 0;
    let progressAnimation;
    let transitions = [];
    let outgoing;
    let swipe;
    let suppressClickUntil = 0;

    function clearTransition() {
      transitions.forEach(animation => animation.cancel());
      transitions = [];
      outgoing?.remove();
      outgoing = null;
    }

    function animateChange(oldImage, direction) {
      clearTransition();
      if (!oldImage || !direction || reducedMotion.matches || typeof screenshot.animate !== "function") return;
      outgoing = screenshot.cloneNode();
      outgoing.removeAttribute("fetchpriority");
      outgoing.src = oldImage;
      outgoing.alt = "";
      outgoing.className = "showcase-outgoing";
      outgoing.setAttribute("aria-hidden", "true");
      preview.append(outgoing);
      const timing = { duration: 520, easing: "cubic-bezier(.16,1,.3,1)" };
      const departing = outgoing.animate([
        { opacity: 1, transform: "translateX(0) scale(1)" },
        { opacity: 0, transform: "translateX(" + (-direction * 34) + "px) scale(.965)" }
      ], timing);
      const arriving = screenshot.animate([
        { opacity: .1, transform: "translateX(" + (direction * 44) + "px) scale(.965)" },
        { opacity: 1, transform: "translateX(0) scale(1)" }
      ], timing);
      transitions = [departing, arriving,
        caption.animate([{ opacity: .1, transform: "translateY(8px)" }, { opacity: 1, transform: "translateY(0)" }], { ...timing, duration: 420 }),
        name.animate([{ opacity: .3 }, { opacity: 1 }], timing)];
      const ghost = outgoing;
      departing.onfinish = () => { ghost.remove(); if (outgoing === ghost) outgoing = null; };
    }

    function schedule() {
      window.clearTimeout(timer);
      if (started) remaining = Math.max(0, remaining - (performance.now() - started));
      started = 0;
      if (!rotation || choices.length < 2) return;
      rotation.innerHTML = paused 
        ? '<svg viewBox="0 0 16 16" fill="currentColor" width="11" height="11" aria-hidden="true"><path d="m4 3 9 5-9 5z"/></svg><span>Play</span>' 
        : '<svg viewBox="0 0 16 16" fill="currentColor" width="11" height="11" aria-hidden="true"><path d="M3.5 3h3v10h-3zm6 0h3v10h-3z"/></svg><span>Pause</span>';
      rotation.setAttribute("aria-label", paused ? "Play previews auto-rotation" : "Pause previews auto-rotation");
      const playing = !paused && !hovered && visible && !document.hidden && !document.querySelector("#preview-dialog[open]");
      showcase.dataset.playing = String(playing);
      if (progress && typeof progress.animate === "function" && !reducedMotion.matches) {
        if (!progressAnimation) progressAnimation = progress.animate([{ transform: "scaleX(0)" }, { transform: "scaleX(1)" }], { duration: interval, fill: "both", easing: "linear" });
        progressAnimation.pause();
        progressAnimation.currentTime = interval - remaining;
        if (playing) progressAnimation.play();
      } else {
        progressAnimation?.cancel(); progressAnimation = null;
      }
      if (!playing) return;
      started = performance.now();
      timer = window.setTimeout(() => {
        started = 0;
        select((selected + 1) % choices.length, false);
      }, remaining);
    }

    function select(index, manual) {
      const choice = choices[index];
      const card = choice && document.getElementById(choice.dataset.featuredApp);
      const source = card?.querySelector(".app-screenshot-frame");
      const heading = card?.querySelector("h3");
      if (!source || !heading || !screenshot || !caption || !meet || !label || !name) return;
      const direction = index === selected ? 0 : ((index - selected + choices.length) % choices.length <= choices.length / 2 ? 1 : -1);
      const oldImage = screenshot.getAttribute("src");
      selected = index;
      remaining = interval;
      started = 0;
      const title = heading.textContent;
      preview.href = source.href;
      preview.dataset.preview = title;
      preview.setAttribute("aria-label", "Enlarge " + title + " app preview");
      screenshot.src = source.href;
      screenshot.alt = source.querySelector("img").alt;
      name.textContent = title;
      label.textContent = "FEATURED TOOL · " + (index + 1) + " OF " + choices.length;
      const windowTitle = showcase.querySelector(".window-title-sub");
      if (windowTitle) windowTitle.textContent = title + " · Desktop Interface";
      caption.textContent = choice.dataset.caption;
      meet.href = "#" + card.id;
      meet.textContent = "Meet " + title + " →";
      choices.forEach((button, i) => button.setAttribute("aria-pressed", String(i === index)));
      animateChange(oldImage, direction);
      if (manual) {
        paused = true;
        announcement.textContent = title + ". " + choice.dataset.caption;
      }
      schedule();
    }

    if (choices.length && rotation && controls && preview && screenshot) {
      controls.hidden = false;
      // Small, real application previews are cached before they enter the stage.
      choices.forEach(choice => {
        const source = document.getElementById(choice.dataset.featuredApp)?.querySelector(".app-screenshot-frame");
        if (source) { const image = new Image(); image.src = source.href; }
      });
      choices.forEach((choice, index) => {
        choice.addEventListener("click", () => select(index, true));
        choice.addEventListener("keydown", event => {
          let next;
          if (event.key === "ArrowRight") next = (index + 1) % choices.length;
          if (event.key === "ArrowLeft") next = (index + choices.length - 1) % choices.length;
          if (event.key === "Home") next = 0;
          if (event.key === "End") next = choices.length - 1;
          if (next === undefined) return;
          event.preventDefault(); choices[next].focus(); select(next, true);
        });
      });
      rotation.addEventListener("click", () => { paused = !paused; schedule(); });
      previous?.addEventListener("click", () => select((selected + choices.length - 1) % choices.length, true));
      next?.addEventListener("click", () => select((selected + 1) % choices.length, true));
      preview.addEventListener("pointerdown", event => {
        if (event.isPrimary) suppressClickUntil = 0;
        if (event.isPrimary && event.pointerType === "touch") swipe = { id: event.pointerId, x: event.clientX, y: event.clientY };
      });
      preview.addEventListener("pointercancel", event => { if (swipe?.id === event.pointerId) swipe = null; });
      preview.addEventListener("pointerup", event => {
        if (!swipe || event.pointerType !== "touch" || swipe.id !== event.pointerId) return;
        const dx = event.clientX - swipe.x, dy = event.clientY - swipe.y;
        swipe = null;
        if (Math.abs(dx) < 45 || Math.abs(dx) < Math.abs(dy) * 1.4) return;
        suppressClickUntil = performance.now() + 600;
        select((selected + (dx < 0 ? 1 : choices.length - 1)) % choices.length, true);
      });
      preview.addEventListener("click", event => {
        if (performance.now() < suppressClickUntil) { event.preventDefault(); event.stopImmediatePropagation(); }
      }, true);
      showcase.addEventListener("mouseenter", () => { hovered = true; schedule(); });
      showcase.addEventListener("mouseleave", () => { hovered = false; schedule(); });
      showcase.addEventListener("focusin", event => {
        if (!rotation.contains(event.target)) { paused = true; schedule(); }
      });
      document.addEventListener("visibilitychange", schedule);
      reducedMotion.addEventListener("change", () => { if (reducedMotion.matches) { paused = true; clearTransition(); } schedule(); });
      document.getElementById("preview-dialog")?.addEventListener("close", schedule);
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(entries => { visible = entries[0].isIntersecting; schedule(); }).observe(showcase);
      }
      select(selected < 0 ? 0 : selected, false);
    }
  }

  const dialog = document.getElementById("preview-dialog");
  const image = document.getElementById("preview-image");
  const title = document.getElementById("preview-title");
  const closeButton = document.getElementById("close-preview");
  if (!dialog || !image || !title || !closeButton || typeof dialog.showModal !== "function") return;

  let trigger = null;
  document.querySelectorAll("a[data-preview]").forEach(link => {
    link.addEventListener("click", event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      trigger = link;
      title.textContent = link.dataset.preview;
      image.src = link.href;
      image.alt = link.dataset.preview + " desktop interface";
      dialog.showModal();
      closeButton.focus();
    });
  });
  closeButton.addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", event => {
    const rect = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right ||
        event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
  });
  dialog.addEventListener("close", () => {
    image.removeAttribute("src");
    if (trigger && trigger.isConnected) trigger.focus({ preventScroll: true });
  });
})();
