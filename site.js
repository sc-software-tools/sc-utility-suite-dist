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
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    let selected = choices.findIndex(choice => choice.getAttribute("aria-pressed") === "true");
    let paused = reducedMotion.matches;
    let hovered = false;
    let visible = true;
    let timer;

    function schedule() {
      window.clearTimeout(timer);
      if (!rotation || choices.length < 2) return;
      rotation.textContent = paused ? "Play previews" : "Pause previews";
      if (paused || hovered || !visible || document.hidden || document.querySelector("#preview-dialog[open]")) return;
      timer = window.setTimeout(() => select((selected + 1) % choices.length, false), 7000);
    }

    function select(index, manual) {
      const choice = choices[index];
      const card = choice && document.getElementById(choice.dataset.featuredApp);
      const source = card?.querySelector(".app-screenshot-frame");
      const heading = card?.querySelector("h3");
      if (!source || !heading || !screenshot || !caption || !meet || !label || !name) return;
      selected = index;
      const title = heading.textContent;
      preview.href = source.href;
      preview.dataset.preview = title;
      preview.setAttribute("aria-label", "Enlarge " + title + " app preview");
      screenshot.src = source.href;
      screenshot.alt = source.querySelector("img").alt;
      name.textContent = title;
      label.textContent = "FEATURED TOOL · " + (index + 1) + " OF " + choices.length;
      caption.textContent = choice.dataset.caption;
      meet.href = "#" + card.id;
      meet.textContent = "Meet " + title + " →";
      choices.forEach((button, i) => button.setAttribute("aria-pressed", String(i === index)));
      if (manual) {
        paused = true;
        announcement.textContent = title + ". " + choice.dataset.caption;
      }
      schedule();
    }

    if (choices.length && rotation && controls && preview && screenshot) {
      controls.hidden = false;
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
      showcase.addEventListener("mouseenter", () => { hovered = true; schedule(); });
      showcase.addEventListener("mouseleave", () => { hovered = false; schedule(); });
      showcase.addEventListener("focusin", event => {
        if (event.target !== rotation) { paused = true; schedule(); }
      });
      document.addEventListener("visibilitychange", schedule);
      reducedMotion.addEventListener("change", () => { if (reducedMotion.matches) paused = true; schedule(); });
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
