from flask import abort
from flask_login import current_user


def check_owner(obj, owner_field='seller_id'):
    """Abort 403 if current user does not own the object."""
    owner_id = getattr(obj, owner_field, None)
    if owner_id != current_user.id and not current_user.is_admin:
        abort(403)
#This just checks if the current user is the owner of the object (like a listing or review) or an admin. If not, it aborts with a 403 Forbidden error. 

def sanitize(text: str, max_length: int = 1000) -> str:
    if not text:
        return ''
    return text.strip()[:max_length]
#This will just clean the users input by removing any extra spaces and limiting the the text length
