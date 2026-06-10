import "../../chunks/index-server.js";
import { c as slot, n as attr_class } from "../../chunks/dev.js";
//#region src/routes/+layout.svelte
function _layout($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		$$renderer.push(`<header class="topbar svelte-12qhfyh"><div class="container row svelte-12qhfyh"><a class="brand svelte-12qhfyh" href="/">AI vs ME - World Cup Prediction Challenge</a> <nav class="svelte-12qhfyh"><a href="/" class="svelte-12qhfyh">Predict</a> <a href="/results" class="svelte-12qhfyh">Results</a></nav></div></header> <main${attr_class("container main svelte-12qhfyh", void 0, { "animate-in": false })}><!--[-->`);
		slot($$renderer, $$props, "default", {}, null);
		$$renderer.push(`<!--]--></main>`);
	});
}
//#endregion
export { _layout as default };
