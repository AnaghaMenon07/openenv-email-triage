import requests
import os

API_URL = "http://127.0.0.1:8000"

def simple_agent(obs):
    subject = obs["subject"].lower()
    body = obs["body"].lower()

    if "win" in subject or "click" in body:
        return {
            "category": "spam",
            "priority": "low",
            "response": "This looks suspicious."
        }

    elif "refund" in subject or "issue" in body:
        return {
            "category": "support",
            "priority": "high",
            "response": "Sorry for the issue. We will help resolve it."
        }

    else:
        return {
            "category": "internal",
            "priority": "medium",
            "response": "Noted. Will take action accordingly."
        }


def run():
    total_score = 0

    obs = requests.post(f"{API_URL}/reset").json()

    done = False

    while not done:
        action = simple_agent(obs)

        res = requests.post(f"{API_URL}/step", json=action).json()

        total_score += res["reward"]
        obs = res["observation"]
        done = res["done"]

    print("Total Score:", total_score)


if __name__ == "__main__":
    run()