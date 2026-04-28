from fastapi import FastAPI
from app.database import  engine, Base
from app.models import  etudiant
from app.routes import etudiants

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Système de Présences")


app.include_router(etudiants.router)

@app.get("/")
def read_root():
    return {"message": "Bravo Jack ! Ton serveur FastAPI fonctionne !"}