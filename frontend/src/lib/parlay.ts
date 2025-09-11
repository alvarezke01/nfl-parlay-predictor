export type ParlayLegInput = {
  model_prob: number;          // 0..1
  market_odds_american: number;
  label: string;               // UI label (e.g., "Eagles ML")
};
export type ParlayState = {
  stake: number;
  legs: ParlayLegInput[];
};
export const defaultParlay: ParlayState = { stake: 10, legs: [] };
