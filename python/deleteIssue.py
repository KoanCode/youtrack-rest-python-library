
"""
http://confluence.jetbrains.com/display/YTD5/Delete+an+Issue

"""
__author__ = 'ryan KoanCode'

import sys
from youtrack import Issue
from youtrack.connection import Connection
import os


def main():
    target_url, target_login, target_password, issue_source = sys.argv[1:5]
    target = Connection(target_url, target_login, target_password)
    if os.path.exists(issue_source): #"treat as a file of issues to delete"
        issues = open(issue_source).readlines()
    else:
        issues = []
        issues.append(issue_source)
    for issue in issues:
        if str(issue).strip() == "": continue
        print "deleting %s" % (issue,)
        try:
            result = target._req("DELETE", "/issue/%s" % (str(issue).strip(),))
            print result
        except Exception  as e:
            print e



if __name__ == "__main__":
    main()


