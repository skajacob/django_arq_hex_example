"ORM mapper for products uses cases"
# Entity
from api.engine.domain.entities import entities_products


def constructor_products_entities(product_orm) -> entities_products.Product:
    return entities_products.Product(
        id=product_orm.id,
        product_name=product_orm.product_name,
        description=product_orm.description,
        stock=product_orm.stock,
        expiry_date=product_orm.expiry_date,
        alarms=product_orm.alarms,
    )


def constructor_alarms_entities(alarm_orm) -> entities_products.Alarm:
    return entities_products.Alarm(
        id=alarm_orm.id,
        product_name=alarm_orm.product_name,
        alert_type=alarm_orm.alert_type,
        alert_date=alarm_orm.alert_date,
        is_active=alarm_orm.is_active,
        is_expired=alarm_orm.is_expired,
    )
