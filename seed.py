import asyncio
from sqlalchemy.future import select
from loguru import logger
from app.database.session import AsyncSessionLocal
from app.models.base import Role

# Architectural RBAC Specification
# IDs are explicitly defined to guarantee referential integrity 
# when users are assigned default roles.
ROLES_DATA = [
    {
        "id": 1,
        "role_name": "Basic User",
        "permissions": {
            "tools": ["chat"],
            "base_monthly_credits": 50,
            "max_tokens_per_request": 2048
        }
    },
    {
        "id": 2,
        "role_name": "Premium User",
        "permissions": {
            "tools": ["chat", "image", "long_content"],
            "base_monthly_credits": 500,
            "max_tokens_per_request": 8192
        }
    },
    {
        "id": 3,
        "role_name": "Moderator",
        "permissions": {
            "admin_access": True,
            "view_audit_logs": True,
            "view_error_logs": True,
            "monitor_prompts": True
        }
    },
    {
        "id": 4,
        "role_name": "Admin",
        "permissions": {
            "admin_access": True,
            "manage_users": True,
            "manual_credit_override": True,
            "view_analytics": True
        }
    },
    {
        "id": 5,
        "role_name": "Super Admin",
        "permissions": {
            "admin_access": True,
            "platform_maintenance_lock": True,
            "create_admin_roles": True,
            "recycle_bin_access": True,
            "global_rate_limits": True
        }
    }
]

async def seed_roles():
    """
    Idempotent script to seed the database with core RBAC tiers.
    It checks for existing roles to prevent Duplicate Key errors.
    """
    logger.info("Initiating RBAC seeding protocol...")
    
    async with AsyncSessionLocal() as session:
        try:
            for role_data in ROLES_DATA:
                # 1. Check if the role ID already exists
                result = await session.execute(
                    select(Role).where(Role.id == role_data["id"])
                )
                existing_role = result.scalars().first()
                
                # 2. Insert if it does not exist
                if not existing_role:
                    new_role = Role(**role_data)
                    session.add(new_role)
                    logger.success(f"Staged Role: {role_data['role_name']}")
                else:
                    logger.info(f"Role already exists, skipping: {role_data['role_name']}")
            
            # 3. Commit the transaction atomically
            await session.commit()
            logger.info("Database transaction committed successfully. Seeding complete.")
            
        except Exception as e:
            await session.rollback()
            logger.error(f"Seeding failed. Transaction rolled back: {str(e)}")

if __name__ == "__main__":
    # Execute the async function
    asyncio.run(seed_roles())