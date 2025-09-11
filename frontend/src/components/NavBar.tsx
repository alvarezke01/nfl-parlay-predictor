import { NavLink } from "react-router-dom";

const linkBase = "px-3 py-2 rounded-lg text-sm font-medium";
const linkInactive = "text-slate-600 hover:text-slate-900 hover:bg-slate-100";
const linkActive = "text-white bg-brand-accent hover:bg-brand-accentDark";

export default function NavBar() {
  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="container-page h-14 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-7 w-7 rounded-lg bg-brand-accent"></div>
          <span className="font-semibold text-slate-900">NFL Parlay Predictor</span>
        </div>
        <div className="flex items-center gap-2">
          <NavLink to="/" className={({isActive}) => `${linkBase} ${isActive?linkActive:linkInactive}`}>Home</NavLink>
          <NavLink to="/games" className={({isActive}) => `${linkBase} ${isActive?linkActive:linkInactive}`}>Games</NavLink>
          <NavLink to="/parlays" className={({isActive}) => `${linkBase} ${isActive?linkActive:linkInactive}`}>Parlays</NavLink>
          <NavLink to="/analytics" className={({isActive}) => `${linkBase} ${isActive?linkActive:linkInactive}`}>Analytics</NavLink>
        </div>
      </div>
    </nav>
  );
}
