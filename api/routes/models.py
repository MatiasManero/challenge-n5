from datetime import datetime
from typing import Dict, Any

from sqlmodel import SQLModel


class InfraccionBase(SQLModel):
    placa_patente: str
    timestamp: datetime
    comentarios: str

    def serialize(self) -> Dict[str, Any]:
        # Convierte el campo 'timestamp' a formato ISO 8601
        return {
            "placa_patente": self.placa_patente,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "comentarios": self.comentarios
        }

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
