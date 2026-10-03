from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News

#提取全部内容
async def get_categories(db:AsyncSession,skip: int = 0, limit: int = 10):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

#查询新闻列表
async def get_news_list(
        db:AsyncSession,
        category_id:int,
        skip: int = 0,
        limit: int = 10):
    #查询新闻列表：category_id 为 0 表示"全部"（不过滤分类），否则按分类查询
    stmt = select(News)
    if category_id != 0:
        stmt = stmt.where(News.category_id == category_id)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

#查询新闻总数
async def get_news_count(db:AsyncSession,category_id:int):
    #查询新闻总数：category_id 为 0 表示"全部"（不过滤分类），否则按分类统计
    #注意：select(func.count()) 必须用 select_from(News) 指定表，
    #否则生成的 SQL 是 "SELECT COUNT(*) "（无 FROM），MySQL 会固定返回 1
    stmt = select(func.count()).select_from(News)
    if category_id != 0:
        stmt = stmt.where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  #只能有一个结果，否则报错

#按id查询新闻
async def get_id_news(db:AsyncSession,news_id:int):
    #注意：select() 必须指定 News 表，否则报错；scalars().first() 返回单个 News 对象（找不到返回 None）
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalars().first()

#修改浏览量
async def update_news_views(db:AsyncSession,news_id:int):
    stmt = update(News).where(News.id == news_id).values(views=News.views+1)
    result = await db.execute(stmt)
    #更新时要检查数据库是否真的命中了数据
    return result.rowcount > 0

#查询同类新闻
async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit: int = 5):
    #order_by 排序->浏览量最多和发布时间最新
    stmt = select(News).where(
        News.id != news_id,
        News.category_id == category_id
    ).order_by(
        News.views.desc(),#默认升序，desc代表降序
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()
    related_news = result.scalars().all()
    #列表推导式 推导出核心数据
    return [{"title":news_detail.title,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time
             }for news_detail in related_news]