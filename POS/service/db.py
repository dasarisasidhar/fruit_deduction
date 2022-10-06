from pymongo import MongoClient
import datetime


client = MongoClient()
client = MongoClient('localhost', 27017) #mongo_db uses local host to store data
db = client['myapp']
products_collection = db['products']
items_collection = db['items']
tags_collection = db['tags']


class product_db:
    def add_tags_to_product(tags, product_barcode):
        # tags: list of tags
        # product_barcode: refers to which product the tag is attached
        total_items = list()
        for each_tag in tags:
            item_details = dict()
            item_details["tag"] = each_tag["epc"]
            item_details["product_barcode"] = product_barcode
            item_details["billed"] = False
            item_details["Tag_updates"] = False
            if items_collection.count_documents({'tag':  each_tag["epc"], "billed": False}, limit = 1) != 0:
                print(each_tag["epc"], "tag is already attached to product and not billed")
                items_collection.update_many({"$and": [{"billed": False}, {'tag':each_tag["epc"]} ] }, {"$set": {'Tag_updates': True}}, upsert = True)
            total_items.append(item_details)
        items_collection.insert_many(total_items) #save user to db
        return True

    def add_recent_scanned_tags(tags):
        print(tags, "are adding to db")
        tags_collection.delete_many({})
        tags_collection.insert_many(tags)
        return True

    def get_scanned_tags():
        data = list()
        for x in tags_collection.find():
            data.append(x)
        return data

    def add_tag_as_billed(tags):
        print(tags, "are billed successfully")
        if len(tags) > 0:
            for each_tag in tags:
                items_collection.update_many({"$and": [{"billed": False}, {'tag':each_tag} ] }, {"$set": {'billed': True}}, upsert = True)      
        return True

    def get_product_details(tags):
        # tags: list of tags
        # product_barcode: refers to which product the tag is attached
        products = list()
        #print(tags)
        if len(tags) == 0:
            print("0 scanned tags")
            return True
        for each_tag in tags: 
            if items_collection.find_one({"$and": [{"tag": str(each_tag["epc"])}, {"billed":False}, {"Tag_updates":False}]}):
                product_barcode = items_collection.find_one({"$and": [{"tag": str(each_tag["epc"])}, {"billed":False}, {"Tag_updates":False}]})["product_barcode"]+".00"
                print("Billed tags: ", each_tag["epc"])
            else:
                print("we can't able to find product for tag", each_tag["epc"])  
                continue      
            product = products_collection.find_one({"Barcode":str(product_barcode)})
            products.append(product)        
        return products