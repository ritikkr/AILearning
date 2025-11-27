from fastapi import FastAPI

app = FastAPI()

"""
Upgrade pip and install FastAPI plus a server (uvicorn):
python3 -m pip install --upgrade pip
pip install fastapi uvicorn[standard]
Run your app with uvicorn (replace demo:app with your module:app if different):
python3 -m uvicorn demo:app --reload

https://fastapi.tiangolo.com/tutorial/path-params/

http://127.0.0.1:8000/docs

"""
itemList = [{"id":1, "name": "Item1"}]
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def getItems(item_id):
    for item in itemList:
        if item["id"] == item_id:
            return item
    
    return {"no item found"}