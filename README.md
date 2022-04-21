# Jira Search Scripts
Your mileage may vary depending on your organization's setup.
These scripts are designed to be installed to `/opt` but run from `bin`.
You can of course handle it differently, but this is how I'll demonstrate it.
*DISCLAIMER* - Credentials should not live in a .env file. Especially unencrypted. This repo won't be covering how to use more fitting credential management strategies.


## What are these used for?
If you're like me, you hate JIRA's query language, and prefer to live in the command line. This will help you quickly search in the Summary, comments, worklog comments, descriptions, deploy guides, revert plans, and/or labels of JIRA tickets you have access to. 

If you need a little more info and still don't want to open JIRA, try `getjira` to print out more info, including comments on the ticket.
Please update line 69 of `getjira` for your environment, or delete it altogether. I left it in as an example of what you'd do for custom fields.


## Installation:
```
cd /opt
git clone repo
cd repo
python3 -m pip install -r requirements.txt --user
nano .env # And update it with your necessary credentials. SEE DISCLAIMER.
cp jirasearch.py /usr/local/bin/jirasearch
cp getjira.py /usr/local/bin/getjira
```
Make sure you got the right permissions on those two files for your user. 
If you want/need to update the python libs, you can `python3 -m pip install --upgrade -r requirements.txt`.