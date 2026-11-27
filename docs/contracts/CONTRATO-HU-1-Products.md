# Contratos Back-Front HU-1-Cheaf
 
# Contratos Back-Front HU S1-01
 
## => CRUDs product
## 1. List products
### URL:
```
/products/{from_date}/{to_date}/
```
### METHOD:
#### GET
### PARAMS:
```
?id=int
?expiry_date=str
````
### BODY:
```
null
````
 
### RESPONSE:
```
{
    "detail": ""
    "data":
        [
            {
                "id": 1,
                "product_name": string,
                "description": string,
                "stock": int,
                "expiry_date":str,
                "alarms":[
                        {"alert_type": string,
                        "alert_day": string,
                        "is_active":bool,
                        "is_expired":bool,
                        "detail": {
                                "is_active": bool,
                                "is_expired": bool,
                                "days_until_activation": int,
                                "days_expired": int
                                    }
                            },
                        {"alert_type": string,
                        "alert_day": string,
                        "is_active":bool,
                        "is_expired":bool,
                        "detail": {
                                "is_active": bool,
                                "is_expired": bool,
                                "days_until_activation": int,
                                "days_expired": int
                                    }
                        }
                ]
            },
            {
                id: 2,
                "product_name": string,
                "description": string,
                "stock": int,
                "expiry_date":str,
                "alarms":[
                        {"alert_type": string,
                        "alert_day": string,
                        "is_active":bool,
                        "is_expired":bool,
                        "detail": {
                                "is_active": bool,
                                "is_expired": bool,
                                "days_until_activation": int,
                                "days_expired": int
                                    }
                        },
                        {"alert_type": string,
                        "alert_day": string,
                        "is_active":bool,
                        "is_expired":bool,
                        "detail": {
                                "is_active": bool,
                                "is_expired": bool,
                                "days_until_activation": int,
                                "days_expired": int
                                    }
                        }
                ]
            },
            {
                id: 3,
                "product_name": string,
                "description": string,
                "stock": int,
                "expiry_date":str,
                "alarms":[
                        {"alert_type": string,
                        "alert_day": string,
                        "is_active":bool,
                        "is_expired":bool,
                        "detail": {
                                "is_active": bool,
                                "is_expired": bool,
                                "days_until_activation": int,
                                "days_expired": int
                                    }
                        },
                        {"alert_type": string,
                        "alert_day": string,
                        "is_active":bool,
                        "is_expired":bool,
                        "detail": {
                                "is_active": bool,
                                "is_expired": bool,
                                "days_until_activation": int,
                                "days_expired": int
                                    }
                        }
                ]
            },
            …
        ]
}
```
La respuesta es páginada teniendo como carga útil el array results.

## 2. Crear products
### URL:
```
/products
```
### METHOD:
#### POST
### PARAMS:
```
None
````
### BODY:
```
                {
                id: 1,
                "product_name": string,
                "description": string,
                "stock": int,
                "expiry_date":str,
                }
````
 
### RESPONSE 201:
```
{
    "detail": "Producto dado de alta exitosamente"
    "data":{
                "product_name": string,
                "description": string,
                "stock": int,
                "expiry_date":str,
                "is_active":bool,
                "created_at":str,
                "updated_at":str
                
    }
}
```

### RESPONSE 40X:
```
{
    "detail": "No se pudo dar de alta el producto"
    "data":{
                "product_name": string,
                "description": string,
                "stock": int,
                "expiry_date":str,
    }
}
```

## 3. Update products
### URL:
```
/products/{id}/
```
### METHOD:
#### PUT
### PARAMS:
```
None
````
### BODY:
```
                {
                "product_name": string,
                "description": string,
                "stock": int,
                "expiry_date":str,
                "is_active":bool,
                "created_at":str,
                "updated_at":str

                }
````
 
### RESPONSE 200:
```
{
    "detail": "Producto actualizado exitosamente"
    "data": {
                "product_name": string,
                "description": string,
                "stock": int,
                "expiry_date":str,
                "is_active":bool,
                "created_at":str,
                "updated_at":str
                }
}
```

### RESPONSE 40X:
```
{
    "detail": "No se pudo actualizar el producto"
    "data":{
                "product_name": string,
                "description": string,
                "stock": int,
                "expiry_date":str,
                "is_active":bool,
                "created_at":str,
                "updated_at":str
    }
}
```

## 4. Delete products
### URL:
```
/products/{id}/
```
### METHOD:
#### PUT
### PARAMS:
```
None
````
### BODY:
```
None
````
 
### RESPONSE 200:
```
{
    "detail": "Producto se a eliminado exitosamente"
}
```

### RESPONSE 40X:
```
{
    "detail": "No se pudo eliminar el producto"
}




