
"""
Leverage csv2youtrack to import pivotal tracker

python pivotalTracker2youtrack.py source_file, target_url, target_login, target_password, project_id, start_number

Requires csv extract from PT: pre-processing is run on the standard extract, and then a standard mapping file is used

Features:
-places Task and TaskStatus in description as numbered items
-Places pivotal tracker number and URL in the description
-Labels placed in the description (until http://youtrack.jetbrains.com/issue/JT-25499 is solved)
-Creates a tag file for future tags of created items
-Supports comments
"""
__author__ = 'ryan - KoanCode'

import csv2youtrack
import sys
import os
import csv
from youtrack.connection import Connection


def main():
    source_file, target_url, target_login, target_password, project_id, start_number = sys.argv[1:7]
    importable_file, tag_file = prep_file(project_id, start_number, source_file)
    csv2youtrack.run(importable_file, target_url, target_login, target_password, "pivotalTrackerMapping")
    add_tags(tag_file, target_url, target_login, target_password)

def prep_file(project_id, start_number, file_in):

    start_number = int(start_number)

    file_in = os.path.abspath(file_in)
    r = os.path.splitext(file_in)
    file_out = r[0]  + "_youtrack_in.csv"
    tag_file_out = r[0] + "_youtrack_tag.csv"
    # now add project, project name to every line
    count = -1
    header = []
    short_header = []
    comment_indexes = []
    with open(tag_file_out, "w+") as tag_o_out:
        tag_writer = csv.writer(tag_o_out)
        with open(file_out, "w+") as file_o_out:
            writer = csv.writer(file_o_out)
            with open(file_in) as file_o_in:
                reader = csv.reader(file_o_in)
                for row in reader: # row is array
                    count += 1
                    if count == 0:
                        row.insert(0, "numberInProject") # needed to put "lower" numbers (PT numbers are too high)
                        row.insert(0, "Project")
                        c_count = -1
                        for r in row:
                            c_count += 1
                            if r == "Comment":
                                comment_indexes.append(c_count)
                            elif r not in ("Task", "Task Status"):
                                short_header.append(r)
                        header = list(row)
                        writer.writerow(short_header)
                    else:
                        row.insert(0, start_number + count-1 )
                        row.insert(0, project_id)
                        write_to_tag_file(tag_writer, header, row, project_id, start_number + count-1)
                        # convert None to single space
                        newRow = []
                        rcount = -1
                        comments = []
                        for r in row: # manipulate some row contents
                            rcount += 1
                            headerV = header[rcount]
                            if rcount in comment_indexes and r != None: # comments need to go at the end, separated by commas without a field header
                                comments.append(r)
                                continue
                            if headerV in ("Task", "Task Status"):
                                continue # will be in description
                            if headerV == "Requested By": # prevents creation of user (and map did not work)
                                newRow.append("root")
                                continue
                            elif headerV == "State" and not r: # prevents creation of _ state
                                newRow.append("unstarted")
                            elif headerV == "Description":
                                newRow.append(enrich_description(header, row))
                            elif r:
                                newRow.append(r)
                            elif not r:
                                newRow.append(None)
                        newRow.extend(comments) # place comments on end


                        writer.writerow(newRow)
    return file_out, tag_file_out

def enrich_description(header, row):
    """
    Place additional information in the description

    Tasks would be mark up, labels eventually real label, and the URL of the original story
    :param header:
    :param row:
    :return:
    """
    description = row[header.index("Description")]
    # all of the tasks
    taskIndexes = []
    for i in range(0, len(header)):
        if header[i] == "Task":
            taskIndexes.append(i)
    for v in taskIndexes:
        try:
            if row[v + 1] == "completed" and row[v]: #task done
                description += "\n# --%s--" % (row[v])
            elif row[v]:
                description += "\n# %s" % (row[v])
        except:
            pass
    description += "\n\nPT#%s" % (row[header.index("Id")])
    description += "\nURL:%s" % (row[header.index("URL")])
    labels = row[header.index("Labels")]
    if labels:
        description += "\nLabels:%s" % (row[header.index("Labels")])
    return description

def write_to_tag_file(tag_file, header, row, project_id, number):
    """
    Create file to later run the tags on the issue

    Has to be run after
    http://confluence.jetbrains.com/display/YTD5/Apply+Command+to+an+Issue
    :return:
    """
    add_row = []
    add_row.append(project_id + "-" + str(number))
    labels = row[header.index("Labels")]
    if labels:
        add_row.extend(labels.split(","))
        tag_file.writerow(add_row)

def add_tags(tag_file,target_url, target_login, target_password):
    """
    Add tags from the tag file (run after known creation)
    :param tag_file:
    :return:
    """
    target = Connection(target_url, target_login, target_password)
    with open(tag_file) as tag_o_file:
        reader = csv.reader(tag_o_file)
        for row in reader:
            issue = row[0]
            for t in row[1:]:
                print "executing tag for %s" %(issue)
                target.executeCommand(issue, "tag %s", (t))




if __name__ == "__main__":
    main()


