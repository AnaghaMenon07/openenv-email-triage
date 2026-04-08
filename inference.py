import requests
import os
import json

API_URL = "http://127.0.0.1:7860"



LLM_URL = os.getenv("API_BASE_URL")
LLM_KEY = os.getenv("API_KEY")


def simple_agent(obs):
    prompt = f"""
You are an email triage assistant.

Return ONLY JSON:
{{
  "category": "spam/support/internal",
  "priority": "low/medium/high",
  "response": "your reply"
}}

Email:
Subject: {obs.get("subject", "")}
Body: {obs.get("body", "")}
"""

    try:
        response = requests.post(
            f"{LLM_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {LLM_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=10
        )

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        return json.loads(content)

    except Exception as e:
        return {
            "category": "internal",
            "priority": "low",
            "response": "fallback response"
        }


def safe_post(url, payload=None):
    try:
        if payload:
            res = requests.post(url, json=payload, timeout=5)
        else:
            res = requests.post(url, timeout=5)

        res.raise_for_status()
        return res.json()

    except Exception as e:
        print(f"Request failed at {url}: {e}")
        return None


def run():
    total_score = 0
    step_count = 0

    print("[START] task=email_triage", flush=True)

    obs = safe_post(f"{API_URL}/reset")
    if obs is None:
        return

    done = False

    while not done:
        action = simple_agent(obs)
        res = safe_post(f"{API_URL}/step", action)

        if res is None:
            return

        reward = round(res.get("reward", 0), 2)
        total_score += reward
        step_count += 1

        print(f"[STEP] step={step_count} reward={reward}", flush=True)

        obs = res.get("observation")
        done = res.get("done", True)

        if obs is None:
            break

    print(f"[END] task=email_triage score={round(total_score,2)} steps={step_count}", flush=True)


if __name__ == "__main__":
    run()