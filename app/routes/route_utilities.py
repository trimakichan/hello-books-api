from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):

    try:
        model_id = int(model_id)
    except ValueError:
        msg = {"message": f"{cls.__name__} {model_id} invalid."}
        abort(make_response(msg, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if model is None: # or if not book:
        msg = {"message": f"{cls.__name__} {model_id} is not found."}
        abort(make_response(msg, 404))

    return model