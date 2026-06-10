import "../../../../chunks/index-server.js";
import { B as escape_html, i as bind_props, l as stringify, n as attr_class, r as attr_style, z as attr } from "../../../../chunks/dev.js";
//#region src/routes/matches/[id]/+page.svelte
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let data = $$props["data"];
		let scoreA = data.humanPrediction?.predicted_score_a ?? 0;
		let scoreB = data.humanPrediction?.predicted_score_b ?? 0;
		let reasoning = data.humanPrediction?.reasoning ?? "";
		let aiState = data.aiPrediction ? "revealed" : "idle";
		let typewriterText = "";
		let typewriterIndex = 0;
		let displayScoreA = 0;
		let displayScoreB = 0;
		let aiReasoningText = data.aiPrediction?.reasoning ?? "";
		data.aiPrediction?.predicted_score_a;
		data.aiPrediction?.predicted_score_b;
		data.aiPrediction?.confidence_score;
		let displayedConfidence = 0;
		$$renderer.push(`<section class="header svelte-182ivh2"><p class="mono stage svelte-182ivh2">${escape_html(data.match.stage.replaceAll("_", " "))}</p> <h1 class="svelte-182ivh2">${escape_html(data.match.team_a_name)} vs ${escape_html(data.match.team_b_name)}</h1> <p class="mono">Kickoff: ${escape_html(new Date(data.match.kickoff_time).toLocaleString())}</p></section> <section class="duel-grid svelte-182ivh2"><article${attr_class("glass-card neon-secondary panel svelte-182ivh2", void 0, { "locked-state": aiState === "thinking" })}><h2>Human Prediction</h2> <div class="inputs svelte-182ivh2"><label class="svelte-182ivh2">${escape_html(data.match.team_a_code)} <input type="number" min="0"${attr("value", scoreA)}${attr("disabled", aiState === "thinking", true)} class="svelte-182ivh2"/></label> <span>:</span> <label class="svelte-182ivh2">${escape_html(data.match.team_b_code)} <input type="number" min="0"${attr("value", scoreB)}${attr("disabled", aiState === "thinking", true)} class="svelte-182ivh2"/></label></div> <textarea rows="4" placeholder="Add your match rationale"${attr("disabled", aiState === "thinking", true)} class="svelte-182ivh2">`);
		const $$body = escape_html(reasoning);
		if ($$body) $$renderer.push(`${$$body}`);
		$$renderer.push(`</textarea> <button class="btn btn-secondary"${attr("disabled", aiState === "thinking", true)}>${escape_html(aiState === "thinking" ? "AI THINKING..." : "Save Prediction")}</button></article> <article${attr_class("glass-card neon-primary panel ai-panel svelte-182ivh2", void 0, {
			"thinking": aiState === "thinking",
			"challenge": aiState === "challenge"
		})}><h2>AI Prediction</h2> `);
		if (aiState === "idle") {
			$$renderer.push("<!--[0-->");
			$$renderer.push(`<p class="idle-placeholder svelte-182ivh2">AI prediction will auto-generate after your human pick is submitted.</p>`);
		} else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--> `);
		if (aiState === "thinking") {
			$$renderer.push("<!--[0-->");
			$$renderer.push(`<div class="thinking-content svelte-182ivh2"><p class="thinking-header svelte-182ivh2">ANALYZING MATCH DATA <span class="thinking-indicator svelte-182ivh2"></span></p> <div class="dots-animation svelte-182ivh2"><div class="dot-row svelte-182ivh2" style="animation-delay: 0ms">▪</div> <div class="dot-row svelte-182ivh2" style="animation-delay: 150ms">▪</div> <div class="dot-row svelte-182ivh2" style="animation-delay: 300ms">▪</div></div> <p class="mono consulting svelte-182ivh2">CONSULTING AI ENGINE</p></div>`);
		} else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--> `);
		if (aiState === "challenge" || aiState === "revealed") {
			$$renderer.push("<!--[0-->");
			$$renderer.push(`<div${attr("key", aiState)}${attr_class("svelte-182ivh2", void 0, { "settling": aiState === "revealed" })}><p class="display score challenge-score svelte-182ivh2">${escape_html(displayScoreA)} : ${escape_html(displayScoreB)}</p> <div class="confidence-container svelte-182ivh2"><p class="mono confidence svelte-182ivh2">CONFIDENCE</p> <div class="confidence-bar svelte-182ivh2"><div class="confidence-fill svelte-182ivh2"${attr_style(`width: ${stringify(displayedConfidence)}%`)}></div></div> <p class="confidence-value svelte-182ivh2">${escape_html(Math.round(displayedConfidence))}%</p></div> `);
			if (aiState === "challenge") {
				$$renderer.push("<!--[0-->");
				$$renderer.push(`<p class="challenge-header svelte-182ivh2">CHALLENGE ACCEPTED</p>`);
			} else $$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--]--> `);
			if (aiState === "revealed") {
				$$renderer.push("<!--[0-->");
				$$renderer.push(`<p class="reasoning-text svelte-182ivh2">${escape_html(typewriterText)}<span class="cursor svelte-182ivh2">${escape_html(typewriterIndex < aiReasoningText.length ? "▋" : "")}</span></p>`);
			} else $$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--]--></div>`);
		} else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></article></section> `);
		$$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]-->`);
		bind_props($$props, { data });
	});
}
//#endregion
export { _page as default };
