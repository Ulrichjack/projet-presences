import os
from deepface import DeepFace

# TON IDÉE DE GÉNIE : On s'assure que le dossier existe !
DOSSIER_PHOTOS = "photos_reference"
os.makedirs(DOSSIER_PHOTOS, exist_ok=True)


def comparer_visages(chemin_photo_reference: str, chemin_photo_capturee: str) -> bool:
    """
    Compare deux photos et dit si c'est la même personne.
    Retourne True si c'est Ulrich, False si c'est un imposteur.
    """
    try:
        # DeepFace fait tout le travail magique ici
        resultat = DeepFace.verify(
            img1_path=chemin_photo_reference,
            img2_path=chemin_photo_capturee,
            model_name="VGG-Face",  # Modèle très rapide et léger
            detector_backend="retinaface",
            enforce_detection=True  # Force l'IA à chercher un visage
        )

        # resultat["verified"] contient True ou False
        return resultat["verified"]

    except ValueError:
        # Si DeepFace ne trouve AUCUN visage sur la photo (ex: photo du plafond)
        print("❌ Aucun visage détecté sur l'une des photos.")
        return False
    except Exception as e:
        print(f"❌ Erreur de l'IA : {e}")
        return False