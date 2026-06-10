import { t as worldCupApi } from "../../chunks/worldcup.js";
//#region src/routes/+page.ts
var fallbackScoreboard = {
	id: "local",
	total_matches: 0,
	human_points: 0,
	ai_points: 0,
	human_exact_scores: 0,
	ai_exact_scores: 0,
	last_updated: (/* @__PURE__ */ new Date()).toISOString()
};
var load = async ({ fetch }) => {
	let scoreboard = fallbackScoreboard;
	let upcoming = [];
	try {
		[scoreboard, upcoming] = await Promise.all([worldCupApi.getScoreboard(fetch), worldCupApi.getUpcomingMatches(fetch)]);
	} catch {}
	return {
		scoreboard,
		upcoming
	};
};
//#endregion
export { load };
