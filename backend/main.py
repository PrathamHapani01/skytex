from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv
from database import engine, Base
from api import router as api_router
from admin import router as admin_router

# Load environment variables
load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sky Tex API",
    docs_url="/docs" if os.getenv("ENVIRONMENT", "production") != "production" else None,
    redoc_url=None,
)

# CORS middleware — Allow Vercel frontend and localhost
# Note: FastAPI CORSMiddleware does NOT support partial wildcards like "https://*.vercel.app".
# Use allow_origin_regex for pattern matching instead.
frontend_url = os.getenv("FRONTEND_URL", "")
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]
if frontend_url:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app|https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers (must be before static file mounts and catch-all)
app.include_router(api_router)
app.include_router(admin_router)

# Health check — placed before catch-all route so it's always reachable
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Serve static files from parent directory (for local dev / Docker)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.exists("/frontend"):
    if os.path.exists("/frontend/frontend"):
        frontend_dir = "/frontend/frontend"
    else:
        frontend_dir = "/frontend"
else:
    if os.path.exists(os.path.join(parent_dir, "frontend")):
        frontend_dir = os.path.join(parent_dir, "frontend")
    else:
        frontend_dir = parent_dir

# Robust Static File Mounts (handles nested frontend or root assets)
assets_path = next((p for p in [os.path.join(frontend_dir, "assets"), "/frontend/assets", os.path.join(parent_dir, "assets")] if os.path.exists(p)), None)
css_path = next((p for p in [os.path.join(frontend_dir, "css"), "/frontend/css", os.path.join(parent_dir, "css")] if os.path.exists(p)), None)
js_path = next((p for p in [os.path.join(frontend_dir, "js"), "/frontend/js", os.path.join(parent_dir, "js")] if os.path.exists(p)), None)

if assets_path:
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
if css_path:
    app.mount("/css", StaticFiles(directory=css_path), name="css")
if js_path:
    app.mount("/js", StaticFiles(directory=js_path), name="js")

# Serve uploaded images
uploads_dir = os.getenv("UPLOAD_DIR", "/app/uploads")
if os.path.exists(uploads_dir):
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
@app.get("/")
def read_root():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Sky Tex API is running"}

@app.get("/{page_name:path}")
def serve_page(page_name: str):
    # Remove .html extension if present
    if page_name.endswith(".html"):
        page_name = page_name[:-5]
    
    # Only serve if it's a known HTML page
    known_pages = ["index", "about", "shop", "product", "contact", "collections", "swatches", "admin"]
    if page_name in known_pages:
        html_path = os.path.join(frontend_dir, f"{page_name}.html")
        if os.path.exists(html_path):
            return FileResponse(html_path)
    
    # Return 404 for unknown paths
    raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
