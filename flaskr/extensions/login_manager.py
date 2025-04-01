from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "auth.signin_get"
login_manager.login_message = "É necessário realizar o login para acessar a página."