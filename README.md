A simple task reminder app. The schedule is built out by OpenAI's API and runs continually every minute checking what task you should be working on and reminds you accordingly whenever that changes.

Run:
pip install openai dotenv

Set-up:

- Rename the plist file to your username
- Go into reset.py and update the plist file to match the file name
- Go into the .plist file and have it point to the correct folder containing your main python file
- Add a .env file containing your OpenAI API key. Change the model to 'gpt3.5-turbo' if you don't have access to gpt-4.
- Go into setup/ and write what works for you inside of reflections, rules, and the tasklist.
- Run setup/gpt.py to create the schedule
- Run reset.py to have the reminders added to your system on boot up
