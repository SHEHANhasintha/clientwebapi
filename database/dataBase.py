import pymongo
import io

class Database:
    "this is a database class"

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://logoimage:2XokFEGevhchsP4S@cluster0.hhg7q.mongodb.net/spamdetector?retryWrites=true&w=majority");
        self.db = self.client["logonames"]
        self.db = self.db["spamdetector"]

    def getDatabase(self):
        return self.db

    def sendImage(self,img_name,image):
        try:
            imgInBytes = io.BytesIO()
            image.save(imgInBytes, format='JPEG')
            imageinfo = {"name": img_name, "image": imgInBytes.getvalue()}
            self.db.insert_one(imageinfo)
            return('image was saved to the database')
        except:
            return('image could not save to the database')

    def deleteImage(self,img_name):
        try:
            deleteQuery = {"name": img_name}
            self.db.delete_one(deleteQuery)
            return('image was deleted ', img_name)
        except:
            return('image could not delete from the database ', img_name)

    def getEveryDisp(self):
        images = list(self.db.find({},{  "image": 0 }))
        return images

    def getImage(self,img_name):
        img = self.db.find_one({ "name":img_name },{ "_id": 0, "name": 0 })
        return img['image']

