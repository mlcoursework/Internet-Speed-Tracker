# Internet-Speed-Tracker
Logs your connection speed to a Google sheet. 
Tested and works with Raspberry Pi 3B, given relevant modules are installed (see below).

### Preparing your google account
The following is based on [this video](https://www.youtube.com/watch?v=7I2s81TsCnc):

1. Go to [https://console.developers.google.com/cloud-resource-manager](https://console.developers.google.com/cloud-resource-manager) and create a new project.
2. Go to **APIs & Services** > **Dashboard** (left sidebar). Click 'Enable APIs and Services' and enable the Google Sheets and Google Drive APIs.
3. Go to **Credentials** (left sidebar):
  + Create credentials > Service account key
  + Select _New service account_ (or select the service account if it already exists)



### Requirements
