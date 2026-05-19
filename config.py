"""应用配置."""

import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///rongguang.db")
API_TITLE = "绒光公社 API"
API_VERSION = "1.0.0"
