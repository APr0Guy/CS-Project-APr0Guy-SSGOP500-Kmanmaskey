ORBIT

PROJECT CONTENTS
----------------
Orbit/main.py              Starts the application
Orbit/pages/               Login, Dashboard, Calendar, Notes, Weather and Settings
Orbit/database/db.py       SQLite database functions
Orbit/database/orbit.db    Local database file created for this project
Orbit/assets/              Images and animated backgrounds

SETUP
-----
1. Install Python 3.10 or newer.
2. Open Command Prompt or PowerShell in the folder that contains the Orbit folder.
3. Install the required packages:

   py -m pip install -r Orbit/requirements.txt

4. Set your Meteosource API key before starting the app. (https://www.meteosource.com/)
   PowerShell:

   $env:METEOSOURCE_API_KEY="YOUR_METEOSOURCE_API_KEY"

   Command Prompt:

   set METEOSOURCE_API_KEY=YOUR_METEOSOURCE_API_KEY

5. Start Orbit:

   py Orbit/main.py

DATABASE
--------
Orbit uses SQLite. The database is stored at Orbit/database/orbit.db and is created
when the app starts if it does not already exist. No MySQL server or internet
connection is needed for accounts, tasks, calendar events, settings or notes.

Keep the Orbit folder structure together when moving the project to a pendrive.
The orbit.db file and any files attached to notes are stored inside Orbit/database.
Copy the entire Orbit folder to keep all data and attachments together.

FEATURES
--------
- Create an account and log in using a username or email address.
- Passwords are saved as salted hashes in SQLite.
- Dashboard summaries, quick task creation and task completion.
- Monthly calendar and event creation/deletion.
- Notes grouped by School, Personal and Projects.
- Attach images or import text files into notes.
- Light, Dark and System appearance settings.
- Change profile details and account password.
- Live Kathmandu weather and a five-day forecast through Meteosource.

NOTES
-----
Email verifiction is a wip 