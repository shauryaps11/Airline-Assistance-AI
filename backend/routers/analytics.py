from fastapi import APIRouter
from backend.database import get_conn

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("")
async def get_analytics():
    conn = get_conn()

    total_sessions = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    total_messages = conn.execute("SELECT COUNT(*) FROM messages WHERE role='assistant'").fetchone()[0]
    escalated_count = conn.execute("SELECT COUNT(*) FROM messages WHERE role='assistant' AND escalated=1").fetchone()[0]

    resolution_rate = round(1 - (escalated_count / total_messages), 3) if total_messages > 0 else 1.0

    avg_tools_row = conn.execute("""
        SELECT AVG(tool_count) FROM (
            SELECT session_id, SUM(CASE WHEN tools_used IS NOT NULL AND tools_used != 'null' THEN
                (LENGTH(tools_used) - LENGTH(REPLACE(tools_used, ',', ''))) + 1 ELSE 0 END) AS tool_count
            FROM messages WHERE role='assistant'
            GROUP BY session_id
        )
    """).fetchone()
    avg_tools = round(avg_tools_row[0] or 0, 2)

    intent_rows = conn.execute("""
        SELECT intent, COUNT(*) as cnt FROM messages
        WHERE role='assistant' AND intent IS NOT NULL
        GROUP BY intent ORDER BY cnt DESC
    """).fetchall()
    intent_distribution = {r["intent"]: r["cnt"] for r in intent_rows}

    escalation_rows = conn.execute("""
        SELECT trigger, COUNT(*) as cnt FROM escalations GROUP BY trigger
    """).fetchall()
    escalation_by_trigger = {r["trigger"]: r["cnt"] for r in escalation_rows}

    daily_rows = conn.execute("""
        SELECT DATE(timestamp) as day, COUNT(*) as cnt
        FROM messages WHERE role='user'
        AND timestamp >= DATE('now', '-30 days')
        GROUP BY day ORDER BY day
    """).fetchall()
    daily_messages = [{"day": r["day"], "count": r["cnt"]} for r in daily_rows]

    conn.close()

    return {
        "total_sessions": total_sessions,
        "total_messages": total_messages,
        "escalated_count": escalated_count,
        "resolution_rate": resolution_rate,
        "avg_tools_per_session": avg_tools,
        "intent_distribution": intent_distribution,
        "escalation_by_trigger": escalation_by_trigger,
        "daily_messages": daily_messages,
    }
