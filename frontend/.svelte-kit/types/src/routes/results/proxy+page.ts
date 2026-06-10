// @ts-nocheck
import { worldCupApi } from "../../lib/api/worldcup";
import type { PageLoad } from "./$types";

export const load = async ({ fetch }: Parameters<PageLoad>[0]) => {
  const [scoreboard, completed] = await Promise.all([
    worldCupApi.getScoreboard(fetch),
    worldCupApi.getCompletedMatches(fetch)
  ]);

  return {
    scoreboard,
    completed
  };
};
