from fastapi import FastAPI 
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from compile_code import initiate_compile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (set specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# "mongodb+srv://salmankhh8:bVWztvu2&$;L+S4@cluster0.4pl6u.mongodb.net/"

MONGO_URI = "mongodb+srv://salmankhh8:xPo0ZHB162JQs3Ct@cluster0.4pl6u.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["compile_craf_v2"]

class CompileRequest(BaseModel):
    code: str
    language: str

class SignInUser(BaseModel):
    userName:str
    password:str
    
class SingupUser(BaseModel):
    userName:str
    email:str
    password:str
    method:str
    joining_date:str

@app.get("/login_users")
def get_users():
    db.create_collection("sign_up")
    
    # db["sign_"]
    
    users = list(db["auth_user"].find({}, {"_id": 0}))
    return {"users": users}

@app.post("/signup_users")
def get_users():
    # db.create_collection("sign_up")
    users = list(db["auth_user"].find({}, {"_id": 0}))
    return {"users": users}

@app.post("/sing_in")
def sign_in_user():
    return {"success":True}

@app.post("/compileCode")
def compile_code(request:CompileRequest):
    # print(request.code, request.language)
    compiled_res = initiate_compile(request.code, request.language)
    
    print("START\n",compiled_res,"compiled ersul")
    
    # print(compiled_res)
    return { "success": True, "result": compiled_res }

@app.post("savedCode")
def save_code():
    return {"success":True}

    

