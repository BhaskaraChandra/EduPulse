from pymongo import MongoClient

class TenantsAdapter:
    def __init__(self):
        self.connection_string = 'mongodb+srv://sai444134:1234567899@cluster0.6nyzm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
        self.database_name = "test"
        self.collection_name = "tenants"
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.database_name]
        self.tenants_collection = self.db[self.collection_name]

    def add_tenant(self, user_id, tenant_name):
        self.tenants_collection.insert_one({
            "user_id": user_id,
            "tenantName": tenant_name,
            "adminCount": 0,
            "userCount": 0
        })

    def add_tenant_admin(self, tenant_name):
        self.tenants_collection.update_one(
            {"tenantName": tenant_name},
            {"$inc": {"adminCount": 1}}
        )

    def get_all_tenants(self, user_id):
        tenants_data = list(self.tenants_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        ))
        return tenants_data

    def close_connection(self):
        self.client.close()
