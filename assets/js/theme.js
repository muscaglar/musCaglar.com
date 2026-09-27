// Cycles the colour theme: follow the system → light → dark. The choice is remembered on this device.
const ORDER = ["system", "light", "dark"];
const LABEL = { system: "Auto", light: "Light", dark: "Dark" };

function read() {
  try {
    const saved = localStorage.getItem("theme");
    return saved === "light" || saved === "dark" ? saved : "system";
  } catch {
    return "system";
  }
}

function apply(choice) {
  const root = document.documentElement;
  if (choice === "system") delete root.dataset.theme;
  else root.dataset.theme = choice;
  try {
    if (choice === "system") localStorage.removeItem("theme");
    else localStorage.setItem("theme", choice);
  } catch {
    // Private browsing: the choice lasts for this page only.
  }
}

export function themeToggle() {
  for (const button of document.querySelectorAll("[data-theme-toggle]")) {
    const label = button.querySelector("[data-theme-label]") ?? button;
    let choice = read();
    const show = () => {
      label.textContent = LABEL[choice];
      button.title = `Colour theme: ${LABEL[choice]}`;
    };
    button.hidden = false;
    show();
    button.addEventListener("click", () => {
      choice = ORDER[(ORDER.indexOf(choice) + 1) % ORDER.length];
      apply(choice);
      show();
    });
  }
}
