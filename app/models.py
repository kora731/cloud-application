
from pydantic import BaseModel, Field



class ServiceCreate(BaseModel):
    name: str = Field(
        ...,
        description="Название облачного сервиса"
    )

    type: str = Field(
        ...,
        description="Тип облачного сервиса"
    )

    status: str = Field(
        ...,
        description="Текущее состояние сервиса"
    )
