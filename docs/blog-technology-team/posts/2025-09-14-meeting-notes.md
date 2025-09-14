---
date:
    created: 2025-09-14T14:00:00-05:00
---

# Notes

## Agenda

- Notes
- Introductions
- Accessibility Proposal from Dain
- Project Management and Strategy questions
- Where to put Tech Team notes?
- Forums
- Gitlab vs Github
- Strikecard

<!-- more -->

## Attendees

Jeff, Kristen, Carl, Jason, Starrise, Pandeaux, Dude, SeokCheon

## Agenda Notes

- Starrise taking notes
- Introductions
- Accessibility Proposal
    - Main Points
        1. Team Channel Restructure
            - Great idea, should help keep discord server cleaner
            - Needs alternative communication tools
        1. Accessibility and DEI Teams
            - See "Ideas" in this agenda item, below.
        1. Workflow Needs
            - Work Platforms
                - Chat
                    - Discord
                - Structured Forum
                    - NodeBB
                - Unstructured Forum
                    - Lemmy
        1. Onboarding New Team Members
            - How do we get people onboarded onto each team?
            - Need a documented internal process for what needs to happen
                - On-boarding for each tool
                - Customer-service oriented mindset and approach
            - Only for Tech Team
        1. Mission Statement ...
    - Ideas
        - Add part 2 ("Accessibility and DEI Teams") to docs as guidelines for projects
        - Add issues for each "Work Platforms" project we want to roll out in project repo
        - Increase formality around client interactions
            - Stakeholders
            - What are needs?
            - What has been discussed?
            - Proposals
            - Consensus and Decisions
        - Who can step up to interact with clients?
    - Clients
        - Content Team
        - Accessibility Team
- Project Management
    - Accountability
        - Who is working on what should be recorded in projects repo.
        - Decisions made should be recorded in projects repo.
    - Strategic Planning
        - Put my top-level thoughts in projects repo.
    - Needs
        - Live document editing and collaboration
        - Alternatives
            - Jira
            - Trello
            - Notion
            - Nextcloud:
                - <https://nextcloud.com/install/#instructions-server>
                - <https://github.com/nextcloud/server>
                - oauth: <https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/oauth2.html>
                - PM "deck": <https://github.com/nextcloud/deck>
                - Possibly soft-limited to 500 people due to server congestion issues: <https://nextcloud.com/de/pushnotifications/>
                - We can work around this by limiting these servers to the teams themselves.
                - Nextcloud is not intended for wide-spread dissemination, but for limited-scope collaboration and sharing
            - OnlyOffice: <https://github.com/ONLYOFFICE/CommunityServer>
            - GitLab: <https://about.gitlab.com/install/>
            - OpenProject: <https://www.openproject.org/>
        - Don't use
            - Proton
            - Double-encrypted, single-source
    - Action Items
        - Identify and research PM tooling: Kristen
- Where to put Tech Team notes?
    - GitHub pages?
        - All info recorded is publicly accessible. Good (transparency, accountability) and bad (restrict what info we record)
        - Monorepo for all TT and project notes
            - Single repo, easier to track and update
        - Each in its own project
            - May be harder to keep track, multiple docs to work on.
            - A bit easier to find relevant material
    - Forums?
        - Easy to find
        - May be slightly more proprietary (can hide forums from people who are not registered or don't have permissions, maybe)
    - Decision: let's be accountable, continue with no-sensitive, on GH pages for now.
- Forums
    - NodeBB exists
    - Structure
        - Organization of topics
        - Organization of roles/permissions
- Gitlab vs Github for tech stack
    - Gitlab
        - Fewer people familiar
        - Slightly less easy to access
        - Project management tooling baked into git workflows
            - Epics
            - Labels
            - Milestones
            - Kanban (issue boards)
            - Deadlines
            - Timelines
            - Project nesting (and the above scope with nesting)
        - Has pages
        - Can import from Github URLs: <https://docs.gitlab.com/user/project/import/github/>
        - Migration guide: <https://about.gitlab.com/blog/github-to-gitlab-migration-made-easy/>
        - What about CI/CD transliteration?
    - Github
        - More people familiar
        - Easier to access up front
        - Project management not baked in quite as straightforwardly
        - Has pages
    - Consensus for now move to GitLab
    - William will explore what it takes to get to GitLab
- Strikecard
    - Carl: Holding off until Strikecard Meeting

## Parts we must have to assist with Team/Chapter launches

- Technology stack
- External-facing Reference documentation
- External-facing Educational materials
- Internal-facing Reference documentation
- Project management
- Purpose (mission, vision, goals, scope, values, expectations, accountability)
- Processes
    - How to build a team
    - How to onboard a team member
- External communications and feedback
- Lifecycle management
- People management

## Technology Resources

- Pandeaux showed off a self-built tool Kaleida: <https://justinpando.github.io/kaleida/>
- Nextcloud:
    - <https://nextcloud.com/install/#instructions-server>
    - <https://github.com/nextcloud/server>
    - oauth: <https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/oauth2.html>
    - PM "deck": <https://github.com/nextcloud/deck>
    - Restrict public sharing: <https://docs.nextcloud.com/server/latest/user_manual/en/files/sharing.html>

## Open Questions

- Can Nextcloud work with Markdown?
    - <https://apps.nextcloud.com/apps/files_markdown>
- Can Nextcloud have static/cached read-only publishing of documents?

## Action Items

- Create self-hosted tooling
    - Structured Forum: NodeBB (Jeff)
        - Jeff hass live
        - Everyone should experiment with NodeBB
            - Organization of topics
            - Organization of roles/permissions
            - Theming and accessibility
            - Play with themes
    - Project Management Tooling and Live Documentation (Jeff, Jason)
        - Nextcloud
        - Jeff will test
        - Jeff will notify us when NextCloud is ready via Discord
        - Jason will assist with oauth setup
    - Unstructured Forum (e.g., Lemmy)
- Justin will write down ideas for how to structure teams
- William will explore and research what it takes to migrate from GitHub to GitLab
- Jeff will add Pando to GitHub

## Site naming

- Nextcloud:
    - `<team>.gsus.tech`
    - `<team>.docs.gsus.tech`
- NodeBB:
    - `forum.gsus.tech/<state-or-us>`
    - `<state-or-us>.forum.gsus.tech`
- Lemmy:
    - `forum.gsus.tech/<state-or-us>`
    - `<state-or-us>.lemmy.gsus.tech`
