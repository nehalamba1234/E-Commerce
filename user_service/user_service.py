from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import db

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup_user(username: str = Form(...), password: str = Form(...)):
    if db.get_user(username):
        return {"error": "User already exists"}
    db.insert_user({"username": username,"password": password})
    print(f"New user signed up: {username}, {password}")
    return RedirectResponse(url="http://localhost:8000/", status_code=303)

@app.post("/login")
async def login_user(request: Request,username: str = Form(...), password: str = Form(...)):
    if db.validate_user(username, password):
        print(f"User logged in: {username} Password: {password}")
        return RedirectResponse(url="http://localhost:8000/", status_code=302) 
    return templates.TemplateResponse("login.html", {"request": request,"message": 'Invalid Credentials'})
     # order_service URL
    
    
    