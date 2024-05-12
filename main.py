from fastapi import FastAPI
from ollama import Client
import json

app = FastAPI()



# uvicorn main:app --host 0.0.0.0 --port 42690



# prompt = "Ceci est une message d'un utilisateur, répond y comme si tu étais un humain lui parlais: Salut, comment ça va ?"

# prompt = "This is a message from a user, respond to it as if you were a human talking to him. Act like an human. Message: Hi, how are you doing?"


client = Client(host='http://192.168.1.43:11434')
global model
model = "llama3"


@app.post("/getObjectAndSubject")
async def querry_mistral(query: str):
    global model
    print("Got a request, user said: ", query)

    splited = query.split()
    for i in range(len(splited)):
        word = splited[i]
        if word.lower() == "lance":
            splited[i] = "joue"
        if word.lower() == "launch":
            splited[i] = "play"
        if word.lower() == "lancer":
            splited[i] = "jouer"
    query = " ".join(splited)

    print("Query after processing: ", query)

    prompt = """Ton but est d'analiser une requète qu'un utilisateur a fait à un lecteur de musique. Tu dois trouver une action et un sujet. 
    L'action ne peut être que "jouer", "pause", "ajouter" ou "passer", mais fait attention, l'utilisateur peut ne pas utiliser cette forme. 
    Le sujet peut être de n'importe quelle forme.
    Répond ce que tu as trouvé sous la forme d'un format JSON comme celui ci: {"action":"action", "sujet":"sujet"}. 
    Ne répond que le JSON. Voici la requète de l'utilisateur: """ + query


    messages = []
    messages.append({"role": "user", "content": prompt})
    response = client.chat(model, messages=messages)
    response = response['message']['content']
    print("Response: ", response)

    parsedJson = ""
    start = False
    for char in response:
        if char == "{":
            start = True
        if start:
            parsedJson += char
        if char == "}":
            break


    print("Parsed JSON: ", parsedJson)

    jsonObject = json.loads(parsedJson)
    if jsonObject["action"] == "jouer":
        jsonObject["action"] = "play"

    return jsonObject

