# Librerias Estandar
from datetime import datetime

# Librerías de Terceros
from django.core.mail import send_mail


def send_notification(alarm, product):
    subject = f"Notificación para la alarma {alarm.id}"
    message = (
        f"La alarma {alarm.id} para el producto {product.product_name} vence hoy.\n"
    )
    message += f"Tipo de alerta: {alarm.alert_type}\n"
    message += f"Fecha de alerta: {alarm.alert_date}\n"
    message += f"Estado: {'Activa' if alarm.is_active else 'Inactiva'}\n"
    message += f"Descripción del producto: {product.description}\n"
    message += f"Stock disponible: {product.stock}\n"
    message += f"Fecha de caducidad: {product.expiry_date}\n"
    message += "\nDetalles adicionales de la alerta:\n"
    message += (
        f"- Días hasta la alerta: {(alarm.alert_date - datetime.now().date()).days}\n"
    )
    message += f"- ¿Expirada? {'Sí' if (datetime.now().date() - alarm.alert_date).days > 0 else 'No'}\n"

    recipient_list = ["jmg_extreme@hotmail.com"]  # Lista de destinatarios

    # Enviar el correo electrónico
    send_mail(subject, message, from_email=None, recipient_list=recipient_list)


def product_generator_data(products):
    """fuction to tranform product entites to a dict"""
    product_data = []
    for product in products:
        product_dict = {
            "id": product.id,
            "product_name": product.product_name,
            "description": product.description,
            "stock": product.stock,
            "expiry_date": product.expiry_date,
            "alarms": [],
        }
        for alarm in product.alarms:
            alarm_info = {
                "id": alarm.id,
                "product_id": alarm.product_id,
                "alert_type": alarm.alert_type,
                "alert_date": alarm.alert_date,
                "is_active": alarm.is_active,
                "detail": {
                    "is_active": alarm.is_active,
                    "is_expired": (datetime.now().date() - alarm.alert_date).days > 0,
                    "days_until_activation": (
                        alarm.alert_date - datetime.now().date()
                    ).days,
                    "days_expired": (datetime.now().date() - alarm.alert_date).days,
                },
            }
            product_dict["alarms"].append(alarm_info)
        product_data.append(product_dict)
    return product_data


def filter_products_by_alert_status(product_data, is_active=None, is_expired=None):
    """keep only products with at least one alarm matching the requested status"""
    if is_active is None and is_expired is None:
        return product_data

    def matches(alarm):
        detail = alarm["detail"]
        return (is_active is None or detail["is_active"] == is_active) and (
            is_expired is None or detail["is_expired"] == is_expired
        )

    return [
        {**product, "alarms": [a for a in product["alarms"] if matches(a)]}
        for product in product_data
        if any(matches(a) for a in product["alarms"])
    ]
