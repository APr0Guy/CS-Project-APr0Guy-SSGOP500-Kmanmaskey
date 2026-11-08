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
   Orbit/config.json/
   
   {
    "weather_api_key": "YOUR_API_KEY_HERE"
}

6. Start Orbit:

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
- Email verifiction is a wip 
- Currently weather is only shown for Kathmandu, if you wish to change under Orbit/pages/weather.py navigate to url and change it to your wish (P.S. it's only for direct running for exe you need to use PyInstaller to build exe again respectively but remove config.json from main file build it then inside dist/Orbit beside _initial, orbit.exe put config.json as shown under _releases_)
