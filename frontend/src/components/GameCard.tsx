import { Game } from "../lib/types";

export default function GameCard({ game }: { game: Game }) {
  return (
    <div className="card p-5">
      <div className="text-slate-900 font-semibold">
        {game.away} @ {game.home}
      </div>
      <div className="text-sm text-slate-600 mt-1">
        Season {game.season}, Week {game.week}
        {game.venue && ` • ${game.venue}`}
      </div>
    </div>
  );
}
