import asyncio
from sqlalchemy.future import select
from app.database.session import get_db
from app.models.base import Role

async def seed_roles():
    print("Connecting to the live Supabase database...")
    
    async for db in get_db():
        roles_data = [
            {"role_name": "free", "permissions": {"tools": ["chat"], "admin_access": False}},
            {"role_name": "starter", "permissions": {"tools": ["chat", "short_content"], "admin_access": False}},
            {"role_name": "pro", "permissions": {"tools": ["chat", "short_content", "image_generation", "long_form_content"], "admin_access": False}},
            {"role_name": "enterprise", "permissions": {"tools": ["chat", "short_content", "image_generation", "long_form_content"], "admin_access": True}}
        ]

        # 1. Fetch ALL roles
        result = await db.execute(select(Role))
        all_roles = result.scalars().all()
        existing_roles = {role.role_name: role for role in all_roles}

        # THE MAGIC FIX: Find the absolute highest ID currently in the database
        current_max_id = max([role.id for role in all_roles]) if all_roles else 0

        # 2. Process everything safely in memory
        for role_info in roles_data:
            if role_info["role_name"] in existing_roles:
                print(f"Role '{role_info['role_name']}' already exists. Updating permissions...")
                existing_roles[role_info["role_name"]].permissions = role_info["permissions"]
            else:
                print(f"Creating new role '{role_info['role_name']}'...")
                current_max_id += 1  # Manually step up the ID
                
                # We FORCE the ID here, completely bypassing the broken Postgres counter
                new_role = Role(
                    id=current_max_id, 
                    role_name=role_info["role_name"], 
                    permissions=role_info["permissions"]
                )
                db.add(new_role)

        # 3. Perform a single, atomic commit at the very end
        try:
            await db.commit()
            print("✅ Successfully synchronized roles with the database!")
        except Exception as e:
            print(f"Failed to commit. Rolling back to protect database. Error: {e}")
            await db.rollback()
        
        break 

if __name__ == "__main__":
    asyncio.run(seed_roles())