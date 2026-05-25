"""
CRUD operations for User model
"""

from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserCRUD:
    """CRUD operations for User model"""

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username"""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_multi(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """Get multiple users"""
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, user_create: UserCreate) -> User:
        """Create new user"""
        hashed_password = get_password_hash(user_create.password)

        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
            is_active=user_create.is_active,
        )

        try:
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            await db.rollback()
            raise ValueError("User with this email or username already exists") from e

    @staticmethod
    async def update(
        db: AsyncSession, user_id: int, user_update: UserUpdate
    ) -> Optional[User]:
        """Update user"""
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()

        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(db_user, field, value)

        try:
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            await db.rollback()
            raise ValueError("User with this email or username already exists") from e

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> bool:
        """Delete user"""
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()

        if not db_user:
            return False

        await db.delete(db_user)
        await db.commit()
        return True

    @staticmethod
    async def authenticate(
        db: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        """Authenticate user"""
        user = await UserCRUD.get_by_username(db, username)
        if not user:
            user = await UserCRUD.get_by_email(db, username)

        if not user or not verify_password(password, user.hashed_password):
            return None

        return user


# Create instance
user_crud = UserCRUD()
