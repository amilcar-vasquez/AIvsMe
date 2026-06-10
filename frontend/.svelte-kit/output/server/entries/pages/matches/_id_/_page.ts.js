import { t as worldCupApi } from "../../../../chunks/worldcup.js";
//#region src/routes/matches/[id]/+page.ts
var load = async ({ params, fetch }) => {
	const [match, predictions] = await Promise.all([worldCupApi.getMatch(params.id, fetch), worldCupApi.getMatchPredictions(params.id, fetch)]);
	return {
		match,
		aiPrediction: predictions.find((p) => p.predictor_type === "ai") ?? null,
		humanPrediction: predictions.find((p) => p.predictor_type === "human") ?? null
	};
};
//#endregion
export { load };
