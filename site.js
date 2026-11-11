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
