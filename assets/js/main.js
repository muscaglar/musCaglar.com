// Small enhancements. The site works without any of this.
import { themeSwitch } from "./theme.js";
import { lightbox } from "./lightbox.js";

themeSwitch();
lightbox();

for (const button of document.querySelectorAll("[data-print]")) {
  button.hidden = false;
  button.addEventListener("click", () => window.print());
}
