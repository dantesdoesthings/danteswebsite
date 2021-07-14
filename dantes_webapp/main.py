from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dantes_api.objects.data_generator_call import DataGeneratorCall, DataGeneratorResult
from dantes_webapp.dantes_data_generator.parse_call import submit_data


app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    data = {
        'page': 'Home page'
    }
    return templates.TemplateResponse('dantes_site/index.html', {'request': request, 'data': data})


@app.get('/projects')
async def page(request: Request):
    data = {
        'page': 'Projects'
    }
    return templates.TemplateResponse('dantes_site/projects.html', {'request': request, 'data': data})


@app.get('/blog')
async def page(request: Request):
    data = {
        'page': 'Blog'
    }
    return templates.TemplateResponse('dantes_blog/blog.html', {'request': request, 'data': data})


@app.get('/projects/data_generator')
async def page(request: Request):
    data = {
        'page': 'Project Data Generator'
    }
    return templates.TemplateResponse('dantes_data_generator/data_generator.html', {'request': request, 'data': data})


@app.post('/projects/data_generator', response_model=DataGeneratorResult, status_code=200)
async def page(data_gen_call: DataGeneratorCall):
    data = {
        'page': 'Project Data Generator'
    }
    result = submit_data(data_gen_call)
    print(result)
    return result
