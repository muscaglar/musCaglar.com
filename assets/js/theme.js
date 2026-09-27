// The theme switch: one word that goes from Auto (follow the system) to Light to Dark and round again.
// The choice is remembered on this device.
const ORDER = ["auto", "light", "dark"];
const LABEL = { auto: "Auto", light: "Light", dark: "Dark" };

function read() {
  try {
    const saved = localStorage.getItem("theme");
    return saved === "light" || saved === "dark" ? saved : "auto";
  } catch {
    return "auto";
  }
}

function apply(choice) {
  const root = document.documentElement;
  if (choice === "auto") delete root.dataset.theme;
  else root.dataset.theme = choice;
  try {
    if (choice === "auto") localStorage.removeItem("theme");
    else localStorage.setItem("theme", choice);
  } catch {
    // Private browsing: the choice lasts for this page only.
  }
}

export function themeSwitch() {
  const buttons = [...document.querySelectorAll("[data-theme-toggle]")];
  let choice = read();
  const show = () => {
    for (const button of buttons) {
      (button.querySelector("[data-theme-label]") ?? button).textContent = LABEL[choice];
      button.hidden = false;
    }
  };
  for (const button of buttons) {
    button.addEventListener("click", () => {
      choice = ORDER[(ORDER.indexOf(choice) + 1) % ORDER.length];
      apply(choice);
      show();
    });
  }
  show();
}
