import { NextResponse } from "next/server";

import { getApiBase } from "@/lib/server-api";

export const dynamic = "force-dynamic";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const base = getApiBase();
  const response = await fetch(`${base}/analysis/${id}/report`, {
    cache: "no-store"
  });
  const buffer = await response.arrayBuffer();
  const headers = new Headers();
  headers.set("Content-Type", "application/pdf");
  const disposition = response.headers.get("Content-Disposition");
  if (disposition) {
    headers.set("Content-Disposition", disposition);
  }
  return new NextResponse(buffer, { status: response.status, headers });
}
