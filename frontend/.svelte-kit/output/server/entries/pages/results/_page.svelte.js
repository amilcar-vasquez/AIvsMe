import { B as escape_html, i as bind_props, n as attr_class, o as ensure_array_like, z as attr } from "../../../chunks/dev.js";
//#region src/lib/components/SocialCardExport.svelte
function SocialCardExport($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let cardUrl;
		const API_BASE_URL = "http://localhost:8000/api/scoreboard/social-card/";
		let ratio = "9:16";
		$: cardUrl = `${API_BASE_URL}?ratio=${encodeURIComponent(ratio)}`;
		$$renderer.push(`<section class="glass-card exporter svelte-j39qkl"><div class="head svelte-j39qkl"><h3 class="svelte-j39qkl">Social Card Export</h3> <p class="mono svelte-j39qkl">Shorts/TikTok/Stories ready</p></div> <div class="controls svelte-j39qkl"><button${attr_class("svelte-j39qkl", void 0, { "active": true })}>9:16</button> <button${attr_class("svelte-j39qkl", void 0, { "active": false })}>16:9</button> <button${attr_class("svelte-j39qkl", void 0, { "active": false })}>1:1</button></div> <a class="preview svelte-j39qkl"${attr("href", cardUrl)} target="_blank" rel="noreferrer"><img${attr("src", cardUrl)} alt="AI vs Me social scoreboard card" loading="lazy" class="svelte-j39qkl"/></a> <div class="actions svelte-j39qkl"><a class="btn btn-primary"${attr("href", cardUrl)}${attr("download", `ai-vs-me-${ratio}.svg`)}>Download SVG</a> <button class="btn btn-secondary">Copy Share Link</button></div></section>`);
	});
}
//#endregion
//#region src/routes/results/+page.svelte
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let leader;
		let data = $$props["data"];
		$: leader = data.scoreboard.human_points === data.scoreboard.ai_points ? "TIE" : data.scoreboard.human_points > data.scoreboard.ai_points ? "HUMAN LEADS" : "AI LEADS";
		$$renderer.push(`<section class="glass-card board neon-primary svelte-bxfdlt"><p class="mono svelte-bxfdlt">LIVE SCOREBOARD LEADER</p> <h1 class="svelte-bxfdlt">${escape_html(leader)}</h1> <div class="line svelte-bxfdlt"></div> <div class="score-row svelte-bxfdlt"><div class="svelte-bxfdlt"><p class="svelte-bxfdlt">Human</p> <strong class="svelte-bxfdlt">${escape_html(data.scoreboard.human_points)}</strong> <small class="svelte-bxfdlt">${escape_html(data.scoreboard.human_exact_scores)} exacts</small></div> <div class="svelte-bxfdlt"><p class="svelte-bxfdlt">AI</p> <strong class="svelte-bxfdlt">${escape_html(data.scoreboard.ai_points)}</strong> <small class="svelte-bxfdlt">${escape_html(data.scoreboard.ai_exact_scores)} exacts</small></div></div></section> `);
		SocialCardExport($$renderer, {});
		$$renderer.push(`<!----> <section class="results-list svelte-bxfdlt"><h2 class="svelte-bxfdlt">Completed Matches</h2> `);
		if (data.completed.length === 0) {
			$$renderer.push("<!--[0-->");
			$$renderer.push(`<div class="glass-card row svelte-bxfdlt">No completed matches yet.</div>`);
		} else {
			$$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--[-->`);
			const each_array = ensure_array_like(data.completed);
			for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
				let match = each_array[$$index];
				$$renderer.push(`<div class="glass-card row pulse-award svelte-bxfdlt"><div class="svelte-bxfdlt"><p class="teams svelte-bxfdlt">${escape_html(match.team_a_code)} vs ${escape_html(match.team_b_code)}</p> <p class="meta svelte-bxfdlt">${escape_html(match.team_a_name)} vs ${escape_html(match.team_b_name)}</p></div> <p class="display score svelte-bxfdlt">${escape_html(match.actual_score_a)} : ${escape_html(match.actual_score_b)}</p></div>`);
			}
			$$renderer.push(`<!--]-->`);
		}
		$$renderer.push(`<!--]--></section>`);
		bind_props($$props, { data });
	});
}
//#endregion
export { _page as default };
