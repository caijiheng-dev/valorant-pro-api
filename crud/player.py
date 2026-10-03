from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.player import Team, Player


# 获取战队列表
async def get_teams(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Team).order_by(Team.sort_order).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# 查询选手列表
async def get_players(
        db: AsyncSession,
        team_id: int = 0,
        skip: int = 0,
        limit: int = 10):
    stmt = select(Player)
    if team_id != 0:
        stmt = stmt.where(Player.team_id == team_id)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# 查询选手总数
async def get_player_count(db: AsyncSession, team_id: int = 0):
    stmt = select(func.count()).select_from(Player)
    if team_id != 0:
        stmt = stmt.where(Player.team_id == team_id)
    result = await db.execute(stmt)
    return result.scalar_one()


# 按id查选手
async def get_player_by_id(db: AsyncSession, player_id: int):
    stmt = select(Player).where(Player.id == player_id)
    result = await db.execute(stmt)
    return result.scalars().first()


# 浏览量+1
async def increase_views(db: AsyncSession, player_id: int):
    stmt = update(Player).where(Player.id == player_id).values(views=Player.views + 1)
    await db.execute(stmt)


# 同战队其他选手(相关推荐)
async def get_related_players(db: AsyncSession, player_id: int, team_id: int, limit: int = 5):
    stmt = select(Player).where(
        Player.id != player_id,
        Player.team_id == team_id
    ).order_by(Player.views.desc()).limit(limit)
    result = await db.execute(stmt)
    return [
        {"id": p.id, "ign": p.ign, "role": p.role, "photoUrl": p.photo_url}
        for p in result.scalars().all()
    ]
