from fastapi import FastAPI
from src.api.routes import optimize, health, history, visualize, esg, whatif

app= FastAPI(title="EcoRoute Optimizer API", version="1.0")

app.include_router(optimize.router)
app.include_router(health.router)
app.include_router(history.router)
app.include_router(visualize.router)
app.include_router(esg.router)
app.include_router(whatif.router)

@app.get("/")
def root():
    return {"message": "EcoRoute Optimizer API is running"}