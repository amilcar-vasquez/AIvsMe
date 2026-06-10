// @ts-nocheck
import { worldCupApi } from "../../../lib/api/worldcup";
import type { PageLoad } from "./$types";

export const load = async ({ params, fetch }: Parameters<PageLoad>[0]) => {
  const [match, predictions] = await Promise.all([
    worldCupApi.getMatch(params.id, fetch),
    worldCupApi.getMatchPredictions(params.id, fetch)
  ]);

  const aiPrediction = predictions.find((p) => p.predictor_type === "ai") ?? null;
  const humanPrediction = predictions.find((p) => p.predictor_type === "human") ?? null;

  return {
    match,
    aiPrediction,
    humanPrediction
  };
};
