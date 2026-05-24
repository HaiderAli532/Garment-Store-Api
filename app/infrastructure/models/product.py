import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import ActivatableTimestampedMixin, Base

if TYPE_CHECKING:
    from app.infrastructure.models.category import Category
    from app.infrastructure.models.order_item import OrderItem
    from app.infrastructure.models.product_image import ProductImage
    from app.infrastructure.models.product_size import ProductSize


class Product(ActivatableTimestampedMixin, Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price >= 0", name="price_non_negative"),
        CheckConstraint(
            "rating IS NULL OR (rating >= 0 AND rating <= 5)",
            name="rating_in_range",
        ),
        Index("ix_products_category_id", "category_id"),
        Index("ix_products_is_active_category_id", "is_active", "category_id"),
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    rating: Mapped[Decimal | None] = mapped_column(Numeric(2, 1), nullable=True)

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    images: Mapped[list["ProductImage"]] = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="ProductImage.sort_order",
    )
    sizes: Mapped[list["ProductSize"]] = relationship(
        "ProductSize",
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="ProductSize.sort_order",
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product",
    )
