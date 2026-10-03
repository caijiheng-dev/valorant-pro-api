from fastapi import APIRouter, HTTPException
from pydantic import Field
from config.db_config import get_db
from crud import news
from fastapi import Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession

#创建APIRouter实例
#prefix 路由前缀（API接口规范文档）
router = APIRouter(prefix="/api/news", tags=["news"])


#接口实现流程
#1、模块化路由->API接口规范文档
#2、定义模型类->数据库表（数据库设计文档）
#3、在curd文件夹里面创建文件、封装操作数据库的方法
#4、在路由处理函数里面调用crud封装好的方法，响应结果



@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100,db:AsyncSession = Depends(get_db)):
    #先获取数据库内新闻分类数据->先定义模型类->封装查询数据的方法
    categories = await news.get_categories(db,skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data":categories
    }

@router.get("/list")
async def get_news_list(
    category_id: int = Query(..., alias="categoryId"),
    page: int = Query(1),
    page_size: int = Query(10, le=100, alias="pageSize"),
    db: AsyncSession = Depends(get_db)
):
    #思路：处理分页规则->查询新闻列表->计算总量->计算是否还有更多
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db,category_id,offset,page_size)
    total = await news.get_news_count(db,category_id)
    #（跳过的+当前列表的）<总量
    if (offset+len(news_list))<total:
        has_more = "有更多数据"
    else:
        has_more = "没有更多数据"
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data":{
            "list":news_list,
            "total":total,
            "hasMore":has_more
        }
    }

@router.get("/detail")
async def get_news_detail(news_id:int = Query(...,alias="id"),db:AsyncSession = Depends(get_db)):
    #查详情必须用 get_id_news（按主键查单个对象），不能用 get_news_list（那是查列表）
    news_detail = await news.get_id_news(db,news_id)
    if news_detail is None:
        raise HTTPException(status_code=404,detail = "新闻不存在")
    await news.update_news_views(db,news_id)
    await db.refresh(news_detail)
    related_news = await news.get_related_news(db,news_id,news_detail.category_id)
    return{
        "code": 200,
        "message":"显示成功",
        "data":{
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":related_news
        }
    }
