import firebase_admin
from firebase_admin import firestore, credentials

from enum import Enum
from typing import TypedDict

doc_snapshot = firestore.firestore.DocumentSnapshot

class FirestoreDocument(TypedDict):
    id: firestore.firestore.DocumentSnapshot


class OPERATION(Enum):
    EQUAL = "=="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    ARRAY_CONTAINS = "array-contains"
    ARRAY_CONTAINS_ANY = "array-contains-any"
    IN = "in"
    NOT_EQUAL = "!="
    NOT_IN = "not-in"

class ORDER_BY_DIRECTION(Enum):
    ASCENDING = firestore.firestore.Query.ASCENDING
    DESCENDING = firestore.firestore.Query.DESCENDING

class Query:
    def __init__(self, collection_ref: firestore.firestore.CollectionReference):
        self.collection_ref = collection_ref
        self.order_by_direction = ORDER_BY_DIRECTION.DESCENDING
        
    
    def filter(self, field: str, operations: OPERATION, value):
        self.field = field
        self.operations = operations
        self.value = value
        return self

    def limit(self, limit: int):
        self.limit_val = limit
        return self

    def order_by(self, field: str, direction: ORDER_BY_DIRECTION=None):
        self.order_by_field = field
        if direction:
            self.order_by_direction = direction
        return self

    def execute(self) -> FirestoreDocument:
        query = self.collection_ref._query()
        
        if hasattr(self, "field") and hasattr(self, "operations") and hasattr(self, "value"):
            query = query.where(filter=firestore.firestore.FieldFilter(field_path=self.field, op_string=self.operations.value, value=self.value))
        
        if hasattr(self, "limit_val"):
            query = query.limit(self.limit_val)
        
        if hasattr(self, "order_by_field"):
            query = query.order_by(self.order_by_field, direction=self.order_by_direction.value)
        data  =  {doc.id:doc for doc in query.stream()}
        data_list = [doc for doc in query.stream()]
        print(data_list)
        return data
    


class Collection:
    def __init__(self, db: firestore.firestore.Client, collection_name: str="", collection_ref: firestore.firestore.CollectionReference=None):
        if collection_ref:
            self.collection_ref = collection_ref
        elif collection_name:
            self.collection_ref = db.collection(collection_name)
        else:
            raise Exception("No collection name or reference given")

    def get_document_by_id(self, document_id: str) -> dict:
        try: 
            data = self.collection_ref.document(document_id).get()
        except Exception as e:
            return None
        return data.to_dict()

    def get_documents(self) -> list[dict]:
        return {doc.id:doc.to_dict() for doc in self.collection_ref.stream()}

    def get_documents_by_filter(self, field: str, operations: OPERATION, value) -> list[dict]:
        return {doc.id:doc.to_dict() for doc in self.collection_ref.where(filter=firestore.firestore.FieldFilter(field_path=field, op_string=operations.value, value=value)).stream()}

    def add_document(self, document_id: str, document: dict) -> str:
        return self.collection_ref.document(document_id).set(document)

    def delete_document(self, document_id: str) -> str:
        return self.collection_ref.document(document_id).delete()

    def query(self) -> Query:
        return Query(self.collection_ref)


class Firestore:
    def __init__(self, cred_path: str):
        cred = credentials.Certificate(cred_path)
        self.app = firebase_admin.initialize_app(cred)
        self.db: firestore.firestore.Client = firestore.client()
        self.collctions = {}
        self.get_collections()

    def get_collection_ref(self, collection_name: str) -> Collection:
        if collection_name in self.collections:
            return self.collections[collection_name]
        else:
            # self.add_collection(collection_name)
            raise Exception(f"Collection named {collection_name} not found")
    
    def add_collection(self, collection_name: str) -> Collection:
        if collection_name in self.collections:
            raise Exception(f"Collection named {collection_name} already exists")
        else:
            self.collections[collection_name] = Collection(self.db, collection_name)
            return self.collections[collection_name]

    def get_collections(self) -> list[dict[str: firestore.firestore.CollectionReference]]:
        self.collections = {}
        for collection in self.db.collections():
            collection: firestore.firestore.CollectionReference = collection
            self.collections[collection.id] = Collection(self.db, collection_ref=collection)

        return self.collections