from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import login,analyze,clothe,upload,user,match
from my_log import logger
from my_config import default_config
from db.db import AsyncDB

app = FastAPI()

app.include_router(login.router)
app.include_router(analyze.router)
app.include_router(clothe.router)
app.include_router(upload.router)
app.include_router(user.router)
app.include_router(match.router)

app.mount(path='/static',  # 网页的路径
    app=StaticFiles(directory=default_config['upload']['save_path']),  # 静态文件目录的路径
    name='static')

@app.on_event('startup')
async def create():
    await AsyncDB.init_sql()
    
@app.get("/")
async def read_root():
    return {"Hello": "World"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, host="0.0.0.0", 
        port=default_config['server']['port'],
        ssl_keyfile='8087833_yige.foolai.top.key',
        ssl_certfile='8087833_yige.foolai.top.pem'
    )