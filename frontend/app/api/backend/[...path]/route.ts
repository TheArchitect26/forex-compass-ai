import { NextRequest, NextResponse } from "next/server";

const backendBase = (
  process.env.BACKEND_API_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000"
).replace(/\/$/, "");

type RouteContext = {
  params: Promise<{ path: string[] }>;
};

async function proxy(req: NextRequest, context: RouteContext) {
  const { path } = await context.params;
  const incomingUrl = new URL(req.url);
  const targetPath = path.join("/");
  const targetUrl = `${backendBase}/${targetPath}${incomingUrl.search}`;

  const headers = new Headers();
  const contentType = req.headers.get("content-type");
  const authorization = req.headers.get("authorization");
  const accept = req.headers.get("accept");

  if (contentType) headers.set("content-type", contentType);
  if (authorization) headers.set("authorization", authorization);
  if (accept) headers.set("accept", accept);

  try {
    const body =
      req.method === "GET" || req.method === "HEAD"
        ? undefined
        : await req.arrayBuffer();

    const response = await fetch(targetUrl, {
      method: req.method,
      headers,
      body,
      cache: "no-store",
    });

    const responseBody = await response.arrayBuffer();
    const responseHeaders = new Headers();
    const responseType = response.headers.get("content-type");

    if (responseType) responseHeaders.set("content-type", responseType);

    return new Response(responseBody, {
      status: response.status,
      statusText: response.statusText,
      headers: responseHeaders,
    });
  } catch (err) {
    return NextResponse.json(
      {
        detail: "Backend proxy fetch failed",
        error: err instanceof Error ? err.message : String(err),
      },
      { status: 502 }
    );
  }
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
