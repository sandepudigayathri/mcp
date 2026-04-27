from fastapi import FastAPI
from pydantic import BaseModel
import requests

app =  FastAPI()

class MyMCP(BaseModel):
  tool_name : str
  arguments : dict

#tools = {"find_distance": find_distance, "get_fare":get_fare}

def find_distance(origin,destination):
  Base_Url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
  full_url = f'{Base_Url}origins={origin}&destinations={destination}&key=AIzaSyCpJwiBDbisM_YJCuPnEfBE78dMUWuqK_8'
  response = requests.get(full_url).json()
  return response['rows'][0]['elements'][0]['distance']['text']

def get_fare(num):
  if num > 0 and num <100:
    return num*10
  else:
    fare = 100*10
    num-=100
    fare+=(num*12)
    return fare
 
tools = {"find_distance": find_distance, "get_fare":get_fare} 

@app.get("/tools")
def list_tools():
  return {
    "tools": [
      {
        "name": "find_distance",
        "description": "Find distance between two cities",
        "parameters": {
          "type": "object",
          "properties": {
            "origin": {
              "type": "string",
              "description": "Starting city"
            },
            "destination": {
              "type": "string",
              "description": "Destination city"
            }
          },
          "required": ["origin", "destination"]
        }
      },
      {
        "name": "get_fare",
        "description": "find fare to travel between two places based on kms",
        "parameters": {
          "type": "object",
          "properties": {
            "num": {
              "type": "integer",
              "description": "Distance in kilometers"
            }
          },
          "required": ["num"]
        }
      }
    ]
  }

@app.post('/mcp')
def call_tool(req : MyMCP):
  if req.tool_name not in tools:
    return {'status': 'error', 'description':'tool not available'}
  else:
    try:
      result = tools[req.tool_name](**req.arguments)
      return {'status':'OK', 'description': result}
    except Exception as e:
      return {'status':'error', 'description': str(e)}

