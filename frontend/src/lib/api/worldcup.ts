import type { Match, Prediction, Scoreboard } from "../types/domain";
import { apiGet, apiPost } from "./client";

export const worldCupApi = {
  getScoreboard(fetchFn: typeof fetch) {
    return apiGet<Scoreboard>("/scoreboard/", fetchFn);
  },
  getUpcomingMatches(fetchFn: typeof fetch) {
    return apiGet<Match[]>("/matches/upcoming/", fetchFn);
  },
  getCompletedMatches(fetchFn: typeof fetch) {
    return apiGet<Match[]>("/matches/completed/", fetchFn);
  },
  getMatch(matchId: string, fetchFn: typeof fetch) {
    return apiGet<Match>(`/matches/${matchId}/`, fetchFn);
  },
  getMatchPredictions(matchId: string, fetchFn: typeof fetch) {
    return apiGet<Prediction[]>(`/matches/${matchId}/predictions/`, fetchFn);
  },
  listPredictions(fetchFn: typeof fetch) {
    return apiGet<Prediction[]>("/predictions/", fetchFn);
  },
  createPrediction(
    payload: {
      match: string;
      predictor_type: "human" | "ai";
      predicted_score_a: number;
      predicted_score_b: number;
      confidence_score?: number;
      reasoning?: string;
    },
    fetchFn: typeof fetch
  ) {
    return apiPost<Prediction>("/predictions/", payload, fetchFn);
  },
  setMatchResult(
    matchId: string,
    payload: { actual_score_a: number; actual_score_b: number },
    fetchFn: typeof fetch
  ) {
    return apiPost<{
      match: Match;
      scoreboard: Omit<Scoreboard, "id" | "last_updated">;
    }>(`/matches/${matchId}/set-result/`, payload, fetchFn);
  }
};
