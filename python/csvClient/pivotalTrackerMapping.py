
"""
Mapping used for Pivotal Tracker

Must be used in conjunction with the pivotal tracker csv pre-processor

#http://confluence.jetbrains.com/display/YTD5/Import+from+a+CSV+File?_ga=1.8473011.766298216.1386850228
"""
__author__ = "ryan - KoanCode"

import csvClient

csvClient.DATE_FORMAT_STRING = "%b %d, %Y"

csvClient.FIELD_NAMES = {
    "Project"       :   "project_name",
    "Title"       :   "summary",
    "Created at"       :   "created", # created is a date
    "Description"   :   "description",
    "Requested By"      :   "reporterName",
    "Type": "Type",
    "Current State" : "State",
    "Comment" : "comment"
    }

# already added
csvClient.FIELD_TYPES = {
    "Fix versions"      :   "version[*]",
    "State"             :   "state[1]",
    "Assignee"          :   "user[1]",
    "Affected versions" :   "version[*]",
    "Fixed in build"    :   "build[1]",
    "Priority"          :   "enum[1]",
    "Subsystem"         :   "ownedField[1]",
    "Browser"           :   "enum[1]",
    "OS"                :   "enum[1]",
    "Verified in build" :   "build[1]",
    "Verified by"       :   "user[1]",
    "Affected builds"   :   "build[*]",
    "Fixed in builds"   :   "build[*]",
    "Reviewed by"       :   "user[1]",
    "Story points"      :   "integer",
    "Value"             :   "integer",
    "Marketing value"   :   "integer"
}

csvClient.CONVERSION = {
    'State': {
        'unstarted' : 'Submitted',
        'started'   : 'In Progress',
        'finished' : 'Fixed',
        'delivered' : 'Fixed',
        'rejected' : 'Reopened',
        'accepted' : 'Verified',
    },
    'Priority': {
        'High'      : 'Major',
        'Low'       : 'Minor',
        'Urgent'    : 'Critical',
        'Immediate' : 'Show-stopper'
    },
    'Type' : {
        'epic' : 'Epic',
        'feature' : 'Feature',
        'bug' : 'Bug',
        'chore' : 'Task',
        'release' : 'Release'

    }
}
