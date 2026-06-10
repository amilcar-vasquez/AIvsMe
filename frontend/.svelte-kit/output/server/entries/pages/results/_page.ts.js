import { t as worldCupApi } from "../../../chunks/worldcup.js";
//#region src/routes/results/+page.ts
var load = async ({ fetch }) => {
	const [scoreboard, completed] = await Promise.all([worldCupApi.getScoreboard(fetch), worldCupApi.getCompletedMatches(fetch)]);
	return {
		scoreboard,
		completed
	};
};
//#endregion
export { load };
