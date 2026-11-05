
from fastapi import FastAPI, HTTPException, Path

from app.config import APP_NAME, APP_VERSION
from app.models import ServiceCreate
from app.routers.services import router as services_router

tags_metadata = [
    {
        "name": "Services",
        "description": (
            "Операции управления программными "
            "сервисами Cloud Application."
        )
    }
]


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "Учебное серверное приложение для изучения "
        "разработки программного обеспечения "
        "облачных систем."
    ),
    openapi_tags=tags_metadata
)


app.include_router(services_router)


# Главная страница
@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "running"
    }


# Проверка состояния
@app.get("/status")
def status():
    return {
        "status": "ok",
        "service": APP_NAME
    }


# Информация о приложении
@app.get("/about")
def about():
    return {
        "name": APP_NAME,
        "type": "server application",
        "language": "Python",
        "framework": "FastAPI"
    }


# Информация о лабораторной работе
@app.get("/course")
def course():
    return {
        "discipline": "Управление работами и разработка программного обеспечения облачных систем",
        "laboratory": 2,
        "project": "Cloud Application"
    }


# Список облачных сервисов
services = [
    {
        "id": 1,
        "name": "Web Service",
        "type": "application",
        "status": "running"
    },
    {
        "id": 2,
        "name": "Database Service",
        "type": "database",
        "status": "running"
    }
]


# Получить все сервисы
@app.get(
    "/services",
    tags=["Services"],
    summary="Получить список сервисов"
)
def get_services():
    return services


@app.get(
    "/services/{service_id}",
    tags=["Services"],
    summary="Получить сервис по идентификатору",
    description="Возвращает сервис с указанным идентификатором.",
    responses={
        404: {
            "description": "Сервис не найден"
        }
    }
)


# Создать новый сервис
@app.post(
    "/services",
    tags=["Services"],
    summary="Создать новый сервис",
    description="Создаёт новый облачный сервис на основе переданных данных.",
    status_code=201
)
def create_service(service: ServiceCreate):
    new_id = max(
        (item["id"] for item in services),
        default=0
    ) + 1

    new_service = {
        "id": new_id,
        "name": service.name,
        "type": service.type,
        "status": service.status
    }

    services.append(new_service)

    return new_service


# Обновить сервис
@app.put(
    "/services/{service_id}",
    tags=["Services"],
    summary="Обновить сервис"
)
def update_service(
    service_id: int,
    service: ServiceCreate
):
    for item in services:
        if item["id"] == service_id:
            item["name"] = service.name
            item["type"] = service.type
            item["status"] = service.status

            return item

    raise HTTPException(
        status_code=404,
        detail="Service not found"
    )


# Удалить сервис
@app.delete(
    "/services/{service_id}",
    tags=["Services"],
    summary="Удалить сервис"
)
def delete_service(service_id: int):
    for item in services:
        if item["id"] == service_id:
            services.remove(item)

            return {
                "message": "Service deleted",
                "id": service_id
            }

    raise HTTPException(
        status_code=404,
        detail="Service not found"
    )

