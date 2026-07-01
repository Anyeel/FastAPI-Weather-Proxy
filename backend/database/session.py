from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.core.config import settings

# Source of connections to the DB.
engine = create_async_engine(
    settings.database_url,
    echo=True,  # Set to allow terminal debug
)

# A factory that generates new Session objects for each request.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    """
    Dependency that provides a database session to be used in a single request.
    It ensures the session is closed after the request is finished.
    """
    async with AsyncSessionLocal() as session:
        yield session
