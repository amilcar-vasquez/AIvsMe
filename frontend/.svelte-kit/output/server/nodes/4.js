import * as universal from '../entries/pages/results/_page.ts.js';

export const index = 4;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/results/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/results/+page.ts";
export const imports = ["_app/immutable/nodes/4.DnLymyqg.js","_app/immutable/chunks/CN1eXuiK.js","_app/immutable/chunks/xihTtKlq.js","_app/immutable/chunks/DlTsYIaJ.js","_app/immutable/chunks/BFtoAh1k.js"];
export const stylesheets = ["_app/immutable/assets/4.o-obsoUB.css"];
export const fonts = [];
