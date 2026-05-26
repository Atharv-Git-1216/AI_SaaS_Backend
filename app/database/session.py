from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config.settings import settings

# 1. Create the async engine with Supabase PgBouncer fixes
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={
        "statement_cache_size": 0,             # Disables asyncpg statement caching
        "prepared_statement_cache_size": 0     # Required for Supabase PgBouncer
    }
)

# 2. Create the session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# 3. The dependency function used by your routes AND your seed script
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session