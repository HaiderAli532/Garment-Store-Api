import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, TimestampedMixin

if TYPE_CHECKING:
    from app.infrastructure.models.product import Product


class ProductSize(TimestampedMixin, Base):
    __tablename__ = "product_sizes"
    __table_args__ = (
        UniqueConstraint("product_id", "size_label", name="uq_product_sizes_product_id_size_label"),
        Index("ix_product_sizes_product_id", "product_id"),
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    size_label: Mapped[str] = mapped_column(String(20), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="sizes")
