import { Game } from "../lib/types";
import { formatKickoff } from "../lib/format";

type Props = {
  game: Game;
  homeName: string;
  awayName: string;
};

export default function GameCard({ game, homeName, awayName }: Props) {
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between">
        <div className="text-slate-900 font-semibold">
          {awayName} @ {homeName}
        </div>
        <div className="text-xs text-slate-500">{formatKickoff(game.kickoff)}</div>
      </div>
      <div className="text-xs text-slate-500 mt-1">
        Season {game.season} • Week {game.week} {game.venue ? `• ${game.venue}` : "" }
      </div>
      {/* Odds & predictions will slot in below on the next commit */}
    </div>
  );
}
