import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:admin@localhost/safepick_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
