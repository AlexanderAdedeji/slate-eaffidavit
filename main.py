import logging
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from database import template_collection, document_collection
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
import namegenerator
from schema import (
    DocumentBase,
    TemplateBase,
    document_individual_serialiser,
    document_list_serialiser,
    template_individual_serialiser,
    template_list_serialiser,
)


url = "mongodb://localhost:27017/E-Affidavit"


def create_app() -> FastAPI:
    app = FastAPI(
        title="E-Affidavit",
        openapi_url=f"/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()


# @app.on_event("startup")
# async def startup_db_client():
#     app.mongodb_client = AsyncIOMotorClient(url)
#     app.mongodb = app.mongodb_client.get_database()


# @app.on_event("shutdown")
# async def shutdown_db_client():
#     print("bye world")
#     app.mongodb_client.close()


@app.get("/")
def root():
    return {"msg": "Hello World"}


@app.get("/get_templates")
async def get_templates():
    # templates = []
    templates = await template_collection.find().to_list(None)
    templates = template_list_serialiser(templates)
    return templates


@app.get("/get_single_template/{template_id}")
async def get_single_template(template_id: str):
    try:
        # Convert the string ID to ObjectId
        object_id = ObjectId(template_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ID format: {template_id}")

    # Log the ObjectId
    logging.info(f"Fetching template with ID: {object_id}")

    template_obj = await template_collection.find_one({"_id": object_id})

    # Log the result of the query
    if template_obj:
        logging.info(f"Found template: {template_obj}")
    else:
        logging.info("No template found")

    if not template_obj:
        raise HTTPException(
            status_code=404,
            detail=f"Template with ID {template_id} does not exist",
        )

    # Assuming individual_serialiser is a valid function
    template_obj = template_individual_serialiser(template_obj)
    return template_obj


@app.get("/get_documents")
async def get_documents():
    # documents = []
    documents = await document_collection.find().to_list(None)
    documents = document_list_serialiser(documents)
    return documents


@app.get("/get_single_document/{document_id}")
async def get_single_documents(document_id):
    try:
        # Convert the string ID to ObjectId
        object_id = ObjectId(document_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ID format: {document_id}")

    # Log the ObjectId
    logging.info(f"Fetching document with ID: {object_id}")

    document_obj = await document_collection.find_one({"_id": object_id})

    # Log the result of the query
    if document_obj:
        logging.info(f"Found document: {document_obj}")
    else:
        logging.info("No document found")

    if not document_obj:
        raise HTTPException(
            status_code=404,
            detail=f"Document with ID {document_id} does not exist",
        )

    # Assuming individual_serialiser is a valid function
    document_obj = document_individual_serialiser(document_obj)
    templateId = document_obj['document']['templateId']
    template = await get_single_template(templateId)
    
    # return template
    return {
        "name":document_obj['name'],
        "template":{"content": template['content'], "id":templateId },
        "documentFields":document_obj['document']['documentFields']
    }


@app.post("/create_template")
async def create_template(
    template_in: TemplateBase,
):
    # Generate the template from the input
    template = template_in.model_dump()

    # Add additional properties to the template
    template["name"] = namegenerator.gen()

    # Insert the template into the collection
    result = await template_collection.insert_one(template)

    # Retrieve the newly inserted template
    template = await template_collection.find_one({"_id": result.inserted_id})
    template = template_individual_serialiser(template)
    return template


@app.post("/create_document")
async def create_document(
    document_in: DocumentBase,
):
    # Generate the template from the input
    document = document_in.model_dump()

    # Add additional properties to the template
    document["name"] = namegenerator.gen()

    # Insert the template into the collection
    result = await document_collection.insert_one(document)

    # Retrieve the newly inserted template
    document = await document_collection.find_one({"_id": result.inserted_id})

    document = document_individual_serialiser(document)
    return document
