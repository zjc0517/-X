"""认养管理路由."""

import uuid
from datetime import datetime
from database import get_conn
from fastapi import HTTPException


def register_adoption_routes(app):
    @app.post("/api/adoption/apply")
    def apply_adoption(data: dict):
        sid = data.get("sheep_id")
        conn = get_conn()
        sheep = conn.execute("SELECT * FROM sheep WHERE sheep_id=?", (sid,)).fetchone()
        if not sheep:
            conn.close()
            raise HTTPException(404, "sheep not found")
        if sheep["status"] != "available":
            conn.close()
            raise HTTPException(400, f"sheep is {sheep['status']}")

        aid = f"RG-ADOPT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
        conn.execute("""INSERT INTO adoption (adoption_id, sheep_id, adopter_name, adopter_phone, adopter_address, price, duration_months, status, created_at)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (aid, sid, data.get("adopter_name",""), data.get("adopter_phone",""),
             data.get("adopter_address",""), sheep["price"], data.get("duration_months",12),
             "active", datetime.now().isoformat()))
        conn.execute("UPDATE sheep SET status='adopted' WHERE sheep_id=?", (sid,))
        conn.commit()
        conn.close()
        return {"adoption_id": aid, "message": "adopted", "sheep_name": sheep["name"]}

    @app.get("/api/adoption/list")
    def list_adoptions():
        conn = get_conn()
        rows = conn.execute("SELECT * FROM adoption ORDER BY created_at DESC LIMIT 50").fetchall()
        result = [dict(r) for r in rows]
        conn.close()
        return result

    @app.get("/api/adoption/{adoption_id}")
    def get_adoption(adoption_id: str):
        conn = get_conn()
        row = conn.execute("SELECT * FROM adoption WHERE adoption_id=?", (adoption_id,)).fetchone()
        conn.close()
        if not row:
            raise HTTPException(404, "adoption not found")
        return dict(row)
