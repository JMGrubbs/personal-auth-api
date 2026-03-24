from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from core.security import verify_password

async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, email: str, hashed_password: str) -> User:
    new_user = User(email=email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

async def update_user(session: AsyncSession, user: User) -> User:
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def delete_user(session: AsyncSession, user: User) -> bool:
    await session.delete(user)
    await session.commit()
    return True

async def check_user_exists(session: AsyncSession, email: str) -> bool:
    result = await session.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none() is not None

async def login_user(session: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(session, email)
    if user:
        verified_pass = verify_password(plain_password=password, hashed_password=user.hashed_password) if user else False
        if verified_pass:
            return user
        return None
    return None
