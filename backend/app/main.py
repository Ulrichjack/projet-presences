from fastapi import FastAPI
from app.database import  engine, Base
from app.routes import etudiants, enseignants, cours, seances, presences

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Système de Présences")


app.include_router(etudiants.router)
app.include_router(enseignants.router)
app.include_router(cours.router)
app.include_router(seances.router)
app.include_router(presences.router)

@app.get("/")
def read_root():
    return {"message": "Bravo Jack ! Ton serveur FastAPI fonctionne !"}