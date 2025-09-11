import { useEffect, useState } from "react";
import api from "../lib/api";
import { Game } from "../lib/types";
import WeekSelector from "../components/WeekSelector";
import GameCard from "../components/GameCard";

export default function Games() {
  const [season, setSeason] = useState(2025);
  const [week, setWeek] = useState(1);
  const [games, setGames] = useState<Game[] | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    api.get("/api/games", { params: { season, week } })
      .then(res => setGames(res.data.results ?? res.data))
      .catch(() => setGames([]))
      .finally(() => setLoading(false));
  }, [season, week]);

  return (
    <div className="container-page">
      <div className="flex items-end justify-between mt-6 mb-4">
        <h2 className="text-xl font-semibold">Games</h2>
        <WeekSelector season={season} week={week} onChange={(s,w)=>{setSeason(s); setWeek(w);}} />
      </div>
      {loading && <div className="card p-6">Loading games…</div>}
      {!loading && (!games || games.length === 0) && <div className="card p-6">No games found.</div>}
      <div className="grid gap-4 md:grid-cols-2">
        {games?.map(g => <GameCard key={g.id} game={g} />)}
      </div>
    </div>
  );
}
