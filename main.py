from fastapi import FastAPI
from api import models
from api.models import engine
import api.routing as router

app = FastAPI(
    title='to-do backend',
    version="1.0.0"
    )

models.Base.metadata.create_all(bind=engine)

app.include_router(router.todo)
app.include_router(router.user)
app.include_router(router.auth)

app = FastAPI()

@app.get('/')
def home():
    return "Welcome to todos api"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app=app,
    )
