from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data, cache_resource

import pymongo


# REF: https://docs.streamlit.io/library/advanced-features/connecting-to-data
# REF: https://experimental-connection.streamlit.app/Build_your_own
# REF: https://docs.streamlit.io/knowledge-base/tutorials/databases/mongodb
# REF: https://github.com/streamlit/files-connection
class MongoConnect(ExperimentalBaseConnection[pymongo.MongoClient]):

    def _connect(self, **kwargs) -> pymongo.MongoClient:
        return pymongo.MongoClient(**kwargs)
    
    # Returns the database provided in the parameters
    def database(self, db:str = None, coll:str = None, ttl: int = 3600):
        @cache_resource(ttl=ttl)
        def _database(db: str = None, coll: str = None):
            return self._instance[db]
        return _database(db, coll)
        
    # Returns the collection from the parameters specified
    def collection(self, db:str = None, coll:str = None, ttl: int = 3600):
        @cache_resource(ttl=ttl)
        def _collection(db: str = None, coll: str = None):
            return self._instance[db][coll]
        return _collection(db, coll)
    
    # Returns a copy of the connection instance
    def client(self):
        return self._instance
    
    # Insert a document
    def insert_one(self, dbname: str, collname: str,*args, **kwargs):
        if 'ttl' in kwargs:
            ttl=kwargs.pop('ttl')
        else:
            ttl=3600
        @cache_data(ttl=ttl)
        def _insert_one(dbname: str, collname: str, *args, **kwargs):
            coll= self.collection(dbname,collname)
            coll.insert_one(*args, **kwargs)
        return _insert_one(dbname, collname, *args, **kwargs)
    
    def delete_one(self, dbname: str, collname: str,*args, **kwargs):
        if 'ttl' in kwargs:
            ttl=kwargs.pop('ttl')
        else:
            ttl=3600
        @cache_data(ttl=ttl)
        def _delete_one(dbname: str, collname: str, *args, **kwargs):
            coll= self.collection(dbname,collname)
            coll.delete_one(*args, **kwargs)
        return _delete_one(dbname, collname, *args, **kwargs)
    
    # Search for documents matching a particular pattern
    def find(self, dbname: str, collname: str,*args, **kwargs):
        coll= self.collection(dbname,collname)
        items = coll.find(*args, **kwargs)
        items = list(items)
        return items

    # Search for a single document
    def find_one(self, dbname: str, collname: str,*args, **kwargs):
        coll= self.collection(dbname,collname)
        document = coll.find_one(*args, **kwargs)
        return document
    
    # Update a single document
    def update_one(self, dbname: str, collname: str,*args, **kwargs):
        def _update_one(dbname: str, collname: str, *args, **kwargs):
            coll= self.collection(dbname,collname)
            coll.update_one(*args, **kwargs)
        return _update_one(dbname, collname, *args, **kwargs)
    
    def count_documents(self, dbname: str, collname: str,*args, **kwargs):
        if 'ttl' in kwargs:
            ttl=kwargs.pop('ttl')
        else:
            ttl=3600
        @cache_data(ttl=ttl)
        def _count_documents(dbname: str, collname: str, *args, **kwargs):
            coll= self.collection(dbname,collname)
            return coll.count_documents(*args, **kwargs)
        return _count_documents(dbname, collname, *args, **kwargs)