from motor.motor_asyncio import AsyncIOMotorClient




url = "mongodb+srv://alexadedeji15:YvwZ9RmXcUsDblDd@e-affidavittest.lagiwwp.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(url)
db = client.get_default_database("E-affidavit-slate")


# You can also access a specific collection like this:
template_collection = db["templates"]
document_collection = db["documents"]


