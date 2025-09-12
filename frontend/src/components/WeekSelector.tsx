import { useState } from "react";

type Props = { season: number; week: number; onChange: (s: number, w: number) => void };

export default function WeekSelector({ season, week, onChange }: Props) {
  const [s, setS] = useState(season);
  const [w, setW] = useState(week);
  return (
    <div className="flex gap-2">
      <select
        className="border rounded-lg px-3 py-2 bg-white text-sm"
        value={s}
        onChange={(e)=>{ const v=Number(e.target.value); setS(v); onChange(v,w); }}>
        {[2023,2024,2025].map(y=> <option key={y} value={y}>Season {y}</option>)}
      </select>
      <select
        className="border rounded-lg px-3 py-2 bg-white text-sm"
        value={w}
        onChange={(e)=>{ const v=Number(e.target.value); setW(v); onChange(s,v); }}>
        {Array.from({length:18},(_,i)=>i+1).map(wk => <option key={wk} value={wk}>Week {wk}</option>)}
      </select>
    </div>
  );
}
