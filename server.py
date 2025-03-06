from sqlalchemy import create_engine, Column, Integer, String
from fastapi import FastAPI, Depends, HTTPException
from fastapi import FastAPI, Depends
import pathlib
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean
import datetime
import random


class requestModel(BaseModel):
    id: str
    client_name: str


class responseModel(BaseModel):
    id: str
    client_name: str
    timestamp: str


app = FastAPI()


@app.post('/', response_model=responseModel)
def get(request: requestModel):

    return responseModel(id=request.id, client_name=request.client_name, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@app.get('/{client_name}')
def get(client_name: str):

    return responseModel(id=str(random.randint(1, 1000)), client_name=client_name, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@app.get('/query/{client_name}')
def get_client(client_name: str, id: str):

    return responseModel(id=id, client_name=client_name, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
