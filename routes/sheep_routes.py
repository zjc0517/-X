"""羊只管理路由."""

import uuid
from datetime import datetime
from database import get_conn
from fastapi import HTTPException


def register_sheep_routes(app):
    @app.get("/api/sheep/list")
    def list_sheep(status: str = None):
        conn = get_conn()
        if status:
            rows = conn.execute("SELECT * FROM sheep WHERE status=? ORDER BY created_at DESC LIMIT 50", (status,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM sheep ORDER BY created_at DESC LIMIT 50").fetchall()
        result = [dict(r) for r in rows]
        conn.close()
        return result

    @app.get("/api/sheep/{sheep_id}")
    def get_sheep(sheep_id: str):
        conn = get_conn()
        row = conn.execute("SELECT * FROM sheep WHERE sheep_id=?", (sheep_id,)).fetchone()
        conn.close()
        if not row:
            raise HTTPException(404, "sheep not found")
        return dict(row)

    @app.post("/api/sheep/create")
    def create_sheep(data: dict):
        sid = f"RG-SH-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
        conn = get_conn()
        conn.execute("""INSERT INTO sheep (sheep_id, name, breed, ranch_id, birth_date, gender, weight_kg, price, status, image_url, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (sid, data.get("name",""), data.get("breed","乌珠穆沁羊"), data.get("ranch_id","RG-RCH-001"),
             data.get("birth_date","2025-09-15"), data.get("gender","female"), data.get("weight_kg",35.0),
             data.get("price",2999.0), "available", data.get("image_url",""), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return {"sheep_id": sid, "message": "created"}
