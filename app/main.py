from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import recipes

#This declaration builds the backend (FastAPI) application
app = FastAPI(title="Recipes API")

#This block is used to allow the frontend to access the backend application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # * allows all sources to access the backend application          
    allow_credentials=False, # used to disable authorisation     
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(recipes.router)

