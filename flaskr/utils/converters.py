from typing import Any, Dict
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import NoInspectionAvailable


SENSITIVE_KEYS = ["password_hash"]


def model_to_dict(obj: Any) -> Dict[str, Any]:
    """
    Converts a SQLAlchemy model instance into a dictionary,
    filtering out internal and sensitive keys.

    Removes:
    - password_hash (Sensitive data)
    """

    try:

        mapper = inspect(obj).mapper

        data = {
            attr.key: getattr(obj, attr.key)
            for attr in mapper.column_attrs
            if attr.key not in SENSITIVE_KEYS
        }

        return data

    except (AttributeError, NoInspectionAvailable):
        return {}