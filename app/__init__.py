from flask import Flask
from app import config
from app.main.model.database import Database
from app.main.model.embedding_service import Embeddings
from app.main.model.vector_store import VectorStore
from app.main.route.document_routes import doc_blueprint

def create_app(ENV):
    app = Flask(__name__)
    app.config.from_object(config.config_by_name[ENV])
    app.db = Database(app)
    app.vectorstore = VectorStore(app)
    app.embedding_service = Embeddings(app)
    app.register_blueprint(doc_blueprint)
    
    return app