from database import Base, engine

# This line will create the prompts table inside prompts.db
Base.metadata.create_all(bind=engine)

print("✅ Database table created.")
