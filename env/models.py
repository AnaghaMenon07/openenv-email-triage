from pydantic import BaseModel
from typing import Optional


# 🧠 What the agent sees
class Observation(BaseModel):
    email_id: str
    subject: str
    body: str
    history: Optional[str] = None


# 🎯 What the agent outputs
class Action(BaseModel):
    category: str          # spam / support / internal
    priority: str          # low / medium / high
    response: Optional[str] = None


# 🧮 Reward structure
class Reward(BaseModel):
    score: float