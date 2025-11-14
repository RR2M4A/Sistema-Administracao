from typing import Any, Dict

def model_to_dict(obj: Any) -> Dict[str, Any]:
    """
    Converts a SQLAlchemy model instance into a dictionary,
    filtering out internal and sensitive keys.

    Removes:
    - _sa_instance_state (SQLAlchemy internal)
    - password_hash (Sensitive data)
    """

    try:
        return {
            key: value
            for key, value in obj.__dict__.items()
            if key not in ("_sa_instance_state", "password_hash")}

    except AttributeError:
        return {}