import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False
    api_key = os.getenv("OPENAI_API_KEY")


class DevConfig(Config):
    DEBUG = True
    MONGO_DATABASE_HOST = os.getenv('MONGO_DATABASE_HOST')
    MONGO_DATABASE_PORT = os.getenv('MONGO_DATABASE_PORT')
    MONGO_DATABASE_NAME = os.getenv('MONGO_DATABASE_NAME')

class ProdConfig(Config):
    pass

config_by_name = dict(dev=DevConfig, prod=ProdConfig)


def get_config_by_name(config_name, default=None, env_param_name=None):
    config_env = os.getenv(env_param_name or "ENV") or "dev"
    config_value = default
    if config_env:
        config_value = getattr(config_by_name[config_env](), config_name, default)
    return config_value