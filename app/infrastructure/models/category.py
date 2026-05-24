import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import ActivatableTimestampedMixin, Base

if TYPE_CHECKING:
    from app.infrastructure.models.product import Product


class Category(ActivatableTimestampedMixin, Base):
    __tablename__ = "categories"
    __table_args__ = (
        Index("ix_categories_parent_id", "parent_id"),
        Index("ix_categories_is_active_parent_id", "is_active", "parent_id"),
    )

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0, server_default="0", nullable=False)

    parent: Mapped["Category | None"] = relationship(
        "Category",
        remote_side=[id],
        back_populates="children",
    )
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
    )
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
    )
