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
git clone git@github.com:GitStoph/jirasearchscripts.git
cd jirasearchscripts
python3 -m pip install -r requirements.txt --user
nano .env # And update it with your necessary credentials. SEE DISCLAIMER.
cp jirasearch.py /usr/local/bin/jirasearch
cp getjira.py /usr/local/bin/getjira
```
Make sure you got the right permissions on those two files for your user. 
If you want/need to update the python libs, you can `python3 -m pip install --upgrade -r requirements.txt`.


## getjira.py
Usage: `getjira PROJECT-3712`
Yeah. This one is pretty simple. Use the key/ticket slug pertinent for your environment.


## jirasearch.py
```
usage: jirasearch.py [-h] [-p PROJECT] -s SEARCHSTRING [-dl DESCLENG] [-sl SUMLENG]

Arguments for searching JIRA. This could be scoped to a Project with -p. It will search in the Summary, comments,
worklog comments, descriptions, deploy guides, revert plans, and/or labels.

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        Which JIRA projects should the results be scoped to? Comma separate.
  -s SEARCHSTRING, --searchstring SEARCHSTRING
                        What string are we searching for?
  -dl DESCLENG, --descleng DESCLENG
                        How many characters should we limit the description field to?
  -sl SUMLENG, --sumleng SUMLENG
                        How many characters should we limit the summary field to?
```
Example: `jirasearch -p SYSADMIN,NETADMIN,SECURITY -s '10.0.0.1' -dl 100 -sl 400`
- `-p` would be projects that exist in your JIRA instance.
- `-s` could be any string that'd show up in a JIRA ticket.
- `-dl` and `-sl` arent necessary. Tweak them to change how your output looks in your terminal.