from sqlalchemy import Column, Integer, String, Text
from backend.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)  # Limit full name length to 100
    email = Column(String(100), nullable=False)       # Limit email length to 100
    phone = Column(String(15), nullable=False)         # Limit phone length to 15 for international formats
    dob = Column(String(10), nullable=False)           # Date of birth as string (e.g., 'YYYY-MM-DD')
    gender = Column(String(10), nullable=False)        # Limit gender length to 10 (e.g., 'Male', 'Female', 'Other')
    college = Column(String(100), nullable=False)      # Limit college name length to 100
    qualification = Column(String(50), nullable=False)  # Limit qualification length to 50
    department = Column(String(50), nullable=False)     # Limit department length to 50
    year_passed_out = Column(Integer, nullable=False)    # Year as integer
    domain_of_interest = Column(String(50), nullable=False)  # Limit domain length to 50
    skills = Column(Text, nullable=False)                # Skills as Text to allow more detailed input
    experience = Column(String(100), nullable=True)      # Experience description length to 100 (nullable)
    company = Column(String(100), nullable=True)          # Company name length to 100 (nullable)
    resume_path = Column(Text, nullable=False)           # Use Text for file path to allow larger strings
