import asyncio
from sqlalchemy.future import select
from loguru import logger
from app.database.session import AsyncSessionLocal
from app.models.base import User

# The email you used to log in via Swagger
TARGET_EMAIL = "admin@aiflow.com" 

async def promote_to_super_admin():
    async with AsyncSessionLocal() as session:
        # Find your user record
        result = await session.execute(select(User).where(User.email == TARGET_EMAIL))
        user = result.scalars().first()
        
        if not user:
            logger.error(f"User {TARGET_EMAIL} not found in the database.")
            return

        # 1. Promote to Super Admin (Role 5)
        user.role_id = 5
        
        # 2. Grant functionally unlimited credits
        user.credits = 999999 
        
        await session.commit()
        logger.success(f"Successfully promoted {user.email} to Super Admin with {user.credits} credits.")

if __name__ == "__main__":
    asyncio.run(promote_to_super_admin())