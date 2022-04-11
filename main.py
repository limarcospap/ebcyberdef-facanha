from sanic import Sanic
from sanic.response import json
from Evaluate import RefereeFunctions


app = Sanic("hello_example")
refereeEvaluate = RefereeFunctions()

#Quando iniciar o programa ja treina o modelo

@app.route("/")
async def test(request):
  return json({"hello": "world"})

@app.route("/test")
async def predictReferee(request):
  flow = [[139310, 18.1029, 0, 0, 2, 40, 75, 0, 1, 0, 1]]
  return json({"Flow": str(flow[0]), "Referee Predictions": str(refereeEvaluate.RefereePredict(flow))})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)