import * as universal from '../entries/pages/_page.ts.js';

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/+page.ts";
export const imports = ["_app/immutable/nodes/2.DyarFSHb.js","_app/immutable/chunks/CN1eXuiK.js","_app/immutable/chunks/xihTtKlq.js","_app/immutable/chunks/DlTsYIaJ.js","_app/immutable/chunks/BRf5KToz.js","_app/immutable/chunks/BFtoAh1k.js"];
export const stylesheets = ["_app/immutable/assets/2.DbSbDnwx.css"];
export const fonts = [];
