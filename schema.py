import datetime
from pydantic import BaseModel


class TemplateBase(BaseModel):
    name: str

    price: str
    date: str
    content: str


class DocumentBase(BaseModel):
    name: str
    template_id: str
    date: str
    document: dict




def template_individual_serialiser(data) -> dict:
    return {
        "id": str(data["_id"]),
        "name": str(data["name"]),
        "price": data["price"],
        "content": data["content"],
    }


def document_individual_serialiser(data) -> dict:
    return {
        "id": str(data["_id"]),
        "name": str(data["name"]),
        "date": data["date"],
        "document": data["document"],
        "template_id": data["document"],
    }


def template_list_serialiser(data) -> list:
    return [template_individual_serialiser(data_item) for data_item in data]


def document_list_serialiser(data) -> list:
    return [document_individual_serialiser(data_item) for data_item in data]
