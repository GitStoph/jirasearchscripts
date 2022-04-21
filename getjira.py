#!/usr/bin/env python3
# 8/30/21 - GitStoph
# JIRA Ticket Output.
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
from rich.live import Live
from rich.align import Align
import time
from contextlib import contextmanager

load_dotenv(os.path.join(current_dir, '.env'))
console = Console()
jira = JIRA(os.environ.get('JIRA_URL'), auth=(os.environ.get('JIRA_USER'), os.environ.get('JIRA_PASS')))

if len(sys.argv) == 1:
    console.print("[green]Usage: getjira PROJECT-3712")
    console.print("[green]Substitute with your ticket #.")
    exit()


try:
    issue = jira.issue(sys.argv[1].upper())
except:
    console.log("[!] Error: ", sys.exc_info(), style='bold red')
    console.print("[red]Please check your formatting. Tickets need key format. ie: PROJ-3712'")
    exit(1)


BEAT_TIME = 0.04

@contextmanager
def beat(length: int = 1) -> None:
    yield
    time.sleep(length * BEAT_TIME)


table = Table(show_footer=False)
table_centered = Align.center(table)

"""
Your company's customfields may be different. I left in line 69 to show as an example of what you may want to tweak for your environment. 
"""

with Live(table_centered, console=console, screen=False, refresh_per_second=20):
    with beat(10):
        table.title = (
            "[green]"+issue.key
        )
    with beat(10):
        table.caption = "[blue]Have a lovely [b]Your Company[/b] day!"
    with beat(10):
        table.add_column("Field:", justify='center', style='blue')
    with beat(10):
        table.add_column("Result:", justify='right', style='green')
    with beat(10):
        table.add_row('Ticket', issue.key)
    #with beat(10):
        #table.add_row('Severity:', issue.fields.customfield_69420.value)
    with beat(10):
        try:
            table.add_row('Assignee:', issue.fields.assignee.name)
        except:
            pass
    with beat(10):
        table.add_row('Reporter:', issue.fields.reporter.name)
    with beat(10):
        table.add_row('Status:', issue.fields.status.name)
    with beat(10):
        try:
            table.add_row('Resolution:', issue.fields.resolution.name)
        except:
            pass
    with beat(10):
        table.add_row('Summary:', issue.fields.summary)
    with beat(10):
        table.add_row('Description:', issue.fields.description)
    for com in issue.fields.comment.comments:
        with beat(10):
            table.add_row('Comment:', com.author.name+" - "+com.body)
    with beat(10):
        table.row_styles = ["none", "dim"]


exit()