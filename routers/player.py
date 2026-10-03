from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import player

router = APIRouter(prefix="/api/players", tags=["players"])


@router.get("/teams")
async def get_teams(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    teams = await player.get_teams(db, skip, limit)
    return {"code": 200, "message": "获取战队列表成功", "data": teams}


@router.get("/list")
async def get_player_list(
    team_id: int = Query(0, alias="teamId"),
    page: int = Query(1),
    page_size: int = Query(10, le=100, alias="pageSize"),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    players = await player.get_players(db, team_id, offset, page_size)
    total = await player.get_player_count(db, team_id)
    has_more = "有更多数据" if (offset + len(players)) < total else "没有更多数据"
    return {
        "code": 200,
        "message": "获取选手列表成功",
        "data": {"list": players, "total": total, "hasMore": has_more}
    }


@router.get("/detail")
async def get_player_detail(player_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    p = await player.get_player_by_id(db, player_id)
    if p is None:
        raise HTTPException(status_code=404, detail="选手不存在")
    await player.increase_views(db, player_id)
    await db.refresh(p)
    related = await player.get_related_players(db, player_id, p.team_id)
    return {
        "code": 200,
        "message": "获取选手详情成功",
        "data": {
            "id": p.id,
            "ign": p.ign,
            "realName": p.real_name,
            "role": p.role,
            "nationality": p.nationality,
            "birthday": p.birthday.strftime("%Y-%m-%d") if p.birthday else None,
            "photoUrl": p.photo_url,
            "dpi": p.dpi,
            "sensitivity": p.sensitivity,
            "crosshairCode": p.crosshair_code,
            "achievements": p.achievements,
            "views": p.views,
            "relatedPlayers": related,
        }
    }
