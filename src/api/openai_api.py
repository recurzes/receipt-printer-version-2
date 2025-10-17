import re
from ctypes.wintypes import tagPOINT

from util.config import OPENAI_API_KEY
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_tasks(topic: str):
    TASK_GENERATOR_PROMPT = prompt = f"""Create 5-8 specific, actionable tasks for: {topic}

Requirements:
- Each task should be a single action item
- Start with action verbs (Create, Research, Review, etc.)
- Keep tasks concise (under 80 characters)
- Order tasks logically

Format: Just number each task on a new line
Example:
1. Research best practices for FastAPI
2. Set up project structure
3. Create database models

Tasks:"""

    messages: list[ChatCompletionMessageParam] = [  # type: ignore
        {"role": "system", "content": "You are a productivity expert who creates clear, actionable task lists."},
        {"role": "user", "content": TASK_GENERATOR_PROMPT}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )

    task_text = response.choices[0].message.content or ""

    tasks = []
    lines = task_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r'^\d+[.)\-:]\s*(.+)$', line)
        if match:
            task_content = match.group(1).strip()

            priority = 1
            if any(word in task_content.lower() for word in ['urgent', 'critical', 'asap', "!!!"]):
                priority = 4
            elif any(word in task_content.lower() for word in ['important', 'high priority', '!!']):
                priority = 3
            elif any(word in task_content.lower() for word in ['medium priority', "!"]):
                priority = 2

            labels = []
            if 'research' in task_content.lower():
                labels.append('research')
            if 'review' in task_content.lower():
                labels.append('review')
            if 'code' in task_content.lower() or 'develop' in task_content.lower():
                labels.append('coding')

            tasks.append({
                "content": task_content,
                "priority": priority,
                "labels": labels
            })

    return tasks



if __name__ == '__main__':
    topic = input("What do you want to make a list of: ")
    tasks = generate_tasks(topic)
    print(f"Tasks for '{topic}':")
    print(tasks)
    print("\n", "=" * 60 + "\n")
