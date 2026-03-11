from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles # Make sure this is at the very top of main.py
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from email_validator import validate_email, EmailNotValidError
import bcrypt
import asyncio
import re
import os

# Get the database URL from Railway's environment, 
# or use your local one if running on your PC
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("mysql://"):
    # Fix for SQLAlchemy if Railway gives a 'mysql://' prefix
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
else:
    # Your local fallback
    DATABASE_URL = "mysql+pymysql://root:Sankalp%402024@localhost/student_dashboard"

engine = create_engine(DATABASE_URL)

# --- Database Setup ---
DATABASE_URL = "mysql+pymysql://root:Sankalp%402024@localhost/student_dashboard"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- FastAPI App Initialization ---
app = FastAPI(title="AI Academic Portal")
app.add_middleware(SessionMiddleware, secret_key="supersecret_fastapi_key")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Models ---
class Student(Base):
    __tablename__ = 'Student'
    student_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    department = Column(String(50))
    enrollment_year = Column(Integer)

class Project(Base):
    __tablename__ = 'Project'
    project_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('Student.student_id'))
    project_title = Column(String(100))
    description = Column(Text)
    grade = Column(String(20), default="Pending")
    # AI/ML Features:
    extracted_skills = Column(String(255), default="")
    complexity_score = Column(Integer, default=0)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# --- Database Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ML Mock Function ---
async def analyze_project_text(description: str):
    """Simulates NLP extraction for project skills."""
    await asyncio.sleep(1) # Simulate processing time
    skills = []
    desc_lower = description.lower()
    
    if "python" in desc_lower: skills.append("Python")
    if "api" in desc_lower or "fastapi" in desc_lower: skills.append("API Architecture")
    if "ml" in desc_lower or "machine learning" in desc_lower: skills.append("Machine Learning")
    if "database" in desc_lower or "sql" in desc_lower: skills.append("Database Management")
    
    complexity = min(10, max(1, len(description.split()) // 8)) 
    return ", ".join(skills) if skills else "General CS", complexity

# ==========================================
#                  ROUTES
# ==========================================

@app.get("/")
async def root():
    return RedirectResponse(url="/student_auth")

# --- 1. SIGNUP ---
@app.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def post_signup(
    request: Request, 
    first_name: str = Form(...), 
    last_name: str = Form(...), 
    department: str = Form(...), 
    enrollment_year: int = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # --- 1. REAL-WORLD EMAIL DOMAIN CHECK ---
    try:
        # Pings the DNS servers to ensure the domain actually exists and accepts mail
        valid = validate_email(email, check_deliverability=True)
        email = valid.normalized
    except EmailNotValidError as e:
        # Catches fake domains (like @123.com) and invalid formats
        return templates.TemplateResponse("signup.html", {
            "request": request, 
            "error": f"Email error: {str(e)}"
        })

    # --- 2. PASSWORD STRENGTH VALIDATION ---
    if len(password) < 8 or not any(char.isdigit() for char in password):
        return templates.TemplateResponse("signup.html", {
            "request": request, 
            "error": "Security Error: Password must be at least 8 characters and contain a number."
        })

    # --- 3. DUPLICATE EMAIL CHECK ---
    if db.query(Student).filter(Student.email == email).first():
        return templates.TemplateResponse("signup.html", {
            "request": request, 
            "error": "Account already exists with this email."
        })
    
    # --- 4. SECURE HASHING & SAVING ---
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    new_student = Student(
        first_name=first_name, 
        last_name=last_name, 
        email=email,
        department=department, 
        enrollment_year=enrollment_year, 
        password_hash=hashed_pw
    )
    db.add(new_student)
    db.commit()
    
    return RedirectResponse(url="/student_auth", status_code=303)

# --- 2. LOGIN ---
@app.get("/student_auth", response_class=HTMLResponse)
async def get_auth(request: Request):
    return templates.TemplateResponse("student_auth.html", {"request": request})

@app.post("/student_auth")
async def post_auth(
    request: Request, email: str = Form(...), password: str = Form(...), 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.email == email).first()
    
    if student:
        try:
            # Safely attempt to verify the password
            if bcrypt.checkpw(password.encode('utf-8'), student.password_hash.encode('utf-8')):
                request.session['username'] = student.email
                request.session['student_id'] = student.student_id
                return RedirectResponse(url="/dashboard", status_code=303)
        except ValueError:
            # If bcrypt crashes, it means this is an old Flask account!
            return templates.TemplateResponse("student_auth.html", {
                "request": request, 
                "error": "Old account format detected. Please click 'Create an account' below."
            })
            
    return templates.TemplateResponse("student_auth.html", {
        "request": request, 
        "error": "Invalid credentials"
    })
@app.get("/add_student", response_class=HTMLResponse)
async def get_add_student(request: Request):
    # In a real app, you'd check if the user is an admin here!
    return templates.TemplateResponse("add_student.html", {"request": request})

@app.post("/add_student")
async def post_add_student(
    request: Request, first_name: str = Form(...), last_name: str = Form(...), 
    email: str = Form(...), department: str = Form(...), 
    enrollment_year: int = Form(...), password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # Hash the default password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    new_student = Student(
        first_name=first_name, last_name=last_name, email=email,
        department=department, enrollment_year=enrollment_year, password_hash=hashed_pw
    )
    db.add(new_student)
    db.commit()
    return RedirectResponse(url="/admin_dashboard", status_code=303)
# --- 3. DASHBOARD ---
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    if 'student_id' not in request.session:
        return RedirectResponse(url="/student_auth")
    
    student = db.query(Student).filter(Student.student_id == request.session['student_id']).first()
    projects = db.query(Project).filter(Project.student_id == student.student_id).all()
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "student": student, "projects": projects})

# --- 4. ADD PROJECT (With AI) ---
@app.get("/add_project", response_class=HTMLResponse)
async def get_add_project(request: Request):
    if 'student_id' not in request.session:
        return RedirectResponse(url="/student_auth")
    return templates.TemplateResponse("add_project.html", {"request": request})

@app.post("/add_project")
async def post_add_project(
    request: Request, project_title: str = Form(...), description: str = Form(...), 
    db: Session = Depends(get_db)
):
    if 'student_id' not in request.session:
        return RedirectResponse(url="/student_auth")
    
    # Run the AI Extraction
    skills, complexity = await analyze_project_text(description)
    
    new_project = Project(
        student_id=request.session['student_id'],
        project_title=project_title,
        description=description,
        extracted_skills=skills,
        complexity_score=complexity
    )
    db.add(new_project)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

# --- 5. LOGOUT ---
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/student_auth")
# --- 6. PROFILE SETTINGS ---
@app.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request, db: Session = Depends(get_db)):
    if 'student_id' not in request.session:
        return RedirectResponse(url="/student_auth")
    
    student = db.query(Student).filter(Student.student_id == request.session['student_id']).first()
    return templates.TemplateResponse("profile.html", {"request": request, "student": student})

@app.post("/profile")
async def post_profile(
    request: Request, 
    first_name: str = Form(...), 
    last_name: str = Form(...), 
    department: str = Form(...), 
    db: Session = Depends(get_db)
):
    if 'student_id' not in request.session:
        return RedirectResponse(url="/student_auth")
    
    student = db.query(Student).filter(Student.student_id == request.session['student_id']).first()
    
    # Update the student's data in the database
    if student:
        student.first_name = first_name
        student.last_name = last_name
        student.department = department
        db.commit()
        
    # Redirect back to the dashboard to see the changes!
    return RedirectResponse(url="/dashboard", status_code=303)