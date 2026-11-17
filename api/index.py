"""Vercel entry point. Vercel's disk is not persistent, so DATABASE_URL (Postgres) and SECRET_KEY are required."""
import os
import sys
from urllib.parse import parse_qsl, urlencode

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402

if os.environ.get("VERCEL") and not os.environ.get("DATABASE_URL"):
    raise RuntimeError("Set DATABASE_URL (a Postgres connection string) in the Vercel project settings.")

_flask = create_app()


def app(environ, start_response):
    """vercel.json rewrites every URL to /api/index?__p=<original path>; restore the real path for Flask."""
    pairs = parse_qsl(environ.get("QUERY_STRING", ""), keep_blank_values=True)
    p = None
    rest = []
    for k, v in pairs:
        if k == "__p" and p is None:
            p = v
        else:
            rest.append((k, v))
    if p is not None:
        environ["PATH_INFO"] = "/" + p.lstrip("/")
        environ["QUERY_STRING"] = urlencode(rest)
    elif environ.get("PATH_INFO", "").startswith("/api/index"):
        environ["PATH_INFO"] = "/"
    seen = {}

    def sr(status, headers, exc_info=None):
        seen["status"] = status
        return start_response(status, headers, exc_info)

    body = _flask(environ, sr)
    if os.environ.get("CREW_DEBUG404") and seen.get("status", "").startswith("404"):
        info = "\n".join(f"{k}={environ.get(k)}" for k in ("PATH_INFO", "QUERY_STRING", "REQUEST_URI", "RAW_URI", "SCRIPT_NAME", "HTTP_X_VERCEL_ID", "HTTP_X_MATCHED_PATH", "HTTP_X_VERCEL_DEPLOYMENT_URL"))
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [info.encode()]
    return body
