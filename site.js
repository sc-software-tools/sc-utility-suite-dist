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

  const showcaseTabs = document.querySelectorAll(".showcase-tab");
  const windowAppIcon = document.getElementById("window-app-icon");
  const windowAppTitle = document.getElementById("window-app-title");
  const windowAppBadge = document.getElementById("window-app-badge");
  const showcaseImg = document.getElementById("showcase-img");
  const showcasePreviewLink = document.getElementById("showcase-preview-link");
  const showcaseCaptionText = document.getElementById("showcase-caption-text");
  const showcaseDetailLink = document.getElementById("showcase-detail-link");

  if (showcaseTabs.length && showcaseImg) {
    // Preload preview images for instant tab switching
    showcaseTabs.forEach(tab => {
      const src = tab.dataset.preview;
      if (src) {
        const img = new Image();
        img.src = src;
      }
    });

    function activateTab(tab) {
      showcaseTabs.forEach(t => {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      });
      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");

      const title = tab.dataset.title;
      const category = tab.dataset.category;
      const caption = tab.dataset.caption;
      const preview = tab.dataset.preview;
      const icon = tab.dataset.icon;
      const app = tab.dataset.app;

      showcaseImg.style.opacity = "0.3";
      setTimeout(() => {
        showcaseImg.src = preview;
        showcaseImg.alt = title + " desktop interface";
        showcaseImg.style.opacity = "1";
      }, 80);

      if (windowAppIcon) windowAppIcon.src = icon;
      if (windowAppTitle) windowAppTitle.textContent = title;
      if (windowAppBadge) windowAppBadge.textContent = category;
      if (showcaseCaptionText) showcaseCaptionText.textContent = caption;
      if (showcasePreviewLink) {
        showcasePreviewLink.href = preview;
        showcasePreviewLink.dataset.preview = title;
        showcasePreviewLink.setAttribute("aria-label", "Enlarge " + title + " preview");
      }
      if (showcaseDetailLink) {
        showcaseDetailLink.href = "#" + app;
        const btnText = showcaseDetailLink.querySelector("span:first-child");
        if (btnText) btnText.textContent = "View " + title + " details";
      }
    }

    showcaseTabs.forEach((tab, index) => {
      tab.addEventListener("click", () => activateTab(tab));
      tab.addEventListener("keydown", (e) => {
        let nextIndex;
        if (e.key === "ArrowRight") nextIndex = (index + 1) % showcaseTabs.length;
        if (e.key === "ArrowLeft") nextIndex = (index - 1 + showcaseTabs.length) % showcaseTabs.length;
        if (e.key === "Home") nextIndex = 0;
        if (e.key === "End") nextIndex = showcaseTabs.length - 1;
        if (nextIndex !== undefined) {
          e.preventDefault();
          showcaseTabs[nextIndex].focus();
          activateTab(showcaseTabs[nextIndex]);
        }
      });
    });
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
