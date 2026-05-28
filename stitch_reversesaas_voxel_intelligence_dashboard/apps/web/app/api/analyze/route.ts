import { NextResponse } from "next/server";

import { getApiBase } from "@/lib/server-api";

export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  const base = getApiBase();
  const body = await request.json();

  const response = await fetch(`${base}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    cache: "no-store"
  });

  const payload = await response.json().catch(() => ({}));
  return NextResponse.json(payload, { status: response.status });
}
