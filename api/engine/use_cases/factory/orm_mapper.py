"ORM mapper for products uses cases"
# Entity
from api.engine.domain.entities import entities_products, entities_alarms


def constructor_alarms_entities(alarm_orm) -> list[entities_alarms.Alarm]:
    return [
        entities_alarms.Alarm(
            id=alarm.id,
            product_id=alarm.product_id,
            alert_type=alarm.alert_type,
            alert_date=alarm.alert_date,
            is_active=alarm.is_active,
        )
        for alarm in alarm_orm
    ]


def constructor_products_entities(product_orm) -> entities_products.Product:
    return entities_products.Product(
        id=product_orm.id,
        product_name=product_orm.product_name,
        description=product_orm.description,
        stock=product_orm.stock,
        expiry_date=product_orm.expiry_date,
        alarms=constructor_alarms_entities(product_orm.alarms.all()),
    )
