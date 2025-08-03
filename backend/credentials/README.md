# Google Sheets Credentials

This directory should contain your Google Sheets service account credentials file.

## Setup Instructions:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API and Google Drive API
4. Create a Service Account:
   - Go to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Give it a name and description
   - Download the JSON key file
5. Place the JSON file as `google-sheets-service-account.json` in this directory
6. Create a Google Spreadsheet and share it with the service account email
7. Copy the spreadsheet ID from the URL and update the `.env` file

## Important:
- Never commit the actual credentials file to version control
- The credentials file should be added to `.gitignore`
