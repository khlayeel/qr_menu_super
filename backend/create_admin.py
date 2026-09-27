# ============================================
# SCRIPT - Créer le compte admin unique + son café
# À lancer une seule fois : python create_admin.py
# ============================================
from app.database import SessionLocal
from app.models.user import User
from app.models.cafe import Cafe
from app.utils.security import hash_password
from slugify import slugify

def main():
    db = SessionLocal()
    try:
        name = input("Nom du propriétaire : ").strip()
        email = input("Email de connexion : ").strip()
        password = input("Mot de passe : ").strip()
        cafe_name = input("Nom du café : ").strip()

        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print("❌ Un utilisateur avec cet email existe déjà.")
            return

        user = User(name=name, email=email, password_hash=hash_password(password))
        db.add(user)
        db.commit()
        db.refresh(user)

        cafe = Cafe(owner_id=user.id, name=cafe_name, slug=slugify(cafe_name))
        db.add(cafe)
        db.commit()

        print(f"✅ Compte admin créé : {email}")
        print(f"✅ Café créé : {cafe_name} (slug: {cafe.slug})")
    finally:
        db.close()

if __name__ == "__main__":
    main()