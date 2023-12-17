import os.path
import time

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

  # Add senders from whom you want to delete emails, e.g. example@gmail.com
  senders = []

  query = ""
  for sender in senders:
      if query == "":
          query += "from:" + sender
      else:
          query += " OR from:" + sender

  # Call the Gmail API
  service = build("gmail", "v1", credentials=creds)
  while True:
      try:
        results = service.users().messages().list(userId="me", q=query).execute()

        if "messages" not in results.keys():
          print("No messages found.")
          break

        messages = results["messages"]

        messages_to_delete = []
        for message in messages:
          messages_to_delete.append(message["id"])
        
        response = service.users().messages().batchDelete(userId="me", body={"ids": messages_to_delete}).execute()
        if response == "":
          print(f"{len(messages)} messages were deleted")
        else:
          print(response)

        time.sleep(5)

      except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
