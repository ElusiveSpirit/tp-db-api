from app import app, db
from app.utils import response

from app.user.models import User
from app.forum.models import Forum
from app.thread.models import Thread
from app.post.models import Post


@app.route('/db/api/clear/')
def db_clear():
    db.drop_all()
    db.create_all()
    return response('OK')


@app.route('/db/api/status/')
def db_status():
    return response({
        'user': User.query.count(),
        'thread': Thread.query.count(),
        'forum': Forum.query.count(),
        'post': Post.query.count()
    })
