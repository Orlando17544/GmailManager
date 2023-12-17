import os
import os.path
import time
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]

def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  page_token = None  
  senders = {}

  # Call the Gmail API
  service = build("gmail", "v1", credentials=creds)
  while True:
      try:
        if page_token == None:
            results = service.users().messages().list(userId="me").execute()
        else:
            results = service.users().messages().list(userId="me", pageToken=page_token).execute()
        messages = results["messages"]

        if "nextPageToken" not in list(results.keys()):
            print("There is no next page")
            break

        page_token = results["nextPageToken"]

        if not messages:
          print("No messages found.")
          break

        for message in messages:
          headers = service.users().messages().get(userId="me", id=message["id"]).execute()["payload"]["headers"]
          
          for header in headers:
              
              if "name" in list(header.keys()) and "value" in list(header.keys()):
                  if header["name"] == "From":
                      match = re.search('(?<=<)[^>]+', header["value"])

                      if match == None:
                          sender = header["value"]
                      else:
                          sender = match.group(0)

                      if sender in list(senders.keys()):
                        senders[sender] += 1
                      else:
                        senders[sender] = 1

        os.system("clear")
        print("Emails from each sender until now: ")
        print(senders)

      except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

  senders = sorted(senders.items(), key=lambda x:x[1], reverse=True)

  with open("emails_from_each_sender.txt", "w") as file:
      for sender, emails in senders:
          file.write(str(emails) + " emails from " + sender + "\n")

if __name__ == "__main__":
  main()
