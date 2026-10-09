// Render smoke test: executes index.html's page script with a stub DOM and
// reports how many cards render a real image vs the SVG placeholder.
// Usage: node scripts/render_check.js [path/to/index.html]
const fs = require("fs");
const path = process.argv[2] || "index.html";
const html = fs.readFileSync(path, "utf8");
const m = html.match(/<script>([\s\S]*)<\/script>/);
if (!m) { console.error("no inline script found"); process.exit(2); }

function el() {
  return { value: "", innerHTML: "", textContent: "",
           addEventListener() {}, dataset: {} };
}
const els = { q: el(), sort: el(), chips: el(), grid: el(),
              count: el(), stats: el(), lists: el() };
els.sort.value = "pop"; // default sort, like the page's <select>
const document = {
  getElementById: (id) => els[id] || el(),
  querySelectorAll: () => [],
};
const window = {};
const vm = require("vm");
vm.runInNewContext(m[1], { document, window, console });

const cards = (els.grid.innerHTML.match(/<div class="card">/g) || []).length;
const imgs = [...els.grid.innerHTML.matchAll(/<img[^>]*src="([^"]*)"/g)].map(x => x[1]);
const real = imgs.filter(s => !s.startsWith("data:")).length;
const broken = imgs.filter(s => !s || s.includes("undefined") || s === "").length;
console.log(`cards=${cards} imgs=${imgs.length} real=${real} placeholder=${imgs.length - real} broken=${broken}`);
// show which titles still fall back to the placeholder
const titles = [...els.grid.innerHTML.matchAll(/<h3>([^<]*)/g)].map(x => x[1]);
const srcs = imgs;
const ph = titles.filter((_, i) => srcs[i] && srcs[i].startsWith("data:"));
console.log("placeholder titles (" + ph.length + "): " + ph.join(" | "));
if (broken) process.exit(1);
