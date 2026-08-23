/**
 * Two Spoons sync relay.
 *
 * It holds two small blobs — one per phone — and the meal photos, and hands them
 * back. That is the whole job. It cannot read any of it: everything is encrypted
 * on the phone before it is sent, with a key that never leaves the two devices.
 *
 * Each phone writes only its OWN key and reads only the other's, so two phones can
 * never overwrite each other. Photos are keyed by the entry they belong to and are
 * written once, so they cannot conflict either.
 *
 *   GET  /s/{room}/{who}      read a phone's state blob
 *   PUT  /s/{room}/{who}      write it
 *   GET  /p/{room}/{photoId}  read a meal photo
 *   PUT  /p/{room}/{photoId}  write one
 *   GET  /health              is it alive
 *
 * {room} is a random 32-character id created when the journey starts. Knowing it is
 * what grants access, which is why it is only ever shared inside the invite.
 */

const MAX_STATE  = 4 * 1024 * 1024;    // a state blob is normally a few KB
const MAX_PHOTO  = 2 * 1024 * 1024;    // photos are stored at ~40 KB; this is slack
const TTL_SECONDS = 60 * 60 * 24 * 400; // untouched data ages out after ~13 months

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, PUT, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
};

const reply = (body, status, extra) =>
  new Response(body, { status, headers: { ...CORS, "Cache-Control": "no-store", ...(extra || {}) } });

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") return reply(null, 204);

    const url = new URL(request.url);
    if (url.pathname === "/health") return reply("ok", 200);

    // /s/{room}/{who}  or  /p/{room}/{id}
    const m = url.pathname.match(/^\/(s|p)\/([a-zA-Z0-9]{16,64})\/([a-zA-Z0-9._-]{1,80})$/);
    if (!m) return reply("not found", 404);

    const [, kind, room, id] = m;
    const key = `${kind}:${room}:${id}`;

    if (request.method === "GET") {
      const value = await env.SYNC.get(key);
      if (value === null) return reply("", 404);
      return reply(value, 200, { "Content-Type": "text/plain; charset=utf-8" });
    }

    if (request.method === "PUT") {
      const body = await request.text();
      const limit = kind === "p" ? MAX_PHOTO : MAX_STATE;
      if (body.length === 0) return reply("empty", 400);
      if (body.length > limit) return reply("too large", 413);
      await env.SYNC.put(key, body, { expirationTtl: TTL_SECONDS });
      return reply("ok", 200);
    }

    return reply("method not allowed", 405);
  },
};
