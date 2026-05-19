"""绒光公社 FastAPI 主应用 — Apple风格管理后台."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database import init_db
from routes.sheep_routes import register_sheep_routes
from routes.adoption_routes import register_adoption_routes


def create_app() -> FastAPI:
    app = FastAPI(title="绒光公社 API", version="1.0.0")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    @app.on_event("startup")
    def startup():
        init_db()

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "rongguang"}

    @app.get("/")
    def index():
        return FileResponse("static/index.html")

    register_sheep_routes(app)
    register_adoption_routes(app)

    # Trace route — simplified
    @app.get("/api/trace/{sheep_id}")
    def get_trace(sheep_id: str):
        from database import get_conn
        conn = get_conn()
        rows = conn.execute(
            "SELECT * FROM trace_log WHERE sheep_id=? ORDER BY timestamp ASC", (sheep_id,)
        ).fetchall()
        conn.close()
        return {"sheep_id": sheep_id, "stages": [dict(r) for r in rows]}

    @app.post("/api/trace/record")
    def record_trace(data: dict):
        from database import get_conn
        from datetime import datetime
        conn = get_conn()
        conn.execute(
            "INSERT INTO trace_log (sheep_id, stage, location, operator, data, timestamp) VALUES (?,?,?,?,?,?)",
            (data.get("sheep_id"), data.get("stage"), data.get("location",""),
             data.get("operator",""), data.get("data",""), datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()
        return {"message": "recorded"}

    return app


app = create_app()
