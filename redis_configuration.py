import redis
from environs import Env

env = Env()
env.read_env()

# Conectarse al servidor Redis
r = redis.Redis(host=env.str("DB_HOST"), port=env.str("DB_HOST"), db=env.str("REDIS_DB_NAME"))

# Obtener todas las configuraciones
all_configurations = r.config_get('*')
print(all_configurations)

# Obtener una configuración específica
maxmemory = r.config_get('maxmemory')
print(maxmemory)