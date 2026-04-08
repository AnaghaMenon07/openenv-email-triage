import requests

API_URL = "http://127.0.0.1:7860"


def simple_agent(obs):
    subject = obs.get("subject", "").lower()
    body = obs.get("body", "").lower()

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

    # 🔥 REQUIRED START BLOCK
    print("[START] task=email_triage", flush=True)

    obs = safe_post(f"{API_URL}/reset")

    if obs is None:
        print("[END] task=email_triage score=0 steps=0", flush=True)
        return

    done = False

    while not done:
        action = simple_agent(obs)

        res = safe_post(f"{API_URL}/step", action)

        if res is None:
            print(f"[END] task=email_triage score={total_score} steps={step_count}", flush=True)
            return

        reward = res.get("reward", 0)
        obs = res.get("observation")
        done = res.get("done", True)

        total_score += reward
        step_count += 1

        # 🔥 REQUIRED STEP BLOCK
        print(f"[STEP] step={step_count} reward={reward}", flush=True)

        if obs is None:
            break

    # 🔥 REQUIRED END BLOCK
    print(f"[END] task=email_triage score={total_score} steps={step_count}", flush=True)


if __name__ == "__main__":
    run()