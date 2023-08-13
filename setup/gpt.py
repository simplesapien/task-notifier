from dotenv import load_dotenv
import os
import json
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

old_schedule = json.load(open('format.json', 'r'))

# Open the file with the old notes and append them to a list. Skip the first line.
notes = []
with open('reflections.txt', 'r') as file:
    for line in file.readlines()[1:]:
        notes.append((line.replace('-', '')).strip())

tasklist = open('tasklist.txt', 'r').readlines()
rules = open('rules.txt', 'r').readlines()

def main():
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[
            {"role": "user", "content": f"""
             I will give you a JSON-styled file with my weekly schedule.
             There are weekly rules that must always be included in the schedule. 
             I would like you to review the personal notes from the previous week.
             I will also give you a task list for a project I am currently working on.
             With all this information, I would like you to create a new schedule for me.
             Answer ONLY with a JSON object. 
             The last week's notes, curent schedule, task list, and rules will be delimited by triple quotes.
             ```Last week's notes: {notes}.```
             ```Current schedule: {old_schedule}```
             ```Task list: {tasklist}```
             ```Rules: {rules}```
             """},
            ]
        )

    new_schedule = chat_completion.choices[0].message.content
    with open('../schedule.json', 'w') as file:
        json.dump(json.loads(new_schedule), file, indent=4)

if __name__ == "__main__":
    main()