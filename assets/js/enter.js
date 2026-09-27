// The page with the password: where to go afterwards, and whether the last try was wrong.
// Both come from the address. Without this script the form still works and leads to the home page.
export function enter() {
  const next = document.querySelector("[data-enter-next]");
  if (!next) return;
  const asked = new URLSearchParams(location.search);
  const to = asked.get("next");
  if (to && to.startsWith("/") && !to.startsWith("//")) next.value = to;
  const wrong = document.querySelector("[data-enter-wrong]");
  if (wrong && asked.has("wrong")) wrong.hidden = false;
}
