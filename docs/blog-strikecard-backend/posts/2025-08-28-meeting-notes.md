---
date:
    created: 2025-08-28T18:00:00-05:00
---

# New Strike Card - Meeting 2025-08-28

## Attendees

Jeff, Joe, Hiram, Dragon, Jason, Corwin

## Needs and Updates

- Dragon
    - not much time to work, getting familiar with the project
    - discussion of audit log granularity
    - decision to unite data at view (vs customizing on-save actions for individual components)
- Jason
    - working on production server setup scripting
    - Scripts could use code review (Corwin volunteers)
    - Issue branch needs a PR; will take care of this and send corwin a link
- Hiram
    - busy this week, next project is ansible configurations
    - have untested guest OS configs; shared these on Discord
    - learned about Ansible's clould management facilities (managing the VPS or a whole VPC)
    - this does appear to support Hetzner cloud
    - direction that this is a good item to continue researching, seems like it will work for us
    - focus on interior stuff; we can do the VPS/VPC provisionally manually if needed
    - Q: does the main application have a start stop function?
        - in paticular the PGSQLDB, considering cases of restore, given Django will manage the framework
        - A: the application will handle the DBs state; we will not manually restore the DB vs what is in backups but can assume that starting the restored system will correct DB schemas to current if there have been changes since the backup was made
- Joe
    - joining the call for the first time; some of these aren't accessable to me as tasks
    - call was helpful from a testing perspective and will share thoughts back with that team
