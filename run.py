import uvicorn


if __name__ == '__main__':
    uvicorn.run('danteswebsite.dantes_webapp.main:app', host='0.0.0.0', port=8080, log_level='info')
