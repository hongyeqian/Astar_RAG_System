# data003
[00:00] William: I can record, and we don't have a ton of items to get to. I might be able to do one that might be fun if we have a little bit of time. So corporate events, I think I saw a little—I put this in Slack and I saw a little bit of kind of noise around it, which was good. The nutshell here is, as we've kind of restructured and tried different things, the event support that we need isn't as nailed down as it needs to be. So the current tactic that we're going with is: go-to-market team signs up 1and kind of sponsors that event, so you support it as a PMM, your campaign manager does the campaigns for that event, et cetera, et cetera. I don't see anyone in the issue—maybe there are comments in the issue—I don't see the header updated yet. I thought we had in Slack sort of farmed each one of them out. So, I guess the next—it looks like Tai put in some folks. This looks good. So that, let's see, need support from GTM teams. So I guess the ask would be to work with your GTM team. So, did—let me ask that. I saw some Slack, I think in our Slack, but did you all, were you all able to connect with like your GTM teams?

[01:56] Cindy: On Slack only and on the issue, actually. Yeah, same. Not even not in real time, but you know,

[02:03] Samia: I got one person to respond so far. So it may end up, Cindy, being you and I just picking the one that we want to do, and then they can back us up.

[02:14] Cindy: Yeah, do y'all—does anybody have like a regular sync still? Are those all been canceled, or is there cases?

[02:24] Samia: Don't have a regular. Yeah, we're on like a two-week cadence. Okay.

[02:34] Brian: Yeah, GitOps has been canceled after the enablement.

[02:42] William: Cool. So I'm just trying to catch up with the thread. So it looks like maybe Platform on ReInvent, CI/CD on Google Next, and GitOps on KubeCon. Does that sound right?

[02:58] Cindy: Yeah, yep, that's where we were last I heard. Cool.

[03:09] William: So then I think we can help the corp events team. They do, they do a lot of like cat hurting and, you know, keep on tracking people down. So I think if this team can take the mission to like try to help track that down, so if you, you know, get the commitment specifically from your campaign managers, "Hey, like we're signing up for KubeCon," you know, "Can you comment on the issue that yes, I can commit to this, etc., etc., etc., you know," so that just so that they can get that event support. But that looks good. And I appreciate... thanks for the link to Samia on the rolls. Product announcements. So I appreciate Brian for adding this. I probably should have added it, but I had two questions about that. One is over what timeframe are we looking at? ... What do you think, Cindy?

[05:47] Cindy: Yeah, I think I was inclined to group some things to say like vulnerability management because there were tiny little MVCs all the way along, but if you look at over the course of the year, we went from this to this, it makes more sense to me to highlight that than any individual little thing. And then the other point was, we just had 14.0, can we just, can we reuse some of those things and plug them in here?

[06:17] William: Absolutely, yeah. Yeah, and vulnerability management was, was one of the, you know, the features out of we looked at 14.0. So I think, yeah, this is like let's take the stuff from 14.0 and then maybe add a few more so that we can hit kind of different areas of press or give, give our PR team—this is kind of like input into our PR team to give them fodder to go out with.

[06:44] Cindy: And are we trying to hit three per stage?

[06:46] William: I, yeah, ideally there's just, you know, three, three items per stage. And then I think y'all made some good notes that, okay, we need to add Manage. So I see Manage in here, that's excellent. And, uh, Integrations, we don't, well, actually we have some pretty exciting integrations. So we have the Jira stuff is pretty good. There's a couple of things in, uh, integrations with VS Code that could be notable.

[07:14] Brian: But can I show what I did for SCM just to get some general feedback on it? And if someone hasn't done it, maybe that will also—

[07:23] William: Okay, I was going Cindy's direction here, which was uh, thinking, you know, a lot of, and then I called them key iterations, the sort of specific things... I don't know what everyone thinks about that.

[09:04] Cindy: I like that.

[09:10] Samia: I've done a similar, I've taken a similar approach for Monitor, with incident management. There were a bunch of things that we released, although the core of incident management was part of 12.X, I think. So I did the same over there as well. Yeah, I think that makes sense. Yeah, and that that would help me with the Plan stuff as well because there are some things like Epic Boards that people have been asking for for years now, and they finally have and that's great. But I think, you know, like the the Milestone Burn-up Charts, that that was a two and that's that's helpful...

[10:02] William: And also, Brian, about the VS Code thing, one other cool thing about that is both of those VS Code integrations that hit the same month were community contributions, which is also kind of cool.

[10:16] Brian: Is, is that, is do we have VS Code listed on here? I didn't add it but I can.

[10:25] William: I can add that in. I've got good notes on that. The extension that had been around for a while became official was kind of one of the things, but there's some other stuff that's a little juicier than that and that I think that's a, that's a pretty good note as well. We did that with like our, our Terraform module, right? There was like a community module, but now it's officially supported. So that's that's the, you know, that can be the line, yes or no, whether you can use the thing for a lot of businesses. So I think that's a good one too.

[11:03] Samia: How are we measuring excitement levels: one, two, and three? Is—

[11:06] Samia: I was, I was looking at maybe MAU as a metric to perhaps measure whether customers have started using that, are interested in using that or not. We probably may not have it for everything, but at least some of it, wherever we have it, it's probably something we can, we can use. Yeah, but we, of course, we need a benchmark level of what MAU we want to call one, two, or three.

[11:38] William: I, I think it's a little, it's a little bit of a judgment call. Like, for example, Cormac was saying, like Epic Boards is something that was asked for for a long time. Now, depending on how it's asked for, maybe that means it's exciting or it's not, right? But usually when something gets a lot of upvotes or when there's a lot of demand for it, then I would, I would bump the excitement level on something like that...

[12:34] Brian: Harsh responded to my comment about why we have the low excitement ones and just said something about having him sort of stack-rank.

[12:54] William: I might even constrain this is we're not going to highlight log segments, but we want to see the full spectrum, especially in the case we have slim pickings. Alternately, if there are double-digit entries, then we can stack-rank. So that's, that's kind of also helpful there...

[13:39] Brian: Hard somebody's one or somebody's three may be more important than somebody else's one, depending. And I had, I started by just looking at what was considered a key feature over the past year from from Create. And, you know, there are at least a dozen things that I'm not mentioning that could be on the list. Like, I could give you ten things instead of three.

[14:04] William: Yeah, give it, give this just like the rough, like pass. And, like, a lot of things recently I've been moving between docs and spreadsheets and the spreadsheet to docs. This, you know, this might, this might end up or some iteration of this might end up in a spreadsheet where we then try to stack-rank in PR is like, okay, out of all of like the, you know, there's maybe ten boxes here and three each, out of the 30 items, which are the top five? Actually, let's just, let's actually just do that. Let's just do this like top top five overall.

[14:44] Cindy: This one is a PR-driven to some degree. What about like the Noob and Christie's product keynote at Commit, are—

[14:48] William: We tailing this with that? So, so this is exactly where this is headed to, is the idea that, during the product keynote and then ideally during Sid's keynote as well, that there's some level of like an announcement that we make that then the press cares about that announcement. Again, really tough to do at GitLab because it's all been around for a while. So this is, this is our attempt to head to that area is to say like these are the announcements of the event. And yeah, maybe it's some things that have been around for a while, but like now they're at a level of maturity, now, you know, there's, there's reason to be excited about this. So that's kind of where it's coming from. So I put a top five overall. Maybe we can just, you know—

[15:48] Samia: We should reserve a spot for Plan, but I'm going to have to go through and do some aggregating after this. Just go through the list of what's shipped in the last 12 months and re-bucket that. So—

[16:09] William: Maybe we can do like a five minutes kind of like, um, just just time boxing, uh, kind of look at these here. What do, what do you all think is, uh, top would be a top five out of the list of, you know, 20 or 30?

[16:26] Brian: I would say if UX does end up being a flag that we fly, that's an easy one because there's more than just maps to the Create stage that would be considered UX improvement. Okay.

[16:46] Cindy: What else? We need to have a security one in there. We could have either vulnerability management or, um, I was, what I've been struggling with a little bit is I'd like to kind of group the, um, some of this the proprietary scanning, without making it sound like they're scanning improvements because that sounds like they weren't good before.

[17:15] William: Yeah, I, let's, let's go with vulnerability management for now. I, I, and I would agree on that one. And I would say that, um, some of these we did do some press around and the the fuzzing acquisitions was one thing. So we might not get that kind of old. I was, I mean, we did the fuzzing acquisitions a long time ago. Was it within the past year or longer?

[17:47] Brian: I thought it was in the last little over six months or so. It was last summer, right? Or—

[17:52] William: Something around there. It was like last spring or summer. And then we did another set of press around the integration of it because the PR team liked all the, I mean, we got a lot of attention on the acquisition. So they had me do a follow-up on the integration. I just feel like it's kind of worn out now. But—

[18:14] Cindy: That's what I was saying is that the the fuzzing we already did press on, so we probably will not get another chomp at that. So I think let's go with vulnerability management unreviewed. But we also have in terms of proprietary stuff, we've also got we replaced one of our scanners with Semgrep, and we did, um, we have our own proprietary DAST scanner now that's in—it's in beta—called Browser. So it's our answer to scanning single-page applications which represent a unique challenge. I think, I mean, if I could have two, it would be vulnerability management and Berserker, probably.

[18:58] William: Okay. Semgrep could get picked up as an online item and a couple of the pieces about GitLab 14.

[19:07] Cindy: Which between, between the the proprietary ships and the vulnerability management, which would you pick as number one out of those two?

[19:14] William: Those two, probably vulnerability management. Okay. I'm just kind of scanning the list. I would probably say like Kubernetes Agent is something that we've made a lot of investment in, although—

[19:35] Samia: I think the Kubernetes Agent and from an integration point of view, perhaps the Terraform integration. I think we have a lot of customers actually using that already.

[19:48] William: I'm going to agree. I'm just going to call those GitOps and I'm going to put like KS Agent plus HashiCorp integrations. It's like a bucket of capabilities that is probably worth talking about.

[20:18] William: Cool. Well, let's, you know, let's try to, uh, this is due Tuesday. I think we want to try to get this done. So maybe just, uh, review this kind of like, let's just kind of pick top five. Maybe something from Planning, something from CI/CD. Yeah, Pipeline Editor is definitely an option for CI/CD.

[20:43] Cindy: Yeah, there might be, no sorry, there might be a Value Stream Analytics story in there too. If we aggregate it all, it's it's a bummer that Customizable Value Stream Analytics is 12.9, but, uh, yeah there might be.

[21:06] William: Cool. Now I'm just going to, I'm going to ping you on this, Cormac, to add at a top five.

[21:14] Samia: Cool. Uh, I think that's a pretty heavy, pretty heavy list. Just looking at it, you know, it's pretty cool.

[21:28] William: Yeah, and this is something we don't do, which I, I agree. Like, we don't, we don't often stop as a company and just kind of look at our wins.

[21:40] Brian: No. Uh, I was really—I don't—did y'all—did anybody miss Assembly?

[21:51] William: Um, if you missed it, I recommend it. I laughed because, like, what Assembly reminds me of is like when I was in like a young child in grade school...

[22:15] Brian: Put everyone in the gym or like convert the half-cafeteria gym, you know, take away the big barrier between it so that we can have more room and then take those carpets that have never been cleaned and just, you know, sit on them and it'll be, it'll be great.

[22:31] William: Beside, aside from the goofy name, I thought that, and of course we can't talk about any of it on YouTube, but man, that was like a really awesome look back at like, here's some wins and here's some exciting things that we've done. And so I think we just need to get better at this as a company. I think this exercise is an opportunity that, um, I think we do a little bit of that, but this is doing it more so. Uh, Samia, you have some questions here for Elita?

[23:04] Samia: Yes. So in the competitive sheet, I was—I mean, I've already identified the features for CI/CD Configure as well as Monitor. Getting it reviewed from PM, my guess was, or my understanding was that we wouldn't have the same set of competitors that we're going to compare to, but the right competitors for that particular stage, right? So for example, for Monitor, we may not have like a GitHub or something like that. We would have Monitor-based competitors, or was that the understanding? Because we identified that entire list of competitors and partners for every single stage. I thought we were going to be using those competitors to compare against, so I just wanted your input on what—because I saw some of you have compared with the five competitors already listed over there. They may not be relevant, for example, CloudBees may not be relevant for Monitor stage at all. So that's what I wanted to check with you.

[24:08] William: Yeah, that's the case. I need to go back and look at the spreadsheet. I mean, if the competitor does not apply to that particular stage, they shouldn't be on that tab in the spreadsheet. So are you saying that you see competitors on that tab for a stage where they don't apply?

[24:26] Samia: Yeah, I think it was copy-pasted. Each Google has the same. Yeah, so each sheet has has ADO, Atlassian, GitHub, Jenkins, J-Frog, and CloudBees, right? So that may not be relevant for Monitor. For Configure, it would be a different set of competitors that we need to include, which I think we already identified a while back.

[24:43] William: I think we identified top three competitors for every stage. Yeah, we tiered them. That's when we tiered them, right? Tier one, tier two, tier three. So this, this where we are right now, is we're looking at just tier one competitors. That's probably why I cut and paste them because those are all tier ones. So we're just 2focusing on tier one right now. So if they don't apply to that stage, don't worry about it. Makes sense.

[25:07] Samia: So just pick the ones out of that list that apply to our stage, right? I just, will just use the tier one competitors and if they're not, if they don't are not applicable, then we don't have to fill out anything for them.

[25:15] William: Yeah, for now. But then we'll move to tier two and tier three. Then we'll look at those other.

[25:28] Samia: Okay. Do we need to add a line item for GitLab as well because I, I—

[25:39] William: I'm just looking at it, Brian. Um, yeah, we're good. Yeah, because the way without it, you're—

[25:48] Brian: Basically putting all the things that we're better at. Yeah, for sure, for sure. Yeah.

[25:56] William: Right. Ideally when we picked like the 10 to 15 features, though, some of those were like GitLab only, some of those were like—

[26:03] Brian: Well, I thought it was supposed to be none of them should be GitLab only, right? It should be all through the lens of, yeah, yeah, exactly.

[26:07] William: Yeah, it should be like market lens. So, yeah, in an ideal world, most of them are like, "This is what I'm shopping for this solution." Some like, some of them might be GitLab only, some of them like competitor only, so that it's a—somebody would look at it and be like, "This looks honest and trustworthy and like a accurate assessment of the market there." Yeah. And then, yeah, I think Samia, for this, just to kind of reiterate, for this one, we're only doing these five competitors, so we'll do the other ones in a later stage...

[27:03] Brian: Yeah, yeah, Jenkins CloudBees does not. Yeah, but, uh, what is—

[27:09] William: You know, Azure DevOps, GitHub, Atlassian, and although Atlassian's we still need to figure something out there that—as a matter of fact, did I go back and add Atlassian? Because I, based on conversation, I think we have to do it. I don't think we can leave them off...

[27:33] William: Because based on discussion, like my, my I wanted to take them off completely and just leave them as a partner, but we can't do that. So, so yeah, so for for those platform, you know, we should call out the fact that they don't have any monitoring. If they have like zero out of 15, we should call that out. Same with Configure stuff or this, you know, any those kind of capabilities.

[28:01] Cindy: I think if we took that a step further, it'd be good to even describe it in a way that doesn't just say our product stage and use like a value-based description of what Monitor and Configure mean because otherwise, we're just, no, that's not going to do any good for us. Have you guys seen the new infographic that the uh, design team has come up with? Not yet. Oh, you haven't? No. Do we have a link to that quickly, William? I don't know, or you can throw it in the uh, you can throw it in the—

[28:22] Brian: Um, notes if you find it. All right, let's see who can find it faster. Guarantee it not with the—

[28:35] William: amount of tabs I have open. Oh my god. That's what I'm like, it probably won't be me. So I—

[28:47] Brian: Gmail because the search is so fast. So I literally have a folder where all of my GitLab pings go and I can just search for infographic and, well, I found it. I found it. I found it. Who can link it first? I found it. I found it. So—

[29:06] William: This is the one. So, this, there's two. This is the one for the single tool comparison, but then for the, but it's going to look the same. But then here's the one for, I just put it in chat for you guys, and here's the one for the platform players. So, so we made it, we made a couple decisions along the way...

[31:07] Cindy: Okay, so we will have a number two. That, because I was about to say you're going to hate me for this, but like, we're, we're, we're being cyclical about the same problem we had, which being the audience coming in and not knowing anything about these specific stages. That was one of the big things. It's like, okay, 15, 15 features, what, what is, what are they? Why do I care? You know, better? Yeah, to say that means nothing to me looking at this, this page. Quick questions, I'm not going to be a Debbie Downer. That's it.

[31:37] Brian: No, we're on top of it. Actually, if you read the thread, I brought that up, but she said we can't do it like right now, which I understand. But small thing, what do you guys think about the colors? I don't know, I usually let the designers handle that stuff. They, they, I, I like, yeah, I, I like the fact that there's no red on there. Oh, you like that? That's what I was going for. You liked it? Okay, it's not, it's not obviously negative.

[32:05] William: So we're saying because it really does lend itself to being a comparison more than a competitive piece because of that, because there's no, you know, "These folks at 37 are in the red and they're terrible." They just have less green, or we would have less green. So it's not, it's not being worse, it's being less good. And I, I think that, I think that lends itself to working with, you know, your all the coopetition situations we're talking about.

[32:37] William: Industry, this is not just like marketing shill. This should be like a helpful page. So it's like, yeah, the goal is to have a comparison comparing DevOps tools, not a, you know, "This is all of our competitors and why we're better." Yeah.

[32:53] Brian: I, I, I think from a competitive mindset and for me, I'm like, "Let's go hard. Let's put some red on there," and that's just the way I think, right? So but I brought it up and that for now we're going to stick with the green. They recommend it. We stick with the green and, uh, see how it goes. But I don't know, I was feeling the red and yellow too. So—

[33:14] William: Cool. Well, we're almost up on time, but I did want to share one thing that kind of came in like basically Friday. It was like late Thursday for me. So this, uh, this is another thing a lot, a lot of these things I don't have like a ton of context on... So this is a little bit of a messaging framework, and then the assignment that was given to me was to to fill in these boxes here...

[35:00] Brian: So what's the difference between that slide and the next one that doesn't have anything under Security? This, this was the—

[35:04] William: Honestly, so that, so when I first got this, it didn't have this and it didn't have anything under Security. So this like, what I'd do is just—

[35:10] Brian: Your iteration of it.

[35:13] William: Yeah, this is this is mine. This is. I just put here so that I would have like the original statements, like, you know, "Automate nearly anything, collaborate on everything." I kind of like that, but I, you know, this one I hate: "Scale up, speed up, test up." I don't think anybody "tests up." I think that's really goofy.

[35:36] Brian: So you hate it. Uh, this—

