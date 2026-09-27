// Opens photographs in a full-screen viewer. Without JavaScript the links simply open the picture.
export function lightbox() {
  for (const gallery of document.querySelectorAll("[data-lightbox]")) {
    const links = [...gallery.querySelectorAll("[data-lightbox-item]")];
    if (links.length === 0) continue;

    const dialog = document.createElement("dialog");
    dialog.className = "lightbox";
    dialog.innerHTML = `
      <div class="lightbox-stage"><img alt=""></div>
      <p class="lightbox-caption"></p>
      <button type="button" data-close title="Close">×</button>
      <button type="button" data-prev title="Previous">‹</button>
      <button type="button" data-next title="Next">›</button>`;
    document.body.append(dialog);

    const image = dialog.querySelector("img");
    const caption = dialog.querySelector(".lightbox-caption");
    let index = 0;

    const show = (i) => {
      index = (i + links.length) % links.length;
      const link = links[index];
      image.src = link.href;
      image.alt = link.querySelector("img")?.alt ?? "";
      caption.textContent = link.closest("figure")?.querySelector("figcaption")?.innerText.replace(/\s*\n\s*/g, " · ") ?? "";
      // Fetch the neighbours ahead of time so that moving on feels instant.
      for (const n of [index + 1, index - 1]) {
        const next = links[(n + links.length) % links.length];
        new Image().src = next.href;
      }
    };

    links.forEach((link, i) => {
      link.addEventListener("click", (event) => {
        if (event.metaKey || event.ctrlKey || event.shiftKey) return;
        event.preventDefault();
        show(i);
        dialog.showModal();
      });
    });

    dialog.querySelector("[data-close]").addEventListener("click", () => dialog.close());
    dialog.querySelector("[data-prev]").addEventListener("click", () => show(index - 1));
    dialog.querySelector("[data-next]").addEventListener("click", () => show(index + 1));
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog || event.target.classList.contains("lightbox-stage")) dialog.close();
    });
    dialog.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") show(index - 1);
      if (event.key === "ArrowRight") show(index + 1);
    });

    let startX = null;
    dialog.addEventListener("touchstart", (event) => { startX = event.touches[0].clientX; }, { passive: true });
    dialog.addEventListener("touchend", (event) => {
      if (startX === null) return;
      const moved = event.changedTouches[0].clientX - startX;
      if (Math.abs(moved) > 50) show(index + (moved < 0 ? 1 : -1));
      startX = null;
    }, { passive: true });
  }
}
