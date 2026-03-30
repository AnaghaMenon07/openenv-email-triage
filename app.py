from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "App is running"}

from fastapi import FastAPI
from env.environment import EmailTriageEnv
from env.models import Action

app = FastAPI()

env = EmailTriageEnv()


@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()


@app.get("/state")
def state():
    obs = env.state()
    return obs.dict()


@app.post("/step")
def step(action: Action):
    next_obs, reward, done, info = env.step(action)
    
    return {
        "observation": next_obs.dict() if next_obs else None,
        "reward": reward,
        "done": done,
        "info": info
    }