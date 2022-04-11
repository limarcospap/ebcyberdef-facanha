from sanic import Sanic
from sanic.response import json
from Evaluate import RefereeFunctions
import json as js


app = Sanic("hello_example")
refereeEvaluate = RefereeFunctions()

#Quando iniciar o programa ja treina o modelo

@app.route("/")
async def test(request):
  return json({"hello": "world"})

@app.route("/json", methods=["POST",])
async def postJson(request):
  newFlow = js.loads(request.json['Flow'])
  #tratar o fluxo recebido -> tirar as colunas que não são usadas no modelo
  refereePrediction = refereeEvaluate.RefereePredict(newFlow)
  return json({ "received": True, "Flow": newFlow, "Referee Prediction": str(refereePrediction)})

@app.route("/test")
async def predictReferee(request):
  flow = [[139310, 18.1029, 0, 0, 2, 40, 75, 0, 1, 0, 1]]
  return json({"Flow": str(flow[0]), "Referee Predictions": str(refereeEvaluate.RefereePredict(flow))})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)