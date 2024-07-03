from datetime import datetime
from uuid import UUID, uuid4

from pydantic import validator, field_validator
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from api.routes.models import InfraccionBase


def create_tables(engine):
    SQLModel.metadata.create_all(engine)


class Personas(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    nombre: str
    correo_electronico: str

    vehiculos: List["Vehiculos"] = Relationship(back_populates="persona")


class Vehiculos(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    placa: str = Field(sa_column_kwargs={"unique": True})
    marca: str
    color: str
    persona_id: UUID = Field(foreign_key="personas.id")

    persona: Personas = Relationship(back_populates="vehiculos")
    infracciones: List["Infracciones"] = Relationship(back_populates="vehiculo")


class Oficiales(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    nombre: str
    numero_unico: int


class Infracciones(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    placa_patente: str = Field(foreign_key="vehiculos.placa")
    timestamp: str
    comentarios: str
    vehiculo: Vehiculos = Relationship(back_populates="infracciones")