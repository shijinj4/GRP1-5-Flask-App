from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
#from datetime import date

# Create an SQLite database connection
engine = create_engine("sqlite:///mydatabase.db")


# Define the base class
Base = declarative_base()


# Define the StudentProfile model
class StudentProfile(Base):
    __tablename__ = "Student_Profile"

    student_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)  # Changed from String to Date
    amount_due = Column(Integer)


# Create the table in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
