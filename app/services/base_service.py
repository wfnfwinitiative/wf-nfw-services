from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from security import hash_password


async def create_record(db: AsyncSession, model, data):
    input_params = data.dict()
    if model.__tablename__ == "users":
        password = input_params.pop("password", None)
        if not password:
            raise Exception("Password is required")

        input_params["password_hash"] = hash_password(password)

    obj = model(**input_params)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_record(db: AsyncSession, model, record_id, id_field):
    result = await db.execute(
        select(model).where(getattr(model, id_field) == record_id)
    )
    return result.scalar_one_or_none()


async def get_all_records(db: AsyncSession, model):
    result = await db.execute(select(model))
    return result.scalars().all()


async def delete_record(db: AsyncSession, model, record_id, id_field):
    obj = await get_record(db, model, record_id, id_field)
    if not obj:
        return None
    await db.delete(obj)
    await db.commit()
    return {"message": "Deleted successfully"}
