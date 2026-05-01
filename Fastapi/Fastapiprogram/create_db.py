from database1 import engine, Base
import model  # IMPORTANT: this registers the models

Base.metadata.create_all(bind=engine)

print("Database tables created successfully")
