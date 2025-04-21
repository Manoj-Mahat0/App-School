from fastapi import FastAPI
from routes import admin, auth, verify

app = FastAPI()

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(verify.router)
