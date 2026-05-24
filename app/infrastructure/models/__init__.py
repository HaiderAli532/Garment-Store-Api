"""Import all models so Alembic autogenerate discovers metadata."""

from app.infrastructure.models.admin_user import AdminUser
from app.infrastructure.models.category import Category
from app.infrastructure.models.order import Order
from app.infrastructure.models.order_item import OrderItem
from app.infrastructure.models.product import Product
from app.infrastructure.models.product_image import ProductImage
from app.infrastructure.models.product_size import ProductSize

__all__ = [
    "AdminUser",
    "Category",
    "Order",
    "OrderItem",
    "Product",
    "ProductImage",
    "ProductSize",
]
