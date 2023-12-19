# Gmail Manager

Gmail Manager allows you to clean all the junk mail in an easy way. First it lets you to find out which senders you receive a lot of emails and then you can easily delete all of the emails from those senders.

## Install

Follow the instructions to download the file credentials.json and to install the dependencies in the following link: 

https://developers.google.com/gmail/api/quickstart/python?hl=es-419

## Get started

First download the executable called calculate_emails_from_each_sender.py and execute:

```bash
python3 calculate_emails_from_each_sender.py
```

This script will allow you to know from which senders you are receiving a lot of emails. This information is going to be saved in a file called emails_from_each_sender.txt

Then with this information you are going to write inside the script delete_emails_from_senders.py in the variable senders. Then execute to delete those emails:

```bash
python3 delete_emails_from_senders.py
```
