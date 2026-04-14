import json 


def read_json():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"appointments":[], "rewiews":[], "clients": {}}    
    
def write_json(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_appointment(service, date, time, client):
    user_data = read_json() 
    user_data["appointments"].append({"service" : service, "date" : date, "time" : time, "client" : client})
    write_json(user_data)

def add_review(client, text):
    user_data = read_json()
    user_data["reviews"].append({"client" : client, "text" : text})
    write_json(user_data)