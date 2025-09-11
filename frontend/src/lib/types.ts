export type Team = { id: number; name: string; conference: string; division: string };
export type Game = {
  id: number;
  season: number;
  week: number;
  home_team: number;
  away_team: number;
  kickoff: string;
  venue?: string | null;
};
export type Odds = {
  id: number;
  game: number;
  book: string;
  spread: number | null;
  spread_price: number | null;
  total: number | null;
  total_price: number | null;
  moneyline_home: number | null;
  moneyline_away: number | null;
  captured_at: string;
};
export type Prediction = {
  id: number;
  game: number;
  win_prob_home: number;
  win_prob_away: number;
  spread_cover_home: number | null;
  spread_cover_away: number | null;
  expected_total: number | null;
  model_version: string;
  generated_at: string;
};
