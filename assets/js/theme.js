// The theme switch: Auto follows the system; Light and Dark are remembered on this device.
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
  const buttons = [...document.querySelectorAll("[data-theme-set]")];
  const show = (choice) => {
    for (const button of buttons) button.setAttribute("aria-pressed", String(button.dataset.themeSet === choice));
  };
  for (const button of buttons) {
    button.addEventListener("click", () => {
      apply(button.dataset.themeSet);
      show(button.dataset.themeSet);
    });
  }
  show(read());
}
