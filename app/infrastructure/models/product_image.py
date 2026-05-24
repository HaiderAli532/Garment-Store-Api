import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, TimestampedMixin

if TYPE_CHECKING:
    from app.infrastructure.models.product import Product


class ProductImage(TimestampedMixin, Base):
    __tablename__ = "product_images"
    __table_args__ = (
        Index("ix_product_images_product_id", "product_id"),
        UniqueConstraint(
            "product_id",
            "sort_order",
            name="uq_product_images_product_id_sort_order",
        ),
        Index(
            "uq_product_images_one_primary_per_product",
            "product_id",
            unique=True,
            postgresql_where=text("is_primary IS TRUE"),
        ),
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    alt_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    product: Mapped["Product"] = relationship("Product", back_populates="images")
