from flask import Blueprint, render_template, request
from decorators import login_required
from validators import validate_all
from models import Client, Entrance
from database import db
from datetime import datetime
from utils import BRAZIL_TZ



system = Blueprint("system", __name__)


@system.get("/system/")
@login_required
def system_get():
    """Carrega a página principal do sistema."""

    return render_template("system.html")


@system.post("/system/")
@login_required
def system_post():
    """Lida com requisições do tipo POST na página principal do sistema."""
    
    res = request.get_json()
    validation = validate_all(res)

    if any(not item["is_valid"] for item in validation):
        return validation

    cpf = res["cpf"]
    
    client = db.session.execute(
        db.select(Client).where(Client.cpf == cpf)
        ).scalar_one_or_none()

    if not client:
        client = Client(
            name=res["name"],
            rg=res["rg"],
            cpf=cpf,
            phone_number=res["phone-number"],
            birth_date=datetime.strptime(res["birth-date"], "%d/%m/%Y")
        )
        
        db.session.add(client)


    entrance = datetime.now(BRAZIL_TZ)
    new_entrance = Entrance(entrance=entrance, client=client)
    
    db.session.add(new_entrance)
    db.session.commit()
    return validation