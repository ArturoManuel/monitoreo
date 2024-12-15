from fastapi import FastAPI
from app.monitoreo.route import router



app = FastAPI()

# Incluir las rutas del router
app.include_router(router)

