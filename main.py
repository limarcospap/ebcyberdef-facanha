from os import curdir
from sanic import Sanic
from sanic.response import json
from Evaluate import RefereeFunctions
import json as js
from pymongo import MongoClient
import pymongo

def get_database():
    # CONNECTION_STRING = "mongodb://localhost:27017/"
    # client = MongoClient(CONNECTION_STRING)
    client = pymongo.MongoClient("mongodb://ebcyberdef:ebcyberdef2022@cluster0-shard-00-00.uvqpv.mongodb.net:27017,cluster0-shard-00-01.uvqpv.mongodb.net:27017,cluster0-shard-00-02.uvqpv.mongodb.net:27017/?ssl=true&replicaSet=atlas-b7wx87-shard-0&authSource=admin&retryWrites=true&w=majority")
    return client["server_db"]
    # return client["pfc"]


app = Sanic("hello_example")
refereeEvaluate = RefereeFunctions()
db = get_database()
collection = db["logs"]

predict_translate = {0: "bot", 1: "normal", 2: "suspicious"}

@app.route("/")
async def test(request):
  return json({"hello": "world"})

@app.route("/sendFlow", methods=["POST",])
async def predictReferee(request):
  data = request.json
  flow = [[data["Dur"],data["sTos"],data["dTos"],data["TotPkts"],data["TotBytes"],data["SrcBytes"],data["Proto_tcp"],data["Proto_udp"],data["Dir_->"],data["Dir_<->"]]]
  result = refereeEvaluate.RefereePredict(flow)
  data["RefereePrediction"] = predict_translate[result[0][0]]
  data["ProbaBot"] = result[1][0][0]
  data["ProbaNormal"] = result[1][0][1]
  collection.insert_one(data)
  return json({"Flow": str(data), "Referee Predictions": str(data["RefereePrediction"]), "Proba_bot": str(data["ProbaBot"]), "Proba_normal": str(data["ProbaNormal"])})

@app.route("/GetFlow", methods=["GET",])
async def getDB(request):
  data = []
  cursor = collection.find()
  for i in cursor:
    data.append(i)
  return json({"Flows": str(data)})

if __name__ == "__main__":
  #app.run(host="0.0.0.0", port=8000)
  app.run(host="localhost", port=8000)
