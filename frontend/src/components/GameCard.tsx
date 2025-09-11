import { Game } from "../lib/types";

export default function GameCard({ game }: { game: Game }) {
  return (
    <div className="card p-5">
      <div className="text-slate-900 font-semibold">
        Game #{game.id} — Season {game.season}, Week {game.week}
      </div>
      <div className="text-sm text-slate-600 mt-1">
        Home team {game.home_team}, Away team {game.away_team}
      </div>
    </div>
  );
}
