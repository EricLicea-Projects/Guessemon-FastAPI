from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel


app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Welcome to Guessamon API'}