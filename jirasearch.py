#!/usr/bin/env python3
# 1/26/20 GitStoph
# 8/30/21 - updated to rich tables, added multi proj handling.
# JIRA Search script. 
##################################################
import sys, os
import argparse

os.chdir('/opt/jirasearch')
current_dir = os.getcwd()
sys.path.append(current_dir)

from jira import JIRA
from jira.exceptions import JIRAError
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv(os.path.join(current_dir, '.env'))
console = Console()
jira = JIRA(os.environ.get('JIRA_URL'), auth=(os.environ.get('JIRA_USER'), os.environ.get('JIRA_PASS')))

def get_args():
    parser = argparse.ArgumentParser(
        description='Arguments for searching JIRA. This could be scoped to a Project with -p. It will search in the Summary, comments, worklog comments, descriptions, deploy guides, revert plans, and/or labels.')
    parser.add_argument('-p', '--project',required=False,type=str,default='None',action='store',
        help="Which JIRA projects should the results be scoped to? Comma separate.")
    parser.add_argument('-s', '--searchstring',required=True,type=str,default='None', action='store',
        help='What string are we searching for?')
    parser.add_argument('-dl', '--descleng',required=False,type=int,default=150,action='store',
        help="How many characters should we limit the description field to?")
    parser.add_argument('-sl', '--sumleng',required=False,type=int,default=500,action='store',
        help="How many characters should we limit the summary field to?")
    args = parser.parse_args()
    return args


def search_jira(project, searchstring):
    """Does the search action. Sometimes Labels can cause errors, so there's a try/except to catch and move on."""
    try:
        results = jira.search_issues('project = {1} AND (summary ~ {0} OR comment ~ {0} OR worklogComment ~ {0} OR description ~ {0} OR "Deploy Guide" ~ {0} OR "Revert Plan" ~ {0} OR labels in {0})  order by updated DESC'.format(searchstring, project), maxResults=100)
        return results
    except JIRAError:
        console.print("[yellow]Label field excluded from [red]{0}[yellow] search, the search string was not in the list of available labels.".format(project))
        results = jira.search_issues('project = {1} AND (summary ~ {0} OR comment ~ {0} OR worklogComment ~ {0} OR description ~ {0} OR "Deploy Guide" ~ {0} OR "Revert Plan" ~ {0})  order by updated DESC'.format(searchstring, project), maxResults=100)
        return results


def print_simple_results(resultlist, descleng, sumleng):
    """Creates the rich table and prints it out. Descleng and sumleng
    exist purely to try to keep the table to realistic sizes."""
    try:
        table = Table(show_header=True, header_style="cyan", show_lines=True)
        table.add_column("Ticket", justify="center")
        table.add_column("Summary", justify="center")
        table.add_column("Description", justify="center")
        table.add_column("URL", justify="center")
        for r in resultlist:
            url = '{0}/browse/'.format(os.environ.get('JIRA_URL'))+r.key
            if r.fields.summary != None:
                summary = r.fields.summary[:sumleng]+"..."
            else:
                summary = "None"
            if r.fields.description != None:
                description = r.fields.description[:descleng]+"..."
                description = description.replace('\r', ' ')
                description = description.replace('\n', ' ')
            else:
                description = "None"
            table.add_row(r.key, summary, description, url)
        console.print(table, style='green')
    except:
        console.print("[!] Error: ", sys.exc_info(), style='bold red')
        pass


def main():
    try:
        args = get_args()
        lookup = []
        for each in args.project.upper().split(','):
            result = search_jira(each, args.searchstring)
            if len(lookup) == 100:
                console.print("[yellow]Results capped at 100. Consider a different searchstring?")
            lookup += result
        if len(lookup) != 0:
            print_simple_results(lookup, args.descleng, args.sumleng)
        exit()
    except KeyboardInterrupt:
        console.print("[red][!!!] Ctrl + C Detected!")
        console.print("[red][XXX] Exiting script now..")
        exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("[red][!!!] Ctrl + C Detected!")
        console.print("[red][XXX] Exiting script now..")
        exit()