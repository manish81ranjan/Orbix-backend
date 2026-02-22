# """
# WSGI entry point for Orbix backend
# Used by Gunicorn / Render
# """
# import os
# from dotenv import load_dotenv

# load_dotenv()  # ensures .env is loaded before anything imports Config/services

# # fallback to prevent KeyError in legacy code
# if "JWT_SECRET" not in os.environ:
#     os.environ["JWT_SECRET"] = os.getenv("JWT_SECRET", "orbix-jwt-fallback")

# from app.main import create_app

# app = create_app()

# if __name__ == "__main__":
#     # For local debugging only (Render uses gunicorn)
#     app.run(host="0.0.0.0", port=5000)
# import os
# from dotenv import load_dotenv

# load_dotenv()

# os.environ.setdefault("JWT_SECRET", os.getenv("JWT_SECRET", "orbix-jwt"))

# from app.main import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
# """
# WSGI entry point for Orbix backend
# """

# from app.main import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
# import os
# from dotenv import load_dotenv

# load_dotenv()  # loads backend/.env

# from app.main import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
import os
from dotenv import load_dotenv

load_dotenv()

from app.main import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))