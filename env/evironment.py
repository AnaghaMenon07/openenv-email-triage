from typing import Tuple, Dict, Any
from env.models import Observation, Action, Reward


class EmailTriageEnv:
    def __init__(self):
        self.data = [
            {
                "email_id": "1",
                "subject": "Refund not received",
                "body": "I ordered last week but did not get refund",
                "category": "support",
                "priority": "high"
            },
            {
                "email_id": "2",
                "subject": "Win $1000 now!!!",
                "body": "Click this link to claim prize",
                "category": "spam",
                "priority": "low"
            },
            {
                "email_id": "3",
                "subject": "Meeting tomorrow",
                "body": "Reminder for team meeting at 10 AM",
                "category": "internal",
                "priority": "medium"
            }
        ]
        self.index = 0

    # 🔁 Reset environment
    def reset(self) -> Observation:
        self.index = 0
        return self._get_observation()

    # 👀 Current state
    def state(self) -> Observation:
        return self._get_observation()

    # ⚡ Take action
    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        current = self.data[self.index]

        score = 0.0

        # 🎯 category check
        if action.category == current["category"]:
            score += 0.4

        # ⚡ priority check
        if action.priority == current["priority"]:
            score += 0.2

        # 💬 response check (basic)
        if action.response:
            if "sorry" in action.response.lower():
                score += 0.2

        # move to next email
        self.index += 1
        done = self.index >= len(self.data)

        next_obs = self._get_observation() if not done else None

        return next_obs, score, done, {}

    # 🧩 helper
    def _get_observation(self) -> Observation:
        current = self.data[self.index]
        return Observation(
            email_id=current["email_id"],
            subject=current["subject"],
            body=current["body"],
            history=None
        )