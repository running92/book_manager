from app import create_app
from app.services.seed import seed_demo_data
from extensions import db


app = create_app()


with app.app_context():
    db.drop_all()
    db.create_all()
    seed_demo_data(force=True)
    print("Database initialized with demo data.")

