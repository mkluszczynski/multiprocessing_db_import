import os
from dotenv import load_dotenv
load_dotenv()

class Config:

    def getDbHost():
        return Config.__getEnvValue("DB_HOST")

    def getDbPort():
        return Config.__getEnvValue("DB_PORT")

    def getDbUser():
        return Config.__getEnvValue("DB_USER")

    def getDbPassword():
        return Config.__getEnvValue("DB_PASSWORD")

    def getDbName():
        return Config.__getEnvValue("DB_NAME")

    def __getEnvValue(config_value: str):
        value = os.getenv(config_value)
        if value:
            return value
        else:
            raise Exception(f"Value: {config_value} is not set.")