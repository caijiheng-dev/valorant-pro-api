from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )


class Team(Base):
    """战队表"""
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="战队ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="战队名")
    region: Mapped[str] = mapped_column(String(20), comment="赛区: CN / NA / EMEA / APAC / KR")
    logo_url: Mapped[Optional[str]] = mapped_column(String(255), comment="战队Logo")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', region='{self.region}')>"


class Player(Base):
    """职业选手表"""
    __tablename__ = "player"

    __table_args__ = (
        Index("fk_player_team_idx", "team_id"),
        Index("idx_player_role", "role"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="选手ID")
    ign: Mapped[str] = mapped_column(String(50), nullable=False, comment="游戏内ID")
    real_name: Mapped[Optional[str]] = mapped_column(String(50), comment="真实姓名")
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("team.id"), nullable=False, comment="所属战队")
    role: Mapped[str] = mapped_column(
        String(20),
        comment="位置: duelist(决斗) / controller(控场) / initiator(先锋) / sentinel(哨位)"
    )
    nationality: Mapped[Optional[str]] = mapped_column(String(50), comment="国籍")
    birthday: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="生日")
    photo_url: Mapped[Optional[str]] = mapped_column(String(255), comment="选手照片")
    dpi: Mapped[Optional[int]] = mapped_column(Integer, comment="鼠标DPI")
    sensitivity: Mapped[Optional[float]] = mapped_column(nullable=True, comment="游戏内灵敏度")
    crosshair_code: Mapped[Optional[str]] = mapped_column(String(500), comment="准星代码(游戏内可导入)")
    achievements: Mapped[Optional[str]] = mapped_column(Text, comment="生涯成就(纯文本)")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")

    def __repr__(self):
        return f"<Player(id={self.id}, ign='{self.ign}', team_id={self.team_id})>"
