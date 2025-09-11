import { createContext, useContext, useMemo, useState, PropsWithChildren } from "react";
import { ParlayState, ParlayLegInput, defaultParlay } from "./parlay";

type Ctx = {
  parlay: ParlayState;
  addLeg: (leg: ParlayLegInput) => void;
  removeLeg: (idx: number) => void;
  clear: () => void;
  setStake: (s: number) => void;
};
const ParlayCtx = createContext<Ctx | null>(null);

export function ParlayProvider({ children }: PropsWithChildren) {
  const [parlay, setParlay] = useState<ParlayState>(defaultParlay);
  const api = useMemo<Ctx>(() => ({
    parlay,
    addLeg: (leg) => setParlay(p => ({...p, legs: [...p.legs, leg]})),
    removeLeg: (idx) => setParlay(p => ({...p, legs: p.legs.filter((_, i) => i!==idx)})),
    clear: () => setParlay(defaultParlay),
    setStake: (s) => setParlay(p => ({...p, stake: Math.max(0, s)})),
  }), [parlay]);
  return <ParlayCtx.Provider value={api}>{children}</ParlayCtx.Provider>;
}
export function useParlay() {
  const ctx = useContext(ParlayCtx);
  if (!ctx) throw new Error("useParlay must be used within ParlayProvider");
  return ctx;
}
