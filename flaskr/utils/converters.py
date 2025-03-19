def model_to_dict(obj: object) -> dict:
    """Returns the SQLAlchemy model as a dict, removing the keys 'id' and
    'sa_instance_state'.
    """

    obj = obj.__dict__
    obj.pop("_sa_instance_state", None)
    obj.pop("id", None)
    return obj