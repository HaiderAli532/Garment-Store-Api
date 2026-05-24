import enum
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, TimestampedMixin

if TYPE_CHECKING:
    from app.infrastructure.models.order_item import OrderItem


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    FULFILLED = "fulfilled"


class Order(TimestampedMixin, Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="subtotal_non_negative"),
        CheckConstraint("shipping_amount >= 0", name="shipping_amount_non_negative"),
        CheckConstraint("total >= 0", name="total_non_negative"),
        Index("ix_orders_status_created_at", "status", "created_at"),
    )

    order_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status", native_enum=False, length=20),
        nullable=False,
        default=OrderStatus.PENDING,
        server_default=OrderStatus.PENDING.value,
    )

    customer_name: Mapped[str] = mapped_column(String(120), nullable=False)
    customer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)

    shipping_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    shipping_line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    shipping_city: Mapped[str] = mapped_column(String(100), nullable=False)
    shipping_state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    shipping_postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    shipping_country: Mapped[str] = mapped_column(String(2), nullable=False, server_default="US")

    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    shipping_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        server_default="0",
    )
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, server_default="USD")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )
