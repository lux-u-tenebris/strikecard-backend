---
date:
    created: 2025-08-31T14:00:00-05:00
---

# Technology Team - Meeting 2025-08-17

## Agenda

- Project Updates
- Media Server
- Strike Card
- Matrix
- Email
- Async Communication
- Forums
- Documentation

<!-- more -->

## Attendees

Jeff, Worms, Stacy, Rachel, Yason, Corwin

## Updates

- Media Server
    - no updates (Corwin did not connect with DJ, Taylor is vetted and has access now but not admin)
- Strike Card
    - Rachel will try to jump in to help with some UI (or other, maybe) stuffs
- Matrix
    - Ora hasn't been at last couple meetings
    - leaning to table this for now to focus on forums or other tools specifically aimed at coolaborative work (writing together, especially)
    - Jason has been experimenting in this direction, discussion of trying to get Strike Card out the door and then change focus (vs. multitask)
- Email
    - forming committees to design email hosting and technical design for sending email from software (automated SMTP)
        - Yason (AWS SMS research)
        - Rachel (design of email, work with Content Creation Team)
        - Corwin (will wrangle volunteers but think that the "all-call" to tech team volunteers in discord is perfect for the design task).
- asynchronous comms
    - Worms has looked into Matrix some, compares well to discord but the security is good, does not have forums
    - Jeff talked about <https://zulip.com/> and asked that members look into this and share thoughts back next meeting
    - Jeff proposes that focus on sync comms is less important than having forums
    - worms: people may not want to give up on discord, will need to be really solid to bring people over
    - jeff: don't need to move people, just create an effective option for project work
    - proposed concensus: we should focus on forums over replacing sync comms
    - worms: representing the needs of all teams is important..
    - jeff: have been working with accessability and communications teams to come to the view expressed
    - worms: making this work well for Mutual Aid projects/groups will be critical
    - jeff agrees, asks for someone to be lieason for these groups/represent these concerns in design/planning
    - worms will do that!
    - we have concensus
- Forums
    - lots of software, lots of variety among them
    - federated or monolithic?
    - one big forum or lots of little ones?
        - Jeff: would like tech and accessability teams to lead structured dialog that is easily searchable and less overwhelming; assuming other teams would apprecaite this same thing.  asking for others' thoughts.
        - Jason: mentions some enhacements needed to experiment; Jeff: preference would be for something more establishd
        - Yason: Archive.org is using PBP BB for Forums; Corwin has a friend working at archive.org who could potentially bring resources forward for us (training, in particular)
    - Alternatives
        - Lobst.rs - a very simple retake on reddit (is it made with rust? we think so, nobody on the call has used it much); focus is more aggrigation than writing directly into the project
        - xmpp - would need to be hosted on a distributed system; many well established libraries for backend but would need major work on front end (would need to create the whole front-end)
        - discorse - Modzilla and Ubuntu use this for their forums (need someone to research this one also; the free software foundation uses this as the primary web-based member feedback option); appears well structured for doing work.
        - lemmy - also needs research (corwin likes this one, doesn't want to own the research for that reason); less web focused in the stack than other alternatives that make web-pages.
        - mastadon or bluesky - uses IPLD (what IPFS uses); not really focums focused but good to consider
    - Q: budgetary consideration?  Have been told to ask for what we need; trying to be cost conscience.
    - Q: Potential combine mastadon and forums?  Think there are use-cases for both and probably want to prioritize forums

General Ask for all tech team-members:
    Please research items from above and bring your thoughts to the next meeting
    - A desired feature would be supports for collective journalisim
    - Jeff: would self-hosting a social media program (BS, mastadon, ...) instance make sense (more control over who speaks on behalf of GSUS)
    - Worms: yes, this seems like an opportunity: practical solutions for the issues people have with less moderated spaces will motivate people to move to newer socials
    - concensus that this seemed like a good use of time, at the time
    - please also consider this as you look into the research items above (does a give tool have features that might motivate you to move socials?)

- Documentation: we have issues around collaborativly writing documents, finding them later, duplicated
    - this is a need at the chapter level also
    - corwin demoed NextCloud briefly
    - Discussion Q: would we want one bit instance or lots of little ones?
    - Research Note: consider single-sign on in context of researching forums and social media software (look for implications in what login providers we could support and how that would work. would the given program need to be the "source of truth" or could it be connected to an external identity store?)
    - (Stacy) researching next clould from the security standpoing; looks decent.  needs oversight from admins; did some light research into alternatives
    - onlyoffice (not recommending this over NextCloud at this point, but could use more research into it)
    - Resuming discussion of nextcloud which appears to be a concensus choice so far; one instance or several?
    - does have federation (could have national repository with documents federated into instance)
    - Yason and Worms to propose creating regional/chapter NextCloud instances; see about Federating with the test instance Corwin demoed; PM corwin on Signal or Discord for access to the test intance (be aware that it is experimental, keep copies of important things somewhere else for now)
    - indexing and dicoverability and reproducability (and backups)
    - discussion of reproducability (what does this mean?): create model for other orgs, be able to replace instances quickly if they are taken down
    - IPFS could be an option for distribution of data (effectively the same as backups but replicating live data);
    - worms has been experimenting with this, could dig into NextCloud+IPFS/IPLD.
    - Chumpy and Justin have also looked into this in context of an hackathon;
    - discussion of in-person vs virtual,
    - in-person may be ideal especially when there are security considerations to address during the development
- Carolia Website:  Yason wants to put the chapter website on hold while explore NextClould
    - NextCloud may be the solution to the more important parts of the problem.
    - problem statement: when people join the project/discord help connect them with projects and documentation, enable joining teams:
    - in the background this pushes data to a cryptpad.
    - chapter has been considering doing a stand-alone vs integrating with National and/or other chapters.
    - Jeff: new strike card project has a dataset that associates chapter information with trusted volunteers having the authority to access members' data submitted via signing the card; this may be reusable for the suggested feature (which seems vy cool); Jeff: would love to draw people into the strike card project if this kills energy to do web-development from the chapter we can def use it here!
    - ACTION item (corwin/jeff) create Project card to discuss Carolia website project at the next meeting
- Hackthons (walk-on, worms)
    - Jeff: would love to participate in a virtual one at the national level but I cannot organize that
    - Worm, Stacy: will work on that
- Q: Rachel (strike card): is there something I could work on for this in the next couple of days?
    - Jeff: several front-end tasks that need attention, e.g.
    - Strikecard UI <https://bru.st/i/chrome_W8wRhO3CN7.png>
    - Channel: <https://discord.com/channels/1054471846436798535/1379823231812501574>
    - Demo: <http://5.78.137.94:8100/chapters/>
    - Q: frameworks? Jeff: maybe avoid giants like React but generally open to what may be needed; Javascript may change under you but styling and validation should be stable to implement better UX
- Yason: consider how we will handle i18n (translations);
    - Jeff: this has come up, def a need, nobody has jumped into this.
    - Yason: this should be considered in selecting JS frameworks, some will have good (or at least some) i18n
