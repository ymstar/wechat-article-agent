import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import logging

logger = logging.getLogger(__name__)

MAX_RETRY_TIME = 20  # 连接最大重试时间（秒）


def get_db_url() -> str:
    """
    Build database URL from environment.
    支持 PostgreSQL 连接字符串
    """
    # 优先从环境变量读取
    url = os.getenv("PGDATABASE_URL") or ""
    
    if url and url.strip():
        return url
    
    # 尝试其他常见的 PostgreSQL 环境变量
    pg_url = os.getenv("DATABASE_URL") or ""
    if pg_url and pg_url.strip():
        return pg_url
    
    # PostgreSQL 标准环境变量
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    database = os.getenv("PGDATABASE", "postgres")
    user = os.getenv("PGUSER", "postgres")
    password = os.getenv("PGPASSWORD", "")
    
    if password:
        url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    else:
        url = f"postgresql://{user}@{host}:{port}/{database}"
    
    return url


_engine = None
_SessionLocal = None


def _create_engine_with_retry():
    url = get_db_url()
    
    # 如果没有配置数据库，返回None让调用方处理
    if not url or url == "":
        logger.warning("Database URL not configured, will use in-memory storage")
        return None
    
    try:
        size = int(os.getenv("DB_POOL_SIZE", "10"))
        overflow = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    except ValueError:
        size = 10
        overflow = 20
    
    recycle = 1800
    timeout = 30
    
    try:
        engine = create_engine(
            url,
            pool_size=size,
            max_overflow=overflow,
            pool_pre_ping=True,
            pool_recycle=recycle,
            pool_timeout=timeout,
        )
        
        # 验证连接，带重试
        start_time = time.time()
        last_error = None
        
        while time.time() - start_time < MAX_RETRY_TIME:
            try:
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                return engine
            except OperationalError as e:
                last_error = e
                elapsed = time.time() - start_time
                logger.warning(f"Database connection failed, retrying... (elapsed: {elapsed:.1f}s)")
                time.sleep(min(1, MAX_RETRY_TIME - elapsed))
        
        logger.error(f"Database connection failed after {MAX_RETRY_TIME}s: {last_error}")
        return None
        
    except Exception as e:
        logger.warning(f"Failed to create database engine: {e}")
        return None


def get_engine():
    global _engine
    if _engine is None:
        _engine = _create_engine_with_retry()
    return _engine


def get_sessionmaker():
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        if engine is None:
            raise RuntimeError("Database not configured. Set PGDATABASE_URL or use in-memory storage.")
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal


def get_session():
    return get_sessionmaker()()


__all__ = [
    "get_db_url",
    "get_engine",
    "get_sessionmaker",
    "get_session",
]
