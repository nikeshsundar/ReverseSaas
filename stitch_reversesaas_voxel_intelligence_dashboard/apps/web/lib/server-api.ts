export function getApiBase(): string {
  const base = process.env.API_URL || "http://localhost:8000";
  return base.replace(/\/$/, "");
}
