import shutil
from fastapi import FastAPI, File, Form, UploadFile, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, Resume
import os
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Initialize the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS settings to allow frontend communication
origins = [
    "http://localhost:3000",  # Frontend
    "http://localhost:8001",  # Backend (Updated port)
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the path to your index.html
index_path = r"D:\CubeAI\resume_submission_form\frontend\index.html"

@app.get("/")
async def read_root():
    # Serve index.html from the specified path
    return FileResponse(index_path)

@app.get("/favicon.ico", response_class=Response)
async def favicon():
    return Response(status_code=204)  # No content

@app.post("/submit")
async def submit_resume(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    college: str = Form(...),
    qualification: str = Form(...),
    department: str = Form(...),
    year_passed_out: int = Form(...),
    domain_of_interest: str = Form(...),
    skills: str = Form(...),
    experience: int = Form(default=0),
    company: str = Form(default=''),
    resume: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    try:
        # Save the uploaded resume to a local directory
        resume_dir = "uploaded_resumes"
        os.makedirs(resume_dir, exist_ok=True)
        file_location = f"{resume_dir}/{resume.filename}"

        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(resume.file, file_object)

        # Store the resume metadata in the database
        new_resume = Resume(
            full_name=full_name,
            email=email,
            phone=phone,
            dob=dob,
            gender=gender,
            college=college,
            qualification=qualification,
            department=department,
            year_passed_out=year_passed_out,
            domain_of_interest=domain_of_interest,
            skills=skills,
            experience=experience,
            company=company,
            resume_path=file_location
        )
        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)

        return {"message": "Resume uploaded successfully", "id": new_resume.id}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)  # Using port 8001
