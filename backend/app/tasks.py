import time

def process_prompt(prompt: str) -> str:
    """Simulate a long-running task by sleeping and returning a result."""
    time.sleep(5)
    return prompt.upper()
