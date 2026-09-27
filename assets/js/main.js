// Small enhancements. The site works without any of this.
import { themeToggle } from "./theme.js";
import { lightbox } from "./lightbox.js";

themeToggle();
lightbox();

for (const button of document.querySelectorAll("[data-print]")) {
  button.hidden = false;
  button.addEventListener("click", () => window.print());
}
