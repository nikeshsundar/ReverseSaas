import { NextResponse } from "next/server";

import { getApiBase } from "@/lib/server-api";

export const dynamic = "force-dynamic";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const base = getApiBase();
  const response = await fetch(`${base}/technology/${id}`, {
    cache: "no-store"
  });
  const payload = await response.json().catch(() => ({}));
  return NextResponse.json(payload, { status: response.status });
}
