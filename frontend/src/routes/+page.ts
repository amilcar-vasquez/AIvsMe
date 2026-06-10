import { worldCupApi } from "../lib/api/worldcup";
import type { Match, Scoreboard } from "../lib/types/domain";
import type { PageLoad } from "./$types";

const fallbackScoreboard: Scoreboard = {
  id: "local",
  total_matches: 0,
  human_points: 0,
  ai_points: 0,
  human_exact_scores: 0,
  ai_exact_scores: 0,
  last_updated: new Date().toISOString()
};

export const load: PageLoad = async ({ fetch }) => {
  let scoreboard = fallbackScoreboard;
  let upcoming: Match[] = [];

  try {
    [scoreboard, upcoming] = await Promise.all([
      worldCupApi.getScoreboard(fetch),
      worldCupApi.getUpcomingWindow(3, fetch)
    ]);
  } catch {
    // Fallback keeps dashboard renderable when API is offline.
  }

  return {
    scoreboard,
    upcoming
  };
};
