from app import app, db
from app.utils import response


@app.route('/db/api/clear/')
def clear_db():
    db.drop_all()
    db.create_all()
    return response('OK')
