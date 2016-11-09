#!flask/bin/python
import os.path

from app import db


db.create_all()
