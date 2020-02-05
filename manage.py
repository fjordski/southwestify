from utils.get_environment import environment
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import flask_app, db

migrate = Migrate(flask_app, db)

manager = Manager(flask_app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
