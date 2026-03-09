from fastapi import Body
from ai_navigation import find_best_match
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Home Page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Services Page
@app.get("/services")
def services(request: Request):
    db: Session = SessionLocal()
    services = db.query(models.Service).all()
    return templates.TemplateResponse("services.html", {"request": request, "services": services})

# Jobs Page
@app.get("/jobs")
def jobs(request: Request):
    db: Session = SessionLocal()
    jobs = db.query(models.Job).all()
    return templates.TemplateResponse("jobs.html", {"request": request, "jobs": jobs})

# About Page
@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# Contact Page
@app.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.post("/contact")
def submit_contact(request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    db: Session = SessionLocal()
    new_contact = models.Contact(name=name, email=email, message=message)
    db.add(new_contact)
    db.commit()
    return templates.TemplateResponse("contact.html", {"request": request, "success": "Message Sent!"})
@app.get("/whitepapers")
def whitepapers(request: Request):
    return templates.TemplateResponse("whitepapers.html", {"request": request})

@app.post("/navigate")
async def navigate(user_input: dict = Body(...)):
    text = user_input.get("text", "")
    url = find_best_match(text)
    return {"url": url}