[35:39] William: I love that. For me, it's I, I love it or I hate it, right? I love how—

[35:43] Brian: I love how you're just like, "Bam."

[35:44] William: So anyway, the what I love in just in five minutes now, and then we can just kind of end the call, is kind of like, anything that you would change this out for, anything that you would change this out for... No, but you can say "More speed, less risk." I like that one the best. I don't like the last one. Okay. I agree. That's, that's why I put this one at top was for that parity... So, yeah, good.

[37:10] Brian: Cindy's last blog post had a really good turn of phrase that I stole from, forgive that 14. When she was out, it was like, "Secure the software factory and all the stuff that you're making in it." She said it really elegantly, and so I just kind of ended deliverables, "Secure the factory and its deliverables." Yeah, I thought it was good to emphasize both because they mean different things.

[37:34] William: Yeah. So you could say, um, "Secure and control your software factory and its deliverables." Maybe that would encompass both.

[37:50] Cindy: I'm, I'm not a big fan of the "it's it's deliverables." Is there—can we say like your software factory in your software or your, your sub or in your product? Sounds like car manufacturer. You can say "IP" here, but it just doesn't sound right and that's always, it's always shorthand. Yeah, I like this one better. Yeah.

[38:22] William: And then the last thing I'll say is, so this is, this is my attempt to channel my inner Ash Withers. I think Ash is like super good at just, again, just like the catchy or like the turn of phrase element to it... So, so here I was trying to like envision what is it that we actually give you with this philosophy. It's like, it's "velocity with confidence" is what is what you get.

[39:00] Cindy: I like your "Move fast with confidence" better than "Increase speed and stay on track."

[39:03] William: Yeah, so I was trying to, I was thinking of like, you know, if you're like, if you're in a race car and like you go like super, super fast... So trying to encapsulate that in this like, that was kind of where I was like "Stay on track," but I didn't like it either. Did you just open the door for a NASCAR partnership? Hey, NASCAR goes fast and turns left because of GitLab.

[40:08] Brian: So you're our new Ricky audience demographic. So, yeah, so I don't think I like that one. And then I think between these two, I like "Move fast with confidence," but I don't like the the verbiage of it because it doesn't have parity. So that's where I think, do you want to add, maybe we can add "high confidence" or "more confidence" at the end of your first statement, so it kind of combines all of it? So "more speed, less risk, high confidence" is kind of overused anyway... I really like the first one, just "more speed, less risk," bam. "No trade-offs." You know, just that's how it is.

[40:43] William: Ooh, "no trade-offs." That's one of my go-to's. I love that one. This, this gets into the, uh—

[40:54] Brian: "No trade-offs." The engineer in me says there's never no trade-offs. That's like saying like 100% secure.

[41:09] Cindy: Everything with messaging, right? I mean, not everything. You know, how about just "more speed, less risk with confidence"?

[41:25] William: Yeah, "more speed."

[41:28] Brian: The Ricky Bobby and me really did like the "no trade off." So, Parker, yeah. Oh, is that, was that—

[41:34] William: from, uh, no, but it could have been. It's something Ricky Bobby would have said. If anyone hasn't seen Talladega Nights, they should. That's the homework for this weekend. We talk about it on Monday in our little social report.

[41:46] Brian: I often say, "Thank you, little eight-pound, five-ounce baby Jesus with the golden diapers." I say that so often that I just think everybody has seen Talladega Nights, but then I realize that people that haven't are like, "William's really weird." And then next week we'll watch Step Brothers. That's another great one. "So much room for activities."

[42:08] William: Okay. Um, I'm going to go with, uh, "more speed, less risk," and um, I think this is due at the end of the day. So, any additional thoughts? I'm actually going to un-tag me. It's strong. All those are, you know, cool. Those are good. Awesome. Well, uh, this was kind of fun to do a little bit of like working together session and, uh, keep a little dazzle, keep it rocking. Good to see everybody. See you soon.