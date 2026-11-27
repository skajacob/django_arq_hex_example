import redis
from environs import Env

env = Env()
env.read_env()

# Conectarse al servidor Redis
r = redis.Redis(host=env.str("REDIS_HOST"), port=env.int("REDIS_PORT"), db=env.int("REDIS_DB_NAME"))

# Obtener todas las configuraciones
all_configurations = r.config_get('*')
print(all_configurations)

# Obtener una configuración específica
maxmemory = r.config_get('maxmemory')
print(maxmemory)