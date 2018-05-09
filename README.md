# Internet Speed Tracker
Logs your connection speed to a Google sheet. 
Tested and works with Raspberry Pi 3B, given relevant modules are installed (see below).

Uses the `gspread` module.


### Preparing Your Google Account
The following is based on [this video](https://www.youtube.com/watch?v=7I2s81TsCnc):

1. Go to [Google Developers Console](https://console.developers.google.com/cloud-resource-manager) and create a new project.
2. Go to **APIs & Services** > **Dashboard** (left sidebar). Click `Enable APIs and Services` and enable the Google Sheets and Google Drive APIs.
3. Go to **Credentials** (left sidebar):
   + Create credentials > Service account key
   + Select `New service account`, give a service account name, and set the Role to _Owner_ (steps will vary a little if the service account already exists and you're just adding a user)
   + Click `Create` (_Key type_ should be set to JSON by default)
4. Open the json and copy the _client_email_.
5. Create a Google Sheet (or go to an existing one) and share that sheet with the _client_email_.

Mind you, you'll need the json file, sheet name and worksheet name for later.


### Requirements

+ speedtest
(pip install speedtest-cli)
+ gspread
+ ouath2client
+ requests
+ BeautifulSoup


### Further Useful Resources

+ Gspread: [github](https://github.com/burnash/gspread), [documentation](http://gspread.readthedocs.io/en/latest/index.html)
+ [Pretty Printed - How to Use Google Sheets in Python](https://www.youtube.com/watch?v=7I2s81TsCnc)  (YouTube)
+ Twilio: Google Spreadsheets and Python: [post](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html), [video](https://www.youtube.com/watch?v=vISRn5qFrkM).
