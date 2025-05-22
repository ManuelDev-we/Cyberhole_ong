# src/extensions.py
from flask_wtf import CSRFProtect      # ← forma corta, 100 % válida
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = "login.login_page"

csrf = CSRFProtect()
