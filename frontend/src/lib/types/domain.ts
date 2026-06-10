export type UUID = string;

export type Team = {
  id: UUID;
  name: string;
  country_code: string;
  fifa_rank: number;
  group: string | null;
  created_at: string;
};

export type Match = {
  id: UUID;
  team_a: UUID;
  team_b: UUID;
  team_a_name: string;
  team_b_name: string;
  team_a_code: string;
  team_b_code: string;
  kickoff_time: string;
  stadium: string;
  stage: string;
  actual_score_a: number | null;
  actual_score_b: number | null;
  status: "upcoming" | "live" | "completed";
  created_at: string;
};

export type Prediction = {
  id: UUID;
  match: UUID;
  predictor_type: "human" | "ai";
  predicted_score_a: number;
  predicted_score_b: number;
  confidence_score: number;
  reasoning: string;
  created_at: string;
};

export type Scoreboard = {
  id: UUID;
  total_matches: number;
  human_points: number;
  ai_points: number;
  human_exact_scores: number;
  ai_exact_scores: number;
  last_updated: string;
};
