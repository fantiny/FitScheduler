from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "BSweetOrder Yoyaku"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "replace_this_with_secure_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "replace_with_db_username"
    DB_PASSWORD: str = "replace_with_db_password"
    DB_NAME: str = "yoyaku"

    # 日志设置
    LOG_LEVEL: str = "INFO"

    class Config:
        case_sensitive = True
        env_file = ".env"

# 这是一个示例配置文件。
# 复制此文件为 config.py 并填入真实的密钥和凭据。
# config.py 应该在 .gitignore 中，以保证敏感信息的安全性。

settings = Settings() 