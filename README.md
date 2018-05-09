# Internet Speed Tracker
Logs your connection speed to a Google sheet. 
Tested and works with Raspberry Pi 3B, given relevant modules are installed (see below).

### Preparing Your Google Account
The following is based on [this video](https://www.youtube.com/watch?v=7I2s81TsCnc):

1. Go to [Google Developers Console](https://console.developers.google.com/cloud-resource-manager) and create a new project.
2. Go to **APIs & Services** > **Dashboard** (left sidebar). Click 'Enable APIs and Services' and enable the Google Sheets and Google Drive APIs.
3. Go to **Credentials** (left sidebar):
   + Create credentials > Service account key
   + Select _New service account_, give a service account name, and set the Role to Owner (steps will vary a little if the service account already exists and you're just adding a user)
   + Click `Create` (_Key type_ should be set to JSON by default)
4. Open the json and copy the 'client_email'.
5. Create a Google Sheet (or go to an existing one) and share that sheet with the client_email.


### Requirements
