import redis

# Conectarse al servidor Redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

# Obtener todas las configuraciones
all_configurations = r.config_get('*')
print(all_configurations)

# Obtener una configuración específica
maxmemory = r.config_get('maxmemory')
print(maxmemory)