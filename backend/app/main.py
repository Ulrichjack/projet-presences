from fastapi import FastAPI
from app.database import  engine, Base
from app.routes import etudiants, enseignants, cours, seances, presences, inscriptions, scan, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Système de Présences")

app.include_router(auth.router)
app.include_router(inscriptions.router)
app.include_router(enseignants.router)
app.include_router(etudiants.router)
app.include_router(cours.router)
app.include_router(seances.router)
app.include_router(presences.router)
app.include_router(scan.router)

@app.get("/")
def read_root():
    return {"message": "Bravo Jack ! Ton serveur FastAPI fonctionne !"}