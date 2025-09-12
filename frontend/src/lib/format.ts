export function formatKickoff(iso?: string | null) {
  if (!iso) return "TBD";
  const d = new Date(iso);
  // Show local time; adjust as you like
  return d.toLocaleString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit"
  });
}
