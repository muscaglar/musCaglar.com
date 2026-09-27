// Small enhancements. The site works without any of this.
import { themeSwitch } from "./theme.js";
import { lightbox } from "./lightbox.js";
import { enter } from "./enter.js";

themeSwitch();
lightbox();
enter();

for (const button of document.querySelectorAll("[data-print]")) {
  button.hidden = false;
  button.addEventListener("click", () => window.print());
}
