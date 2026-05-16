from fastapi import FastAPI
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.routes import etudiants, enseignants, cours, seances, presences, inscriptions, scan, auth, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Système de Présences")

# --- 2. CONFIGURE LE CORS ICI (TRÈS IMPORTANT !) ---
origins = [
    "http://localhost:5173", # L'adresse de ton frontend Vue
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------------------------

# Et ENSUITE, on charge les routes
app.include_router(dashboard.router)
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