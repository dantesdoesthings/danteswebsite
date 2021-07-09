from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "page": "Home page"
    }
    return templates.TemplateResponse('dantes_site/index.html', {'request': request, 'data': data})


@app.get("/projects")
async def page(request: Request):
    data = {
        "page": "Projects"
    }
    return templates.TemplateResponse('dantes_site/projects.html', {'request': request, 'data': data})
