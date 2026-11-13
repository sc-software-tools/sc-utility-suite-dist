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

  const stageTabs = document.querySelectorAll(".stage-tab");
  const windowIcon = document.getElementById("window-icon");
  const windowTitle = document.getElementById("window-title");
  const windowTag = document.getElementById("window-tag");
  const showcaseImg = document.getElementById("showcase-img");
  const showcasePreviewLink = document.getElementById("showcase-preview-link");
  const stageHeadline = document.getElementById("stage-headline");
  const stageSubtext = document.getElementById("stage-subtext");
  const stageCta = document.getElementById("stage-cta");
  const heroShowcase = document.getElementById("hero-showcase");

  if (stageTabs.length && showcaseImg) {
    const DURATION = 4600; // 4.6 seconds per app
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let currentIndex = 0;
    let isPaused = prefersReducedMotion;
    let startTime = performance.now();
    let elapsedBeforePause = 0;

    // Preload all previews
    stageTabs.forEach(tab => {
      const src = tab.dataset.preview;
      if (src) {
        const img = new Image();
        img.src = src;
      }
    });

    function selectTab(index, userInitiated) {
      currentIndex = index;
      elapsedBeforePause = 0;
      startTime = performance.now();

      stageTabs.forEach((tab, i) => {
        const isActive = (i === index);
        tab.classList.toggle("active", isActive);
        tab.setAttribute("aria-selected", String(isActive));
        const fill = tab.querySelector(".tab-progress-fill");
        if (fill) fill.style.width = "0%";
      });

      const activeTab = stageTabs[index];
      const title = activeTab.dataset.title;
      const category = activeTab.dataset.category;
      const headline = activeTab.dataset.headline;
      const subtext = activeTab.dataset.subtext;
      const preview = activeTab.dataset.preview;
      const icon = activeTab.dataset.icon;
      const app = activeTab.dataset.app;

      showcaseImg.style.opacity = "0.3";
      setTimeout(() => {
        showcaseImg.src = preview;
        showcaseImg.alt = title + " desktop interface";
        showcaseImg.style.opacity = "1";
      }, 70);

      if (windowIcon) windowIcon.src = icon;
      if (windowTitle) windowTitle.textContent = title;
      if (windowTag) windowTag.textContent = category;
      if (stageHeadline) stageHeadline.textContent = headline;
      if (stageSubtext) stageSubtext.textContent = subtext;
      if (showcasePreviewLink) {
        showcasePreviewLink.href = preview;
        showcasePreviewLink.dataset.preview = title;
        showcasePreviewLink.setAttribute("aria-label", "Enlarge " + title + " preview");
      }
      if (stageCta) {
        stageCta.href = "#" + app;
        const btnText = stageCta.querySelector("span:first-child");
        if (btnText) btnText.textContent = "Explore " + title;
      }

      // Only scroll the horizontal tabs track itself, NEVER the page window
      const track = activeTab.parentElement;
      if (track && track.scrollWidth > track.clientWidth) {
        const left = activeTab.offsetLeft - track.offsetLeft - 10;
        track.scrollTo({ left: Math.max(0, left), behavior: "smooth" });
      }
    }

    function tick(now) {
      if (!isPaused && stageTabs[currentIndex]) {
        const elapsed = (now - startTime) + elapsedBeforePause;
        const pct = Math.min(100, (elapsed / DURATION) * 100);
        const fill = stageTabs[currentIndex].querySelector(".tab-progress-fill");
        if (fill) fill.style.width = pct + "%";

        if (elapsed >= DURATION) {
          selectTab((currentIndex + 1) % stageTabs.length, false);
        }
      }
      requestAnimationFrame(tick);
    }

    // Start auto-rotation animation loop
    requestAnimationFrame(tick);

    // Pause on hover
    if (heroShowcase) {
      heroShowcase.addEventListener("mouseenter", () => {
        if (!prefersReducedMotion) {
          elapsedBeforePause += (performance.now() - startTime);
          isPaused = true;
        }
      });
      heroShowcase.addEventListener("mouseleave", () => {
        if (!prefersReducedMotion) {
          startTime = performance.now();
          isPaused = false;
        }
      });
    }

    // Tab click and keyboard controls
    stageTabs.forEach((tab, index) => {
      tab.addEventListener("click", () => {
        selectTab(index, true);
      });

      tab.addEventListener("keydown", (e) => {
        let nextIndex;
        if (e.key === "ArrowRight") nextIndex = (index + 1) % stageTabs.length;
        if (e.key === "ArrowLeft") nextIndex = (index - 1 + stageTabs.length) % stageTabs.length;
        if (e.key === "Home") nextIndex = 0;
        if (e.key === "End") nextIndex = stageTabs.length - 1;
        if (nextIndex !== undefined) {
          e.preventDefault();
          stageTabs[nextIndex].focus();
          selectTab(nextIndex, true);
        }
      });
    });

    // Pause rotation if document tab loses visibility
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        isPaused = true;
      } else if (!prefersReducedMotion) {
        startTime = performance.now();
        isPaused = false;
      }
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
