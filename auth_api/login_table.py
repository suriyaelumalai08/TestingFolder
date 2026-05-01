from logindb import engine, Base
import model  # registers Login model

Base.metadata.create_all(bind=engine)

print("✅ Login table created successfully")
