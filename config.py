import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = b'\xbd\x83\xb2\xb1\x84\xb6\x9e&C\x01\xec\xc9\x88\xd7@\x07\xef\xc8`\x87|8\xe2\x8a'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
