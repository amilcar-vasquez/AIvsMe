import "../../chunks/index-server.js";
import { B as escape_html, i as bind_props, o as ensure_array_like, z as attr } from "../../chunks/dev.js";
//#region src/lib/components/ScoreboardHero.svelte
function ScoreboardHero($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let lead, momentum;
		let scoreboard = $$props["scoreboard"];
		let displayedHumanPoints = 0;
		let displayedAIPoints = 0;
		$: lead = displayedAIPoints - displayedHumanPoints;
		$: momentum = lead === 0 ? "TIED" : lead > 0 ? "AI MOMENTUM" : "HUMAN MOMENTUM";
		$$renderer.push(`<section class="glass-card neon-primary hero svelte-1820a2y"><div><p class="mono label svelte-1820a2y">LIVE TOURNAMENT STATUS</p> <h1 class="svelte-1820a2y">World Cup Arena</h1> <p class="momentum svelte-1820a2y">${escape_html(momentum)}</p></div> <div class="score svelte-1820a2y"><div><p class="mono human svelte-1820a2y">HUMAN</p> <span class="display svelte-1820a2y">${escape_html(displayedHumanPoints)}</span></div> <div class="vs display svelte-1820a2y">VS</div> <div><p class="mono ai svelte-1820a2y">AI</p> <span class="display svelte-1820a2y">${escape_html(displayedAIPoints)}</span></div></div></section>`);
		bind_props($$props, { scoreboard });
	});
}
//#endregion
//#region src/lib/components/UpcomingMatches.svelte
function UpcomingMatches($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let matches = $$props["matches"];
		$$renderer.push(`<section class="list svelte-hho2fb"><h2 class="svelte-hho2fb">Upcoming Matches</h2> `);
		if (matches.length === 0) {
			$$renderer.push("<!--[0-->");
			$$renderer.push(`<div class="glass-card item svelte-hho2fb">No upcoming matches yet.</div>`);
		} else {
			$$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--[-->`);
			const each_array = ensure_array_like(matches);
			for (let i = 0, $$length = each_array.length; i < $$length; i++) {
				let match = each_array[i];
				$$renderer.push(`<a class="glass-card item svelte-hho2fb"${attr("href", `/matches/${match.id}`)}><div><p class="teams svelte-hho2fb">${escape_html(match.team_a_code)} vs ${escape_html(match.team_b_code)}</p> <p class="meta svelte-hho2fb">${escape_html(match.team_a_name)} vs ${escape_html(match.team_b_name)}</p></div> <p class="mono kickoff svelte-hho2fb">${escape_html(new Date(match.kickoff_time).toLocaleString())}</p></a>`);
			}
			$$renderer.push(`<!--]-->`);
		}
		$$renderer.push(`<!--]--></section>`);
		bind_props($$props, { matches });
	});
}
//#endregion
//#region src/routes/+page.svelte
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let humanRate, aiRate;
		let data = $$props["data"];
		const stats = [
			{
				label: "HUMAN EXACT SCORE RATE",
				value: humanRate,
				unit: "%"
			},
			{
				label: "AI EXACT SCORE RATE",
				value: aiRate,
				unit: "%"
			},
			{
				label: "TOTAL MATCHES SCORED",
				value: data.scoreboard.total_matches,
				unit: ""
			}
		];
		$: humanRate = data.scoreboard.total_matches ? Math.round(data.scoreboard.human_exact_scores / data.scoreboard.total_matches * 100) : 0;
		$: aiRate = data.scoreboard.total_matches ? Math.round(data.scoreboard.ai_exact_scores / data.scoreboard.total_matches * 100) : 0;
		ScoreboardHero($$renderer, { scoreboard: data.scoreboard });
		$$renderer.push(`<!----> <section class="glass-card neon-secondary stats svelte-1uha8ag"><!--[-->`);
		const each_array = ensure_array_like(stats);
		for (let i = 0, $$length = each_array.length; i < $$length; i++) {
			let stat = each_array[i];
			$$renderer.push(`<div><p class="mono svelte-1uha8ag">${escape_html(stat.label)}</p> <h3 class="svelte-1uha8ag">${escape_html(stat.value)}${escape_html(stat.unit)}</h3></div>`);
		}
		$$renderer.push(`<!--]--></section> `);
		UpcomingMatches($$renderer, { matches: data.upcoming });
		$$renderer.push(`<!---->`);
		bind_props($$props, { data });
	});
}
//#endregion
export { _page as default };
