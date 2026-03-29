# env/tasks.py

tasks = [
    {
        "name": "easy",
        "description": "Classify the email into correct category (spam, support, internal)",
        "required_fields": ["category"]
    },
    {
        "name": "medium",
        "description": "Classify email and assign correct priority (low, medium, high)",
        "required_fields": ["category", "priority"]
    },
    {
        "name": "hard",
        "description": "Classify email, assign priority, and generate appropriate response",
        "required_fields": ["category", "priority", "response"]
    }
]