from os import environ
from functools import lru_cache

class Settings():
    complete_genome_model_path: str = environ['COMPLETE_GENOME_MODEL_PATH']
    origin: str = environ['ORIGIN']

@lru_cache()
def get_settings() -> Settings:
    # log.info("Loading config settings from the environment...")
    return Settings()