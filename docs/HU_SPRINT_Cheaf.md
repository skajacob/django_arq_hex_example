# Django Assessment

## Intro

Esta aplicación usa python 3.8.13 y Django 3.1.3

## Listado de tareas 

### Tareas

#### CRUD de Productos

Crear 2 tablas, products, alarms

1. Estructura de la tabla products

   - id
   - Nombre_del_producto
   - descripcion
   - fecha_caducidad

2. Estructura de la tabla alarms

   - id
   - Nombre_del_producto
   - fecha_alarma
   - is_active
   - is_expired


Crear CRUD para la tabla products.

   - Cada ves que se inserte un registro en la tabla products se debe crear dos alarmas en la tabla alarms una con fecha  10 días antes de su fecha de caducidad y otra con 5 días antes de su fecha de caducidad

Crear vistas de listado
   - se deben filtrar por fecha especificada por el usuario
   - filtrar productos pos estado de alerta
   - listado de products proporcionando detalle del estado de la alerta,incluyendo:
      ○ Si la alerta está activa.
      ○ Si la alerta está expirada.
      ○ La cantidad de días restantes antes de que la alerta se active.
      ○ La cantidad de días que han pasado desde que se activó la alerta.

Crear un API REST

   - Implementar modulo de autenticacion(los enpoints deben estar protegidos) 
   - Solo los usuarios autenticados pueden hacer uso del servicio
   - Endpoint que listara products
   - Endpoint para insertar products
   - Endpoint para editar products
   - Endpoint para eliminar products
   - Implementar un cronjob para calcular automáticamente si una alerta se ha activado o no, y realizar el cálculo de los días restantes hasta la activación o si la alerta ya ha pasado. Este cron debería correr cada 24 horas.

