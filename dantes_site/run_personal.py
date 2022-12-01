import os

import uvicorn

if __name__ == '__main__':
    os.environ["DANTES_ENV"] = 'personal'
    uvicorn.run('dantes_site.asgi:application', host='0.0.0.0', port=8001, log_level='info')
