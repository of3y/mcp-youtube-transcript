# Andrej Karpathy: Software Is Changing (Again)

## Video Information

- **Video ID:** `LCEmiRjPEtQ`
- **URL:** https://youtu.be/LCEmiRjPEtQ
- **Title:** Andrej Karpathy: Software Is Changing (Again)
- **Channel:** Y Combinator
- **Duration:** 39:31 (2371 seconds)
- **Upload Date:** 20250619
- **View Count:** 163,411 views

## Transcript Metadata

- **Extraction Method:** yt-dlp
- **Language:** en
- **Line Count:** 2273
- **Generated:** 2025-06-19 17:23:37

## Available Languages

N/A

## Plain Text Script

Please welcome former director of AI Tesla Andre Carpathy. [Music] Hello.

So I'm excited to be here today to talk to you about software here today to talk to you about software in the era of AI. And I'm told that many of you are students like bachelors, masters, PhD and so on.

And you're about masters, PhD and so on. And you're about to enter the industry.

And I think it's actually like an extremely unique and very interesting time to enter the very interesting time to enter the industry right now. And I think industry right now.

And I think fundamentally the reason for that is fundamentally the reason for that is that um software is changing uh again. And I say again because I actually gave this talk already.

Um but the problem is that software keeps changing. So I actually have a lot of material to create new talks and I think it's changing quite fundamentally.

I think changing quite fundamentally. I think roughly speaking software has not roughly speaking software has not changed much on such a fundamental level changed much on such a fundamental level for 70 years.

And then it's changed I for 70 years. And then it's changed I think about twice quite rapidly in the think about twice quite rapidly in the last few years.

And so there's just a last few years. And so there's just a huge amount of work to do a huge amount of software to write and rewrite.

So let's take a look at maybe the realm of software. So if we kind of think of this as like the map of software this is a Um this is kind of like all the software that's written.

Uh these are that's written. Uh these are instructions to the computer for instructions to the computer for carrying out tasks in the digital space.

So if you zoom in here, these are all different kinds of repositories and this different kinds of repositories and this is all the code that has been written. And a few years ago I kind of observed that um software was kind of changing and there was kind of like a new type of software around and I called this software around and I called this software 2.0 at the time and the idea here was that software 1.0 is the code you write for the computer.

Software 2.0 you write for the computer. Software 2.0 know are basically neural networks and know are basically neural networks and in particular the weights of a neural network and you're not writing this code directly you are most you are more kind directly you are most you are more kind of like tuning the data sets and then of like tuning the data sets and then you're running an optimizer to create to create the parameters of this neural net and I think like at the time neural nets were kind of seen as like just a different kind of classifier like a different kind of classifier like a decision tree or something like that and so I think it was kind of like um I think this framing was a lot more think this framing was a lot more appropriate and now actually what we appropriate and now actually what we have is kind of like an equivalent of GitHub in the realm of software 2.0 And I think the hugging face is basically equivalent of GitHub in software 2.0.

And there's also model atlas and you can visualize all the code written there. In case you're curious, by the way, the giant circle, the point in the middle, uh these are the parameters of flux, the uh these are the parameters of flux, the image generator.

And so anytime someone image generator. And so anytime someone tunes a on top of a flux model, you tunes a on top of a flux model, you basically create a git commit uh in this space and uh you create a different kind of a image generator.

So basically what we have is software 1.0 is the computer code that programs a computer.

Software 2.0 are the weights which program neural 2.0 are the weights which program neural networks. Uh and here's an example of Alexet image recognizer neural network.

Now so far all of the neural networks that we've been familiar with until recently where kind of like fixed recently where kind of like fixed function computers image to categories function computers image to categories or something like that. And I think or something like that.

And I think what's changed and I think is a quite fundamental change is that neural networks became programmable with large networks became programmable with large language models. And so I I see this as quite new, unique.

It's a new kind of a computer and uh so in my mind it's uh worth giving it a new designation of software 3.0. And basically your prompts software 3.0.

And basically your prompts are now programs that program the LLM. And uh remarkably uh these uh prompts are written in English.

So it's kind of a very interesting programming language. Um so maybe uh to summarize the Um so maybe uh to summarize the difference if you're doing sentiment difference if you're doing sentiment classification for example you can classification for example you can imagine writing some uh amount of Python to to basically do sentiment classification or you can train a neural net or you can prompt a large language model.

Uh so here this is a few short prompt and you can imagine changing it and programming the computer in a and programming the computer in a slightly different way. So basically we slightly different way.

So basically we have software 1.0 software 2.0 and I have software 1.0 software 2.0 and I think we're seeing maybe you've seen a think we're seeing maybe you've seen a lot of GitHub code is not just like code anymore.

there's a bunch of like English interspersed with code and so I think kind of there's a growing category of new kind of code. So not only is it a new programming paradigm, it's also remarkable to me that it's in our native language of English.

And so when this blew my mind a few uh I guess years ago now I tweeted this and um I think it captured the attention of a lot of people and this is my currently pinned tweet uh is that remarkably we're now tweet uh is that remarkably we're now programming computers in English. Now, programming computers in English.

Now, when I was at uh Tesla, um we were working on the uh autopilot and uh we were trying to get the car to drive and I sort of showed this slide at the time where you can imagine that the inputs to where you can imagine that the inputs to the car are on the bottom and they're going through a software stack to produce the steering and acceleration produce the steering and acceleration and I made the observation at the time that there was a ton of C++ code around in the autopilot which was the software 1.0 code and then there was some neural nets in there doing image recognition nets in there doing image recognition and uh I kind of observed that over time and uh I kind of observed that over time as we made the autopilot better as we made the autopilot better basically the neural network grew in basically the neural network grew in capability and size and in addition to that all the C++ code was being deleted and kind of like was um and a lot of the kind of capabilities and functionality that was originally written in 1.0 was that was originally written in 1.0 was migrated to 2.0.

So as an example, a lot of the stitching up of information across images from the different cameras across images from the different cameras and across time was done by a neural network and we were able to delete a lot of code and so the software 2.0 stack quite literally ate through the software stack of the autopilot.

So I thought stack of the autopilot. So I thought this was really remarkable at the time and I think we're seeing the same thing again where uh basically we have a new again where uh basically we have a new kind of software and it's eating through the stack.

We have three completely different programming paradigms and I different programming paradigms and I think if you're entering the industry think if you're entering the industry it's a very good idea to be fluent in it's a very good idea to be fluent in all of them because they all have slight all of them because they all have slight pros and cons and you may want to pros and cons and you may want to program some functionality in 1.0 or 2.0 or 3.0.

Are you going to train neurallet? Are you going to just prompt an LLM?

Should this be a piece of code that's explicit etc. So we all have to make these decisions and actually potentially uh fluidly trans transition potentially uh fluidly trans transition between these paradigms.

So what I between these paradigms. So what I wanted to get into now is first I want to in the first part talk about LLMs and how to kind of like think of this new paradigm and the ecosystem and what that looks like.

Uh like what are what is looks like. Uh like what are what is this new computer?

What does it look like and what does the ecosystem look like? Um I was struck by this quote from like?

Um I was struck by this quote from Anduring actually uh many years ago now Anduring actually uh many years ago now I think and I think Andrew is going to I think and I think Andrew is going to be speaking right after me. Uh but he be speaking right after me.

Uh but he said at the time AI is the new said at the time AI is the new electricity and I do think that it um kind of captures something very interesting in that LLMs certainly feel like they have properties of utilities right now. So right now.

So um LLM labs like OpenAI, Gemini, Enthropic etc. They spend capex to train the LLMs and this is kind of equivalent the LLMs and this is kind of equivalent to building out a grid and then there's opex to serve that intelligence over APIs to all of us and this is done through metered access where we pay per million tokens or something like that million tokens or something like that and we have a lot of demands that are very utility- like demands out of this API we demand low latency high uptime API we demand low latency high uptime consistent quality etc.

In electricity, consistent quality etc. In electricity, you would have a transfer switch.

So you can transfer your electricity source from like grid and solar or battery or from like grid and solar or battery or generator. In LLM, we have maybe open router and easily switch between the different types of LLMs that exist.

different types of LLMs that exist. Because the LLM are software, they don't Because the LLM are software, they don't compete for physical space.

So it's okay compete for physical space. So it's okay to have basically like six electricity to have basically like six electricity providers and you can switch between providers and you can switch between them, right?

Because they don't compete them, right? Because they don't compete in such a direct way.

And I think what's also a little fascinating and we saw this in the last few days actually a lot of the LLMs went down and people were kind of like stuck and unable to work. And uh I think it's kind of fascinating to me that when the state-of-the-art LLMs go down, it's actually kind of like an intelligence brownout in the world.

It's kind of like when the voltage is unreliable in the grid and uh the planet unreliable in the grid and uh the planet just gets dumber the more reliance we just gets dumber the more reliance we have on these models, which already is have on these models, which already is like really dramatic and I think will like really dramatic and I think will continue to grow.

But LLM's don't only have properties of utilities. I think it's also fair to say that they have some properties of fabs.

And the reason for this is that the capex required for for this is that the capex required for building LLM is actually quite large. Uh building LLM is actually quite large.

Uh it's not just like building some uh it's not just like building some uh power station or something like that, power station or something like that, right? You're investing a huge amount of right?

You're investing a huge amount of money and I think the tech tree and uh for the technology is growing quite rapidly. So we're in a world where we rapidly.

So we're in a world where we have sort of deep tech trees, research have sort of deep tech trees, research and development secrets that are and development secrets that are centralizing inside the LLM labs. Um and but I think the analogy muddies a little bit also because as I mentioned this is software and software is a bit less defensible because it is so malleable.

And so um I think it's just an interesting kind of thing to think about potentially. There's many analogy analogies you can make like a 4 nanometer process node maybe is something like a cluster with certain something like a cluster with certain max flops.

You can think about when max flops. You can think about when you're use when you're using Nvidia GPUs you're use when you're using Nvidia GPUs and you're only doing the software and you're not doing the hardware.

That's kind of like the fabless model. But if you're actually also building your own hardware and you're training on TPUs if hardware and you're training on TPUs if you're Google, that's kind of like the you're Google, that's kind of like the Intel model where you own your fab.

So I Intel model where you own your fab. So I think there's some analogies here that think there's some analogies here that make sense.

But actually I think the analogy that makes the most sense perhaps is that in my mind LLM have very strong kind of analogies to operating systems. Uh in that this is not just electricity or water.

It's not something that comes out of the tap as a that comes out of the tap as a commodity. uh this is these are now increasingly complex software ecosystems right so uh they're not just like simple commodities like electricity and it's kind of interesting to me that the kind of interesting to me that the ecosystem is shaping in a very similar kind of way where you have a few closed source providers like Windows or Mac OS and then you have an open source alternative like Linux and I think for u neural for LLMs as well we have a kind of a few competing closed source of a few competing closed source providers and then maybe the llama ecosystem is currently like maybe a close approximation to something that close approximation to something that may grow into something like Linux.

may grow into something like Linux. Again, I think it's still very early Again, I think it's still very early because these are just simple LLMs, but because these are just simple LLMs, but we're starting to see that these are we're starting to see that these are going to get a lot more complicated.

going to get a lot more complicated. It's not just about the LLM itself.

It's about all the tool use and the multiodalities and how all of that multiodalities and how all of that works. And so when I sort of had this realization a while back, I tried to sketch it out and it kind of seemed to me like LLMs are kind of like a new operating system, right?

So the LLM is a new kind of a computer. It's sitting it's kind of like the CPU equivalent.

uh the context windows are kind of like the memory and then the LLM is orchestrating memory and compute uh for problem solving um using all of these uh capabilities here and so definitely if you look at it looks very much like operating system from that perspective. Um, a few more analogies.

For example, Um, a few more analogies. For example, if you want to download an app, say I go to VS Code and I go to download, you can download VS Code and you can run it on Windows, Linux or or Mac in the same way as you can take an LLM app like cursor and you can run it on GPT or cloud or Gemini series, right?

It's just a drop Gemini series, right? It's just a drop down.

So, it's kind of like similar in that way as well. uh more analogies that I think strike me is that we're kind of like in this 1960sish 1960sish era where LLM compute is still very expensive for this new kind of a computer and that forces the LLMs to be centralized in the cloud and we're all just uh sort of thing clients that interact with it over the network and none of us have full utilization of these computers and therefore it makes sense to use time sharing where we're sense to use time sharing where we're all just you know a dimension of the batch when they're running the computer in the cloud.

And this is very much what computers used to look like at during this time. The operating systems were in the cloud.

Everything was streamed around and there was batching. And so the p the personal computing revolution hasn't happened yet because it's just hasn't happened yet because it's just not economical.

It doesn't make sense. But I think some people are trying.

And it turns out that Mac minis, for example, are a very good fit for some of example, are a very good fit for some of the LLMs because it's all if you're the LLMs because it's all if you're doing batch one inference, this is all doing batch one inference, this is all super memory bound. So this actually works.

And uh I think these are some early indications maybe of personal computing. Uh but this hasn't really happened yet.

Uh but this hasn't really happened yet. It's not clear what this looks like.

It's not clear what this looks like. Maybe some of you get to invent what what this is or how it works or uh what this should what this should be.

Maybe this should what this should be. Maybe one more analogy that I'll mention is one more analogy that I'll mention is whenever I talk to Chach or some LLM whenever I talk to Chach or some LLM directly in text, I feel like I'm talking to an operating system through the terminal.

Like it's just it's it's text. It's direct access to the operating system.

And I think a guey operating system. And I think a guey hasn't yet really been invented in like a general way like should chatt have a guey like different than just a tech guey like different than just a tech bubbles.

Uh certainly some of the apps bubbles. Uh certainly some of the apps that we're going to go into in a bit that we're going to go into in a bit have guey but there's no like guey have guey but there's no like guey across all the tasks if that makes across all the tasks if that makes sense.

Um there are some ways in which LLMs are different from kind of operating systems in some fairly unique operating systems in some fairly unique way and from early computing. And I way and from early computing.

And I wrote about uh this one particular wrote about uh this one particular property that strikes me as very different uh this time around. It's that LLMs like flip they flip the direction of technology diffusion uh that is usually uh present in technology.

So for example with electricity, cryptography, computing, flight, internet, GPS, lots computing, flight, internet, GPS, lots of new transformative technologies that of new transformative technologies that have not been around. Typically it is the government and corporations that are the first users because it's new and expensive etc.

and it only later diffuses to consumer. Uh, but I feel diffuses to consumer.

Uh, but I feel like LLMs are kind of like flipped like LLMs are kind of like flipped around. So maybe with early computers, around.

So maybe with early computers, it was all about ballistics and military use, but with LLMs, it's all about how do you boil an egg or something like do you boil an egg or something like that. This is certainly like a lot of my that.

This is certainly like a lot of my use. And so it's really fascinating to use.

And so it's really fascinating to me that we have a new magical computer and it's like helping me boil an egg. It's not helping the government do something really crazy like some military ballistics or some special military ballistics or some special technology.

Indeed, corporations are technology. Indeed, corporations are governments are lagging behind the adoption of all of us, of all of these technologies.

So, it's just backwards technologies. So, it's just backwards and I think it informs maybe some of the uses of how we want to use this technology or like where are some of the first apps and so on.

So, in summary so far, LLM labs LLMs. I think it's accurate language to use, but LLMs are complicated operating systems.

LLMs are complicated operating systems. They're circa 1960s in computing and They're circa 1960s in computing and we're redoing computing all over again.

and they're currently available via time sharing and distributed like a utility. sharing and distributed like a utility.

What is new and unprecedented is that they're not in the hands of a few governments and corporations. They're in the hands of all of us because we all have a computer and it's all just have a computer and it's all just software and Chaship was beamed down to software and Chaship was beamed down to our computers like billions of people like instantly and overnight and this is insane.

Uh and it's kind of insane to me that this is the case and now it is our time to enter the industry and program these computers. This is crazy.

So I think this is quite remarkable. Before think this is quite remarkable.

Before we program LLMs, we have to kind of like spend some time to think about what these things are. And I especially like to kind of talk about their psychology.

So the way I like to think about LLMs is that they're kind of like people spirits. Um they are stoastic spirits.

Um they are stoastic simulations of people. Um and the simulations of people.

Um and the simulator in this case happens to be an auto reggressive transformer. So transformer is a neural net.

Uh it's and it just kind of like is goes on the level of tokens. It goes chunk chunk level of tokens.

It goes chunk chunk chunk chunk chunk. And there's an almost equal amount of compute for every single chunk.

Um and um this simulator of chunk. Um and um this simulator of course is is just is basically there's course is is just is basically there's some weights involved and we fit it to all of text that we have on the internet and so on.

And you end up with this kind of a simulator and because it is trained on humans, it's got this emergent on humans, it's got this emergent psychology that is humanlike. So the psychology that is humanlike.

So the first thing you'll notice is of course first thing you'll notice is of course uh LLM have encyclopedic knowledge and uh LLM have encyclopedic knowledge and memory. uh and they can remember lots of things, a lot more than any single individual human can because they read individual human can because they read so many things.

It's it actually kind of so many things. It's it actually kind of reminds me of this movie Rainman, which I actually really recommend people watch.

Um and Dustin Hoffman here is an autistic savant who has almost is an autistic savant who has almost perfect memory. So, he can read a he can perfect memory.

So, he can read a he can read like a phone book and remember all of the names and phone numbers. And I kind of feel like LM are kind of like kind of feel like LM are kind of like very similar.

They can remember Shaw very similar. They can remember Shaw hashes and lots of different kinds of things very very easily.

So they certainly have superpowers in some set in some respects. But they also have a bunch of I would say cognitive deficits.

bunch of I would say cognitive deficits. So they hallucinate quite a bit.

Um and they kind of make up stuff and don't have a very good uh sort of internal model of self-nowledge, not sufficient at least. And this has gotten better but not perfect.

They display jagged intelligence. So they're going to be intelligence.

So they're going to be superhuman in some problems solving domains. And then they're going to make mistakes that basically no human will mistakes that basically no human will make.

like you know they will insist that 9.11 is greater than 9.9 or that there are two Rs in strawberry these are there are two Rs in strawberry these are some famous examples but basically there some famous examples but basically there are rough edges that you can trip on so are rough edges that you can trip on so that's kind of I think also kind of that's kind of I think also kind of unique um they also kind of suffer from entrograde amnesia um so uh and I think I'm alluding to the fact that if you I'm alluding to the fact that if you have a co-orker who joins your have a co-orker who joins your organization this co-orker will over organization this co-orker will over time learn your organization and uh they will understand and gain like a huge amount of context on the organization and they go home and they sleep and they consolidate knowledge and they develop expertise over time.

LLMs don't natively do this and this is not something that do this and this is not something that has really been solved in the R&amp;D of has really been solved in the R&amp;D of LLM. I think um and so context windows are really kind of like working memory and you have to sort of program the working memory quite directly because they don't just kind of like get smarter by uh by default and I think a lot of people get tripped up by the analogies uh in this way.

Uh in popular culture I recommend people watch these two movies uh Momento and 51st dates. In both of these movies, the protagonists, their these movies, the protagonists, their weights are fixed and their context weights are fixed and their context windows gets wiped every single morning windows gets wiped every single morning and it's really problematic to go to and it's really problematic to go to work or have relationships when this happens and this happens to all the time.

I guess one more thing I would point to is security kind of related limitations of the use of LLM. So for limitations of the use of LLM.

So for example, LLMs are quite gullible. Uh example, LLMs are quite gullible.

Uh they are susceptible to prompt injection they are susceptible to prompt injection risks. They might leak your data etc.

And so um and there's many other And so um and there's many other considerations uh security related. So, considerations uh security related.

So, so basically long story short, you have to load your you have to load your you have to simultaneously think through this superhuman thing that has a bunch of cognitive deficits and issues.

How do of cognitive deficits and issues. How do we and yet they are extremely like useful and so how do we program them and how do we work around their deficits and enjoy their superhuman powers.

So what I want to switch to now is talk about the opportunities of how do we use these models and what are some of the these models and what are some of the biggest opportunities. This is not a comprehensive list just some of the things that I thought were interesting things that I thought were interesting for this talk.

The first thing I'm kind of excited about is what I would call partial autonomy apps. So for example, partial autonomy apps.

So for example, let's work with the example of coding. let's work with the example of coding.

You can certainly go to chacht directly You can certainly go to chacht directly and you can start copy pasting code around and copyping bug reports and stuff around and getting code and copy pasting everything around. Why would you why would you do that?

Why would you go directly to the operating system? It makes a lot more sense to have an app dedicated for this.

And so I think many of you uh use uh cursor. I do as well.

And uh cursor is kind of like the thing you want instead. You don't want to just directly go to the chash apt.

And I think cursor is a very good example of think cursor is a very good example of an early LLM app that has a bunch of properties that I think are um useful across all the LLM apps. So in across all the LLM apps.

So in particular, you will notice that we have a traditional interface that allows a human to go in and do all the work manually just as before. But in addition to that, we now have this LLM integration that allows us to go in bigger chunks.

And so some of the bigger chunks. And so some of the properties of LLM apps that I think are shared and useful to point out.

Number one, the LLMs basically do a ton of the context management. Um, number two, they orchestrate multiple calls to LLMs, orchestrate multiple calls to LLMs, right?

So in the case of cursor, there's under the hood embedding models for all your files, the actual chat models, your files, the actual chat models, models that apply diffs to the code, and this is all orchestrated for you. A really big one that uh I think also maybe not fully appreciated always is application specific uh GUI and the application specific uh GUI and the importance of it.

Um because you don't just want to talk to the operating system directly in text. Text is very hard to read, interpret, understand and also like you don't want to take some of these actions natively in text.

So it's much better to just see a diff as like much better to just see a diff as like red and green change and you can see red and green change and you can see what's being added is subtracted. It's what's being added is subtracted.

It's much easier to just do command Y to much easier to just do command Y to accept or command N to reject. I accept or command N to reject.

I shouldn't have to type it in text, shouldn't have to type it in text, right? So, a guey allows a human to right?

So, a guey allows a human to audit the work of these fallible systems audit the work of these fallible systems and to go faster. I'm going to come back and to go faster.

I'm going to come back to this point a little bit uh later as well. And the last kind of feature I want to point out is that there's what I call the autonomy slider.

So, for example, in cursor, you can just do tap completion. You're mostly in charge.

You can select a chunk of code and command K to change just that chunk of code. You can do command L to change the entire file.

Or you can do command I which just you know let it rip do whatever you want you know let it rip do whatever you want in the entire repo and that's the sort in the entire repo and that's the sort of full autonomy agent agentic version and so you are in charge of the autonomy slider and depending on the complexity of the task at hand you can uh tune the amount of autonomy that you're willing to give up uh for that task maybe to show one more example of a fairly show one more example of a fairly successful LLM app uh perplexity um it successful LLM app uh perplexity um it also has very similar features to what I've just pointed out to in cursor uh it packages up a lot of the information.

It orchestrates multiple LLMs. It's got a GUI that allows you to audit some of its GUI that allows you to audit some of its work.

So, for example, it will site sources and you can imagine inspecting them. And it's got an autonomy slider.

You can either just do a quick search or you can do research or you can do deep you can do research or you can do deep research and come back 10 minutes later. research and come back 10 minutes later.

So, this is all just varying levels of So, this is all just varying levels of autonomy that you give up to the tool. So, I guess my question is I feel like a lot of software will become partially lot of software will become partially autonomous.

I'm trying to think through autonomous. I'm trying to think through like what does that look like?

And for like what does that look like? And for many of you who maintain products and many of you who maintain products and services, how are you going to make your products and services partially autonomous?

Can an LLM see everything autonomous? Can an LLM see everything that a human can see?

Can an LLM act in all the ways that a human could act? And can humans supervise and stay in the can humans supervise and stay in the loop of this activity?

Because again, loop of this activity? Because again, these are fallible systems that aren't these are fallible systems that aren't yet perfect.

And what does a diff look like in Photoshop or something like that? You know, and also a lot of the traditional software right now, it has all these switches and all this kind of all these switches and all this kind of stuff that's all designed for human.

All of this has to change and become accessible to LLMs. accessible to LLMs.

So, one thing I want to stress with a lot of these LLM apps that I'm not sure gets as much attention as it should is gets as much attention as it should is um we we're now kind of like cooperating um we we're now kind of like cooperating with AIS and usually they are doing the generation and we as humans are doing the verification.

It is in our interest the verification. It is in our interest to make this loop go as fast as to make this loop go as fast as possible.

So, we're getting a lot of possible. So, we're getting a lot of work done.

There are two major ways that work done. There are two major ways that I think uh this can be done.

Number one, I think uh this can be done. Number one, you can speed up verification a lot.

Um, and I think guies, for example, are extremely important to this because a extremely important to this because a guey utilizes your computer vision GPU guey utilizes your computer vision GPU in all of our head. Reading text is in all of our head.

Reading text is effortful and it's not fun, but looking at stuff is fun and it's it's just a kind of like a highway to your brain. kind of like a highway to your brain.

So, I think guies are very useful for auditing systems and visual representations in general. And number two, I would say is we have to keep the AI on the leash.

We I think a lot of AI on the leash. We I think a lot of people are getting way over excited with people are getting way over excited with AI agents and uh it's not useful to me AI agents and uh it's not useful to me to get a diff of 10,000 lines of code to to get a diff of 10,000 lines of code to my repo.

Like I have to I'm still the bottleneck, right? Even though that 10,00 lines come out instantly, I have to make sure that this thing is not introducing bugs.

It's just like and that it's doing the correct thing, right? And that there's no security right?

And that there's no security issues and so on. So um I think that um yeah basically you we have to sort of like it's in our interest to make the like it's in our interest to make the the flow of these two go very very fast the flow of these two go very very fast and we have to somehow keep the AI on and we have to somehow keep the AI on the leash because it gets way too the leash because it gets way too overreactive.

It's uh it's kind of like overreactive. It's uh it's kind of like this.

This is how I feel when I do AI this. This is how I feel when I do AI assisted coding.

If I'm just bite coding everything is nice and great but if I'm actually trying to get work done it's actually trying to get work done it's not so great to have an overreactive uh not so great to have an overreactive uh agent doing all this kind of stuff. So agent doing all this kind of stuff.

So this slide is not very good. I'm sorry, this slide is not very good.

I'm sorry, but I guess I'm trying to develop like but I guess I'm trying to develop like many of you some ways of utilizing these many of you some ways of utilizing these agents in my coding workflow and to do AI assisted coding. And in my own work, I'm always scared to get way too big diffs.

I always go in small incremental chunks. I want to make sure that chunks.

I want to make sure that everything is good. I want to spin this loop very very fast and um I sort of work on small chunks of single concrete thing.

Uh and so I think many of you probably are developing similar ways of probably are developing similar ways of working with the with LLMs. working with the with LLMs.

Um, I also saw a number of blog posts that try to develop these best practices for working with LLMs. And here's one that I read recently and I thought was quite good.

And it kind of discussed quite good. And it kind of discussed some techniques and some of them have to some techniques and some of them have to do with how you keep the AI on the do with how you keep the AI on the leash.

And so, as an example, if you are leash. And so, as an example, if you are prompting, if your prompt is vague, then prompting, if your prompt is vague, then uh the AI might not do exactly what you uh the AI might not do exactly what you wanted and in that case, verification wanted and in that case, verification will fail.

You're going to ask for something else. If a verification fails, then you're going to start spinning.

So it makes a lot more sense to spend a bit more time to be more concrete in your more time to be more concrete in your prompts which increases the probability prompts which increases the probability of successful verification and you can of successful verification and you can move forward. And so I think a lot of us are going to end up finding um kind of techniques like this.

I think in my own techniques like this. I think in my own work as well I'm currently interested in uh what education looks like in um together with kind of like now that we have AI uh and LLMs what does education look like?

And I think a a large amount look like? And I think a a large amount of thought for me goes into how we keep AI on the leash.

I don't think it just works to go to chat and be like, "Hey, teach me physics." I don't think this works because the AI is like gets lost works because the AI is like gets lost in the woods. And so for me, this is actually two separate apps.

For example, there's an app for a teacher that creates courses and then there's an app that takes courses and serves them to that takes courses and serves them to students. And in both cases, we now have students.

And in both cases, we now have this intermediate artifact of a course this intermediate artifact of a course that is auditable and we can make sure it's good. We can make sure it's consistent.

and the AI is kept on the consistent. and the AI is kept on the leash with respect to a certain leash with respect to a certain syllabus, a certain like um progression syllabus, a certain like um progression of projects and so on.

And so this is of projects and so on. And so this is one way of keeping the AI on leash and I think has a much higher likelihood of working and the AI is not getting lost in the woods.

One more kind of analogy I wanted to sort of allude to is I'm not I'm no stranger to partial autonomy and I kind stranger to partial autonomy and I kind of worked on this I think for five years at Tesla and this is also a partial autonomy product and shares a lot of the autonomy product and shares a lot of the features like for example right there in the instrument panel is the GUI of the autopilot so it's showing me what the autopilot so it's showing me what the what the neural network sees and so on and we have the autonomy slider where over the course of my tenure there we did more and more autonomous tasks for the user and maybe the story that I the user and maybe the story that I wanted to tell very briefly is uh actually the first time I drove a self-driving vehicle was in 2013 and I had a friend who worked at Whimo and uh he offered to give me a drive around he offered to give me a drive around Palo Alto.

I took this picture using Palo Alto. I took this picture using Google Glass at the time and many of you Google Glass at the time and many of you are so young that you might not even are so young that you might not even know what that is.

Uh but uh yeah, this know what that is. Uh but uh yeah, this was like all the rage at the time.

And was like all the rage at the time. And we got into this car and we went for we got into this car and we went for about a 30-minute drive around Palo Alto highways uh streets and so on.

And this drive was perfect. There was zero interventions and this was 2013 which is now 12 years ago.

And it kind of struck me because at the time when I had this perfect drive, this perfect demo, I felt perfect drive, this perfect demo, I felt like, wow, self-driving is imminent because this just worked. This is incredible.

Um, but here we are 12 years later and we are still working on autonomy. Um, we are still working on driving agents and even now we haven't actually like really solved the problem.

actually like really solved the problem. like you may see Whimos going around and they look driverless but you know there's still a lot of teleoperation and a lot of human in the loop of a lot of this driving so we still haven't even this driving so we still haven't even like declared success but I think it's definitely like going to succeed at this point but it just took a long time and so I think like like this is software is really tricky I think in the same way that driving is tricky and so when I see things like oh 2025 is the year of agents I get very concerned and I kind of feel like you know this is the decade of agents and this is going to be quite some time.

We need humans in the loop. We need to do this carefully.

One more kind of analogy that I always think more kind of analogy that I always think through is the Iron Man suit. Uh I think this is I always love Iron Man.

I think it's like so um correct in a bunch of it's like so um correct in a bunch of ways with respect to technology and how ways with respect to technology and how it will play out. And what I love about it will play out.

And what I love about the Iron Man suit is that it's both an augmentation and Tony Stark can drive it and it's also an agent. And in some of and it's also an agent.

And in some of the movies, the Iron Man suit is quite autonomous and can fly around and find Tony and all this kind of stuff. And so this is the autonomy slider is we can be we can build augmentations or we can we can build augmentations or we can build agents and we kind of want to do a bit of both.

But at this stage I would say working with fallible LLMs and so say working with fallible LLMs and so on. I would say you know it's less Iron Man robots and more Iron Man suits that you want to build.

It's less like you want to build. It's less like building flashy demos of autonomous building flashy demos of autonomous agents and more building partial agents and more building partial autonomy products.

And these products autonomy products. And these products have custom gueies and UIUX.

And we're have custom gueies and UIUX. And we're trying to um and this is done so that the generation verification loop of the human is very very fast.

But we are not losing the sight of the fact that it is in principle possible to automate this in principle possible to automate this work. And there should be an autonomy slider in your product.

And you should be thinking about how you can slide that autonomy slider and make your product uh sort of um more autonomous over time. sort of um more autonomous over time.

But this is kind of how I think there's lots of opportunities in these kinds of products. I want to now switch gears a products.

I want to now switch gears a little bit and talk about one other little bit and talk about one other dimension that I think is very unique. dimension that I think is very unique.

Not only is there a new type of programming language that allows for autonomy in software but also as I mentioned it's programmed in English which is this natural interface and which is this natural interface and suddenly everyone is a programmer because everyone speaks natural language like English.

So this is extremely like English. So this is extremely bullish and very interesting to me and bullish and very interesting to me and also completely unprecedented.

I would also completely unprecedented. I would say it it used to be the case that you need to spend five to 10 years studying something to be able to do something in something to be able to do something in software.

this is not the case anymore. So, I don't know if by any chance anyone has heard of vibe coding.

Uh, this this is the tweet that kind of like introduced this, but I'm told that this is now like a major meme. Um, fun story about this is that I've been on Twitter for like 15 years or something Twitter for like 15 years or something like that at this point and I still have like that at this point and I still have no clue which tweet will become viral cares.

And I thought that this tweet was going to be the latter. I don't know.

It was just like a shower of thoughts. But this became like a total meme and I really just can't tell.

But I guess like it struck a chord and it gave a name to something that everyone was feeling but couldn't quite say in words. So now couldn't quite say in words.

So now there's a Wikipedia page and everything. This is like [Applause] now or something like that.

So, um, so Tom Wolf from HuggingFace shared um, so Tom Wolf from HuggingFace shared this beautiful video that I really love. Um, these are kids vibe coding.

And I find that this is such a wholesome video. Like, I love this video.

Like, how can you look at this video and feel bad about the future? The future is great.

great. I think this will end up being like a gateway drug to software development.

Um, I'm not a doomer about the future of the generation and I think yeah, I love this video. So, I tried by coding a this video.

So, I tried by coding a little bit uh as well because it's so little bit uh as well because it's so fun. Uh, so bike coding is so great when fun.

Uh, so bike coding is so great when you want to build something super duper you want to build something super duper custom that doesn't appear to exist and you just want to wing it because it's a Saturday or something like that. So, I Saturday or something like that.

So, I built this uh iOS app and I don't I built this uh iOS app and I don't I can't actually program in Swift, but I can't actually program in Swift, but I was really shocked that I was able to was really shocked that I was able to build like a super basic app and I'm not going to explain it. It's really uh dumb, but uh I kind of like this was just like a day of work and this was running on my phone like later that day and I was like, "Wow, this is amazing." I didn't have to like read through Swift for like five days or something like that to like get started.

I also that to like get started. I also vipcoded this app called Menu Genen.

And vipcoded this app called Menu Genen. And this is live.

You can try it in menu.app. And I basically had this problem where I show up at a restaurant, I read through the menu, and I have no idea what any of the things are.

So I was like, "Hey, I'm going to bite code it." So, um, this is what it looks like. You go to menu.app, You go to menu.app, um, and, uh, you take a picture of a of a menu and then menu generates the images and everyone gets $5 in credits images and everyone gets $5 in credits for free when you sign up.

And for free when you sign up. And therefore, this is a major cost center therefore, this is a major cost center in my life.

So, this is a negative negative uh, revenue app for me right now. now.

But the fascinating thing about menu genen for me is that the code of the v the vite coding part the code was actually the easy part of v of v coding menu and most of it actually was when I tried to make it real so that you can actually have authentication and actually have authentication and payments and the domain name and averal deployment.

This was really hard and all of this was not code. All of this devops stuff was in me in the browser clicking stuff and this was extreme slo and took stuff and this was extreme slo and took another week.

So it was really another week. So it was really fascinating that I had the menu genen um fascinating that I had the menu genen um basically demo working on my laptop in a basically demo working on my laptop in a few hours and then it took me a week few hours and then it took me a week because I was trying to make it real and because I was trying to make it real and the reason for this is this was just the reason for this is this was just really annoying.

Um, so for example, if really annoying. Um, so for example, if you try to add Google login to your web you try to add Google login to your web page, I know this is very small, but page, I know this is very small, but just a huge amount of instructions of just a huge amount of instructions of this clerk library telling me how to this clerk library telling me how to integrate this.

And this is crazy. Like it's telling me go to this URL, click on this dropdown, choose this, go to this, and click on that.

And it's like telling me what to do. Like a computer is telling me the actions I should be taking.

What the hell? I had to follow all these instructions.

This was crazy. So I think the last part This was crazy.

So I think the last part of my talk therefore focuses on can we of my talk therefore focuses on can we just build for agents? I don't want to just build for agents?

So roughly speaking, I think there's a new category of consumer and manipulator of digital information. It manipulator of digital information.

It used to be just humans through GUIs or computers through APIs. And now we have a completely new thing and agents are they're computers but they are humanlike kind of right they're people spirits kind of right they're people spirits there's people spirits on the internet there's people spirits on the internet and they need to interact with our and they need to interact with our software infrastructure like can we software infrastructure like can we build for them it's a new thing so as an example you can have robots.txt on your domain and you can instruct uh or like advise I suppose um uh web crawlers on how to behave on your website in the how to behave on your website in the same way you can have maybe lm.txt txt same way you can have maybe lm.txt txt file which is just a simple markdown file which is just a simple markdown that's telling LLMs what this domain is about and this is very readable to a to an LLM.

If it had to instead get the HTML of your web page and try to parse it, this is very errorprone and it, this is very errorprone and difficult and will screw it up and it's difficult and will screw it up and it's not going to work. So we can just directly speak to the LLM.

It's worth it. Um a huge amount of documentation is it.

Um a huge amount of documentation is currently written for people. So you currently written for people.

So you will see things like lists and bold and will see things like lists and bold and pictures and this is not directly pictures and this is not directly accessible by an LLM. So I see some of accessible by an LLM.

So I see some of the services now are transitioning a lot the services now are transitioning a lot of the their docs to be specifically for of the their docs to be specifically for LLMs. So Versell and Stripe as an LLMs.

So Versell and Stripe as an example are early movers here but there example are early movers here but there are a few more that I've seen already are a few more that I've seen already and they offer their documentation in and they offer their documentation in markdown. Markdown is super easy for LMS markdown.

Markdown is super easy for LMS to understand. This is great.

Um maybe one simple example from from uh my one simple example from from uh my experience as well. Maybe some of you know three blue one brown.

He makes beautiful animation videos on YouTube. Yeah, I love this library.

So that he wrote uh Manon and I wanted to make my own and uh there's extensive documentations on how to use manon and so I didn't want to actually read through it. So I copy pasted the whole thing to an LLM and I described what I wanted and it just worked out of the box like LLM just bcoded me an animation exactly what I wanted and I was like wow exactly what I wanted and I was like wow this is amazing.

So if we can make docs this is amazing. So if we can make docs legible to LLMs, it's going to unlock a legible to LLMs, it's going to unlock a huge amount of um kind of use and um I think this is wonderful and should should happen more.

The other thing I wanted to point out is that you do unfortunately have to it's not just unfortunately have to it's not just about taking your docs and making them about taking your docs and making them appear in markdown. That's the easy appear in markdown.

That's the easy part. We actually have to change the part.

We actually have to change the docs because anytime your docs say click docs because anytime your docs say click this is bad. An LLM will not be able to natively take this action right now.

So, Verscell, for example, is replacing Verscell, for example, is replacing every occurrence of click with an every occurrence of click with an equivalent curl command that your LM equivalent curl command that your LM agent could take on your behalf. Um, and so I think this is very interesting.

And then, of course, there's a model context protocol from Enthropic. And this is also another way, it's a protocol of speaking directly to agents as this new consumer and manipulator of digital consumer and manipulator of digital information.

So, I'm very bullish on information. So, I'm very bullish on these ideas.

The other thing I really these ideas. The other thing I really like is a number of little tools here like is a number of little tools here and there that are helping ingest data that in like very LLM friendly formats.

So for example, when I go to a GitHub repo like my nanoGPT repo, I can't feed this to an LLM and ask questions about this to an LLM and ask questions about it uh because it's you know this is a it uh because it's you know this is a human interface on GitHub. So when you human interface on GitHub.

So when you just change the URL from GitHub to get just change the URL from GitHub to get ingest then uh this will actually ingest then uh this will actually concatenate all the files into a single giant text and it will create a directory structure etc. And this is directory structure etc.

And this is ready to be copy pasted into your favorite LLM and you can do stuff. Maybe even more dramatic example of this is even more dramatic example of this is deep wiki where it's not just the raw content of these files.

uh this is from Devon but also like they have Devon Devon but also like they have Devon basically do analysis of the GitHub repo and Devon basically builds up a whole docs uh pages just for your repo and you docs uh pages just for your repo and you can imagine that this is even more can imagine that this is even more helpful to copy paste into your LLM.

So helpful to copy paste into your LLM. So I love all the little tools that I love all the little tools that basically where you just change the URL basically where you just change the URL and it makes something accessible to an and it makes something accessible to an LLM.

So this is all well and great and u LLM. So this is all well and great and u I think there should be a lot more of it.

One more note I wanted to make is that it is absolutely possible that in that it is absolutely possible that in the future LLMs will be able to this is not even future this is today they'll be able to go around and they'll be able to able to go around and they'll be able to click stuff and so on but I still think click stuff and so on but I still think it's very worth u basically meeting LLM halfway LLM's halfway and making it easier for them to access all this easier for them to access all this information uh because this is still information uh because this is still fairly expensive I would say to use and uh a lot more difficult and so I do think that lots of software there will think that lots of software there will be a long tail where it won't like adapt be a long tail where it won't like adapt apps because these are not like live apps because these are not like live player sort of repositories or digital player sort of repositories or digital infrastructure and we will need these infrastructure and we will need these tools.

Uh but I think for everyone else tools. Uh but I think for everyone else I think it's very worth kind of like I think it's very worth kind of like meeting in some middle point.

So I'm meeting in some middle point. So I'm bullish on both if that makes sense.

So in summary, what an amazing time to get into the industry. We need to get into the industry.

We need to rewrite a ton of code. A ton of code rewrite a ton of code.

A ton of code will be written by professionals and by will be written by professionals and by coders. These LLMs are kind of like utilities, kind of like fabs, but they're kind of especially like operating systems.

But it's so early. It's like 1960s of operating systems and uh and I think a lot of the analogies cross over.

Um and these LMS are kind of like these fallible uh you know people spirits that we have to learn to work spirits that we have to learn to work with. And in order to do that properly, we need to adjust our infrastructure towards it.

So when you're building towards it. So when you're building these LLM apps, I describe some of the ways of working effectively with these LLMs and some of the tools that make that uh kind of possible and how you can spin this loop very very quickly and spin this loop very very quickly and basically create partial tunneling basically create partial tunneling products and then um yeah, a lot of code has to also be written for the agents more directly.

But in any case, going more directly. But in any case, going back to the Iron Man suit analogy, I back to the Iron Man suit analogy, I think what we'll see over the next think what we'll see over the next decade roughly is we're going to take decade roughly is we're going to take the slider from left to right.

And I'm very interesting. It's going to be very interesting to see what that looks like.

interesting to see what that looks like. And I can't wait to build it with all of

## Timestamped Transcript

[00:01] Please welcome former director of AI
[00:03] Please welcome former director of AI
[00:04] Please welcome former director of AI Tesla Andre Carpathy.
[00:07] Tesla Andre Carpathy.
[00:07] Tesla Andre Carpathy. [Music]
[00:11] [Music]
[00:11] [Music] Hello.
[00:14] [Music]
[00:19] Wow, a lot of people here. Hello.
[00:22] Wow, a lot of people here. Hello.
[00:22] Wow, a lot of people here. Hello. Um, okay. Yeah. So I'm excited to be
[00:24] Um, okay. Yeah. So I'm excited to be
[00:24] Um, okay. Yeah. So I'm excited to be here today to talk to you about software
[00:27] here today to talk to you about software
[00:27] here today to talk to you about software in the era of AI. And I'm told that many
[00:30] in the era of AI. And I'm told that many
[00:30] in the era of AI. And I'm told that many of you are students like bachelors,
[00:32] of you are students like bachelors,
[00:32] of you are students like bachelors, masters, PhD and so on. And you're about
[00:34] masters, PhD and so on. And you're about
[00:34] masters, PhD and so on. And you're about to enter the industry. And I think it's
[00:36] to enter the industry. And I think it's
[00:36] to enter the industry. And I think it's actually like an extremely unique and
[00:37] actually like an extremely unique and
[00:37] actually like an extremely unique and very interesting time to enter the
[00:38] very interesting time to enter the
[00:38] very interesting time to enter the industry right now. And I think
[00:41] industry right now. And I think
[00:41] industry right now. And I think fundamentally the reason for that is
[00:43] fundamentally the reason for that is
[00:43] fundamentally the reason for that is that um software is changing uh again.
[00:47] that um software is changing uh again.
[00:47] that um software is changing uh again. And I say again because I actually gave
[00:49] And I say again because I actually gave
[00:49] And I say again because I actually gave this talk already. Um but the problem is
[00:52] this talk already. Um but the problem is
[00:52] this talk already. Um but the problem is that software keeps changing. So I
[00:54] that software keeps changing. So I
[00:54] that software keeps changing. So I actually have a lot of material to
[00:55] actually have a lot of material to
[00:55] actually have a lot of material to create new talks and I think it's
[00:56] create new talks and I think it's
[00:56] create new talks and I think it's changing quite fundamentally. I think
[00:58] changing quite fundamentally. I think
[00:58] changing quite fundamentally. I think roughly speaking software has not
[01:00] roughly speaking software has not
[01:00] roughly speaking software has not changed much on such a fundamental level
[01:01] changed much on such a fundamental level
[01:02] changed much on such a fundamental level for 70 years. And then it's changed I
[01:04] for 70 years. And then it's changed I
[01:04] for 70 years. And then it's changed I think about twice quite rapidly in the
[01:06] think about twice quite rapidly in the
[01:06] think about twice quite rapidly in the last few years. And so there's just a
[01:08] last few years. And so there's just a
[01:08] last few years. And so there's just a huge amount of work to do a huge amount
[01:09] huge amount of work to do a huge amount
[01:09] huge amount of work to do a huge amount of software to write and rewrite. So
[01:12] of software to write and rewrite. So
[01:12] of software to write and rewrite. So let's take a look at maybe the realm of
[01:14] let's take a look at maybe the realm of
[01:14] let's take a look at maybe the realm of software. So if we kind of think of this
[01:16] software. So if we kind of think of this
[01:16] software. So if we kind of think of this as like the map of software this is a
[01:17] as like the map of software this is a
[01:17] as like the map of software this is a really cool tool called map of GitHub.
[01:19] really cool tool called map of GitHub.
[01:20] really cool tool called map of GitHub. Um this is kind of like all the software
[01:21] Um this is kind of like all the software
[01:21] Um this is kind of like all the software that's written. Uh these are
[01:23] that's written. Uh these are
[01:23] that's written. Uh these are instructions to the computer for
[01:24] instructions to the computer for
[01:24] instructions to the computer for carrying out tasks in the digital space.
[01:26] carrying out tasks in the digital space.
[01:26] carrying out tasks in the digital space. So if you zoom in here, these are all
[01:27] So if you zoom in here, these are all
[01:28] So if you zoom in here, these are all different kinds of repositories and this
[01:30] different kinds of repositories and this
[01:30] different kinds of repositories and this is all the code that has been written.
[01:31] is all the code that has been written.
[01:31] is all the code that has been written. And a few years ago I kind of observed
[01:33] And a few years ago I kind of observed
[01:33] And a few years ago I kind of observed that um software was kind of changing
[01:35] that um software was kind of changing
[01:35] that um software was kind of changing and there was kind of like a new type of
[01:37] and there was kind of like a new type of
[01:37] and there was kind of like a new type of software around and I called this
[01:39] software around and I called this
[01:39] software around and I called this software 2.0 at the time and the idea
[01:42] software 2.0 at the time and the idea
[01:42] software 2.0 at the time and the idea here was that software 1.0 is the code
[01:44] here was that software 1.0 is the code
[01:44] here was that software 1.0 is the code you write for the computer. Software 2.0
[01:46] you write for the computer. Software 2.0
[01:46] you write for the computer. Software 2.0 know are basically neural networks and
[01:48] know are basically neural networks and
[01:48] know are basically neural networks and in particular the weights of a neural
[01:50] in particular the weights of a neural
[01:50] in particular the weights of a neural network and you're not writing this code
[01:53] network and you're not writing this code
[01:53] network and you're not writing this code directly you are most you are more kind
[01:55] directly you are most you are more kind
[01:55] directly you are most you are more kind of like tuning the data sets and then
[01:56] of like tuning the data sets and then
[01:56] of like tuning the data sets and then you're running an optimizer to create to
[01:58] you're running an optimizer to create to
[01:58] you're running an optimizer to create to create the parameters of this neural net
[02:00] create the parameters of this neural net
[02:00] create the parameters of this neural net and I think like at the time neural nets
[02:02] and I think like at the time neural nets
[02:02] and I think like at the time neural nets were kind of seen as like just a
[02:03] were kind of seen as like just a
[02:03] were kind of seen as like just a different kind of classifier like a
[02:04] different kind of classifier like a
[02:04] different kind of classifier like a decision tree or something like that and
[02:06] decision tree or something like that and
[02:06] decision tree or something like that and so I think it was kind of like um I
[02:09] so I think it was kind of like um I
[02:09] so I think it was kind of like um I think this framing was a lot more
[02:10] think this framing was a lot more
[02:10] think this framing was a lot more appropriate and now actually what we
[02:12] appropriate and now actually what we
[02:12] appropriate and now actually what we have is kind of like an equivalent of
[02:13] have is kind of like an equivalent of
[02:13] have is kind of like an equivalent of GitHub in the realm of software 2.0 And
[02:15] GitHub in the realm of software 2.0 And
[02:15] GitHub in the realm of software 2.0 And I think the hugging face is basically
[02:18] I think the hugging face is basically
[02:18] I think the hugging face is basically equivalent of GitHub in software 2.0.
[02:20] equivalent of GitHub in software 2.0.
[02:20] equivalent of GitHub in software 2.0. And there's also model atlas and you can
[02:22] And there's also model atlas and you can
[02:22] And there's also model atlas and you can visualize all the code written there. In
[02:24] visualize all the code written there. In
[02:24] visualize all the code written there. In case you're curious, by the way, the
[02:25] case you're curious, by the way, the
[02:25] case you're curious, by the way, the giant circle, the point in the middle,
[02:28] giant circle, the point in the middle,
[02:28] giant circle, the point in the middle, uh these are the parameters of flux, the
[02:30] uh these are the parameters of flux, the
[02:30] uh these are the parameters of flux, the image generator. And so anytime someone
[02:32] image generator. And so anytime someone
[02:32] image generator. And so anytime someone tunes a on top of a flux model, you
[02:34] tunes a on top of a flux model, you
[02:34] tunes a on top of a flux model, you basically create a git commit uh in this
[02:37] basically create a git commit uh in this
[02:37] basically create a git commit uh in this space and uh you create a different kind
[02:39] space and uh you create a different kind
[02:39] space and uh you create a different kind of a image generator. So basically what
[02:41] of a image generator. So basically what
[02:41] of a image generator. So basically what we have is software 1.0 is the computer
[02:43] we have is software 1.0 is the computer
[02:43] we have is software 1.0 is the computer code that programs a computer. Software
[02:45] code that programs a computer. Software
[02:45] code that programs a computer. Software 2.0 are the weights which program neural
[02:48] 2.0 are the weights which program neural
[02:48] 2.0 are the weights which program neural networks. Uh and here's an example of
[02:50] networks. Uh and here's an example of
[02:50] networks. Uh and here's an example of Alexet image recognizer neural network.
[02:53] Alexet image recognizer neural network.
[02:53] Alexet image recognizer neural network. Now so far all of the neural networks
[02:55] Now so far all of the neural networks
[02:55] Now so far all of the neural networks that we've been familiar with until
[02:56] that we've been familiar with until
[02:56] that we've been familiar with until recently where kind of like fixed
[02:58] recently where kind of like fixed
[02:58] recently where kind of like fixed function computers image to categories
[03:01] function computers image to categories
[03:01] function computers image to categories or something like that. And I think
[03:03] or something like that. And I think
[03:03] or something like that. And I think what's changed and I think is a quite
[03:05] what's changed and I think is a quite
[03:05] what's changed and I think is a quite fundamental change is that neural
[03:06] fundamental change is that neural
[03:06] fundamental change is that neural networks became programmable with large
[03:09] networks became programmable with large
[03:09] networks became programmable with large language models. And so I I see this as
[03:12] language models. And so I I see this as
[03:12] language models. And so I I see this as quite new, unique. It's a new kind of a
[03:14] quite new, unique. It's a new kind of a
[03:14] quite new, unique. It's a new kind of a computer and uh so in my mind it's uh
[03:17] computer and uh so in my mind it's uh
[03:18] computer and uh so in my mind it's uh worth giving it a new designation of
[03:19] worth giving it a new designation of
[03:19] worth giving it a new designation of software 3.0. And basically your prompts
[03:22] software 3.0. And basically your prompts
[03:22] software 3.0. And basically your prompts are now programs that program the LLM.
[03:25] are now programs that program the LLM.
[03:25] are now programs that program the LLM. And uh remarkably uh these uh prompts
[03:28] And uh remarkably uh these uh prompts
[03:28] And uh remarkably uh these uh prompts are written in English. So it's kind of
[03:30] are written in English. So it's kind of
[03:30] are written in English. So it's kind of a very interesting programming language.
[03:33] a very interesting programming language.
[03:33] a very interesting programming language. Um so maybe uh to summarize the
[03:36] Um so maybe uh to summarize the
[03:36] Um so maybe uh to summarize the difference if you're doing sentiment
[03:37] difference if you're doing sentiment
[03:37] difference if you're doing sentiment classification for example you can
[03:39] classification for example you can
[03:39] classification for example you can imagine writing some uh amount of Python
[03:42] imagine writing some uh amount of Python
[03:42] imagine writing some uh amount of Python to to basically do sentiment
[03:44] to to basically do sentiment
[03:44] to to basically do sentiment classification or you can train a neural
[03:45] classification or you can train a neural
[03:46] classification or you can train a neural net or you can prompt a large language
[03:47] net or you can prompt a large language
[03:47] net or you can prompt a large language model. Uh so here this is a few short
[03:49] model. Uh so here this is a few short
[03:50] model. Uh so here this is a few short prompt and you can imagine changing it
[03:51] prompt and you can imagine changing it
[03:51] prompt and you can imagine changing it and programming the computer in a
[03:52] and programming the computer in a
[03:52] and programming the computer in a slightly different way. So basically we
[03:54] slightly different way. So basically we
[03:54] slightly different way. So basically we have software 1.0 software 2.0 and I
[03:57] have software 1.0 software 2.0 and I
[03:57] have software 1.0 software 2.0 and I think we're seeing maybe you've seen a
[03:59] think we're seeing maybe you've seen a
[03:59] think we're seeing maybe you've seen a lot of GitHub code is not just like code
[04:01] lot of GitHub code is not just like code
[04:01] lot of GitHub code is not just like code anymore. there's a bunch of like English
[04:03] anymore. there's a bunch of like English
[04:03] anymore. there's a bunch of like English interspersed with code and so I think
[04:05] interspersed with code and so I think
[04:05] interspersed with code and so I think kind of there's a growing category of
[04:07] kind of there's a growing category of
[04:07] kind of there's a growing category of new kind of code. So not only is it a
[04:09] new kind of code. So not only is it a
[04:09] new kind of code. So not only is it a new programming paradigm, it's also
[04:10] new programming paradigm, it's also
[04:10] new programming paradigm, it's also remarkable to me that it's in our native
[04:12] remarkable to me that it's in our native
[04:12] remarkable to me that it's in our native language of English. And so when this
[04:14] language of English. And so when this
[04:14] language of English. And so when this blew my mind a few uh I guess years ago
[04:17] blew my mind a few uh I guess years ago
[04:17] blew my mind a few uh I guess years ago now I tweeted this and um I think it
[04:20] now I tweeted this and um I think it
[04:20] now I tweeted this and um I think it captured the attention of a lot of
[04:21] captured the attention of a lot of
[04:21] captured the attention of a lot of people and this is my currently pinned
[04:23] people and this is my currently pinned
[04:23] people and this is my currently pinned tweet uh is that remarkably we're now
[04:25] tweet uh is that remarkably we're now
[04:25] tweet uh is that remarkably we're now programming computers in English. Now,
[04:28] programming computers in English. Now,
[04:28] programming computers in English. Now, when I was at uh Tesla, um we were
[04:31] when I was at uh Tesla, um we were
[04:31] when I was at uh Tesla, um we were working on the uh autopilot and uh we
[04:34] working on the uh autopilot and uh we
[04:34] working on the uh autopilot and uh we were trying to get the car to drive and
[04:37] were trying to get the car to drive and
[04:37] were trying to get the car to drive and I sort of showed this slide at the time
[04:39] I sort of showed this slide at the time
[04:39] I sort of showed this slide at the time where you can imagine that the inputs to
[04:41] where you can imagine that the inputs to
[04:41] where you can imagine that the inputs to the car are on the bottom and they're
[04:43] the car are on the bottom and they're
[04:43] the car are on the bottom and they're going through a software stack to
[04:44] going through a software stack to
[04:44] going through a software stack to produce the steering and acceleration
[04:47] produce the steering and acceleration
[04:47] produce the steering and acceleration and I made the observation at the time
[04:48] and I made the observation at the time
[04:48] and I made the observation at the time that there was a ton of C++ code around
[04:51] that there was a ton of C++ code around
[04:51] that there was a ton of C++ code around in the autopilot which was the software
[04:52] in the autopilot which was the software
[04:52] in the autopilot which was the software 1.0 code and then there was some neural
[04:54] 1.0 code and then there was some neural
[04:54] 1.0 code and then there was some neural nets in there doing image recognition
[04:56] nets in there doing image recognition
[04:56] nets in there doing image recognition and uh I kind of observed that over time
[04:58] and uh I kind of observed that over time
[04:58] and uh I kind of observed that over time as we made the autopilot better
[05:00] as we made the autopilot better
[05:00] as we made the autopilot better basically the neural network grew in
[05:02] basically the neural network grew in
[05:02] basically the neural network grew in capability and size and in addition to
[05:05] capability and size and in addition to
[05:05] capability and size and in addition to that all the C++ code was being deleted
[05:08] that all the C++ code was being deleted
[05:08] that all the C++ code was being deleted and kind of like was um and a lot of the
[05:12] and kind of like was um and a lot of the
[05:12] and kind of like was um and a lot of the kind of capabilities and functionality
[05:14] kind of capabilities and functionality
[05:14] kind of capabilities and functionality that was originally written in 1.0 was
[05:16] that was originally written in 1.0 was
[05:16] that was originally written in 1.0 was migrated to 2.0. So as an example, a lot
[05:19] migrated to 2.0. So as an example, a lot
[05:19] migrated to 2.0. So as an example, a lot of the stitching up of information
[05:20] of the stitching up of information
[05:20] of the stitching up of information across images from the different cameras
[05:22] across images from the different cameras
[05:22] across images from the different cameras and across time was done by a neural
[05:24] and across time was done by a neural
[05:24] and across time was done by a neural network and we were able to delete a lot
[05:26] network and we were able to delete a lot
[05:26] network and we were able to delete a lot of code and so the software 2.0 stack
[05:29] of code and so the software 2.0 stack
[05:29] of code and so the software 2.0 stack quite literally ate through the software
[05:32] quite literally ate through the software
[05:32] quite literally ate through the software stack of the autopilot. So I thought
[05:34] stack of the autopilot. So I thought
[05:34] stack of the autopilot. So I thought this was really remarkable at the time
[05:35] this was really remarkable at the time
[05:35] this was really remarkable at the time and I think we're seeing the same thing
[05:37] and I think we're seeing the same thing
[05:37] and I think we're seeing the same thing again where uh basically we have a new
[05:39] again where uh basically we have a new
[05:39] again where uh basically we have a new kind of software and it's eating through
[05:40] kind of software and it's eating through
[05:40] kind of software and it's eating through the stack. We have three completely
[05:42] the stack. We have three completely
[05:42] the stack. We have three completely different programming paradigms and I
[05:44] different programming paradigms and I
[05:44] different programming paradigms and I think if you're entering the industry
[05:45] think if you're entering the industry
[05:45] think if you're entering the industry it's a very good idea to be fluent in
[05:47] it's a very good idea to be fluent in
[05:47] it's a very good idea to be fluent in all of them because they all have slight
[05:49] all of them because they all have slight
[05:49] all of them because they all have slight pros and cons and you may want to
[05:50] pros and cons and you may want to
[05:50] pros and cons and you may want to program some functionality in 1.0 or 2.0
[05:53] program some functionality in 1.0 or 2.0
[05:53] program some functionality in 1.0 or 2.0 or 3.0. Are you going to train
[05:54] or 3.0. Are you going to train
[05:54] or 3.0. Are you going to train neurallet? Are you going to just prompt
[05:55] neurallet? Are you going to just prompt
[05:55] neurallet? Are you going to just prompt an LLM? Should this be a piece of code
[05:57] an LLM? Should this be a piece of code
[05:57] an LLM? Should this be a piece of code that's explicit etc. So we all have to
[05:59] that's explicit etc. So we all have to
[05:59] that's explicit etc. So we all have to make these decisions and actually
[06:00] make these decisions and actually
[06:00] make these decisions and actually potentially uh fluidly trans transition
[06:03] potentially uh fluidly trans transition
[06:03] potentially uh fluidly trans transition between these paradigms. So what I
[06:06] between these paradigms. So what I
[06:06] between these paradigms. So what I wanted to get into now is first I want
[06:09] wanted to get into now is first I want
[06:09] wanted to get into now is first I want to in the first part talk about LLMs and
[06:11] to in the first part talk about LLMs and
[06:11] to in the first part talk about LLMs and how to kind of like think of this new
[06:13] how to kind of like think of this new
[06:13] how to kind of like think of this new paradigm and the ecosystem and what that
[06:15] paradigm and the ecosystem and what that
[06:15] paradigm and the ecosystem and what that looks like. Uh like what are what is
[06:17] looks like. Uh like what are what is
[06:17] looks like. Uh like what are what is this new computer? What does it look
[06:18] this new computer? What does it look
[06:18] this new computer? What does it look like and what does the ecosystem look
[06:20] like and what does the ecosystem look
[06:20] like and what does the ecosystem look like? Um I was struck by this quote from
[06:23] like? Um I was struck by this quote from
[06:23] like? Um I was struck by this quote from Anduring actually uh many years ago now
[06:25] Anduring actually uh many years ago now
[06:25] Anduring actually uh many years ago now I think and I think Andrew is going to
[06:27] I think and I think Andrew is going to
[06:27] I think and I think Andrew is going to be speaking right after me. Uh but he
[06:29] be speaking right after me. Uh but he
[06:29] be speaking right after me. Uh but he said at the time AI is the new
[06:30] said at the time AI is the new
[06:30] said at the time AI is the new electricity and I do think that it um
[06:33] electricity and I do think that it um
[06:33] electricity and I do think that it um kind of captures something very
[06:34] kind of captures something very
[06:34] kind of captures something very interesting in that LLMs certainly feel
[06:36] interesting in that LLMs certainly feel
[06:36] interesting in that LLMs certainly feel like they have properties of utilities
[06:38] like they have properties of utilities
[06:38] like they have properties of utilities right now. So
[06:41] right now. So
[06:41] right now. So um LLM labs like OpenAI, Gemini,
[06:44] um LLM labs like OpenAI, Gemini,
[06:44] um LLM labs like OpenAI, Gemini, Enthropic etc. They spend capex to train
[06:47] Enthropic etc. They spend capex to train
[06:47] Enthropic etc. They spend capex to train the LLMs and this is kind of equivalent
[06:48] the LLMs and this is kind of equivalent
[06:48] the LLMs and this is kind of equivalent to building out a grid and then there's
[06:51] to building out a grid and then there's
[06:51] to building out a grid and then there's opex to serve that intelligence over
[06:53] opex to serve that intelligence over
[06:53] opex to serve that intelligence over APIs to all of us and this is done
[06:56] APIs to all of us and this is done
[06:56] APIs to all of us and this is done through metered access where we pay per
[06:58] through metered access where we pay per
[06:58] through metered access where we pay per million tokens or something like that
[07:00] million tokens or something like that
[07:00] million tokens or something like that and we have a lot of demands that are
[07:01] and we have a lot of demands that are
[07:01] and we have a lot of demands that are very utility- like demands out of this
[07:03] very utility- like demands out of this
[07:03] very utility- like demands out of this API we demand low latency high uptime
[07:06] API we demand low latency high uptime
[07:06] API we demand low latency high uptime consistent quality etc. In electricity,
[07:08] consistent quality etc. In electricity,
[07:08] consistent quality etc. In electricity, you would have a transfer switch. So you
[07:10] you would have a transfer switch. So you
[07:10] you would have a transfer switch. So you can transfer your electricity source
[07:12] can transfer your electricity source
[07:12] can transfer your electricity source from like grid and solar or battery or
[07:14] from like grid and solar or battery or
[07:14] from like grid and solar or battery or generator. In LLM, we have maybe open
[07:16] generator. In LLM, we have maybe open
[07:16] generator. In LLM, we have maybe open router and easily switch between the
[07:18] router and easily switch between the
[07:18] router and easily switch between the different types of LLMs that exist.
[07:20] different types of LLMs that exist.
[07:20] different types of LLMs that exist. Because the LLM are software, they don't
[07:23] Because the LLM are software, they don't
[07:23] Because the LLM are software, they don't compete for physical space. So it's okay
[07:25] compete for physical space. So it's okay
[07:25] compete for physical space. So it's okay to have basically like six electricity
[07:26] to have basically like six electricity
[07:26] to have basically like six electricity providers and you can switch between
[07:28] providers and you can switch between
[07:28] providers and you can switch between them, right? Because they don't compete
[07:29] them, right? Because they don't compete
[07:29] them, right? Because they don't compete in such a direct way. And I think what's
[07:31] in such a direct way. And I think what's
[07:31] in such a direct way. And I think what's also a little fascinating and we saw
[07:33] also a little fascinating and we saw
[07:33] also a little fascinating and we saw this in the last few days actually a lot
[07:36] this in the last few days actually a lot
[07:36] this in the last few days actually a lot of the LLMs went down and people were
[07:38] of the LLMs went down and people were
[07:38] of the LLMs went down and people were kind of like stuck and unable to work.
[07:41] kind of like stuck and unable to work.
[07:41] kind of like stuck and unable to work. And uh I think it's kind of fascinating
[07:42] And uh I think it's kind of fascinating
[07:42] And uh I think it's kind of fascinating to me that when the state-of-the-art
[07:43] to me that when the state-of-the-art
[07:43] to me that when the state-of-the-art LLMs go down, it's actually kind of like
[07:45] LLMs go down, it's actually kind of like
[07:45] LLMs go down, it's actually kind of like an intelligence brownout in the world.
[07:47] an intelligence brownout in the world.
[07:47] an intelligence brownout in the world. It's kind of like when the voltage is
[07:49] It's kind of like when the voltage is
[07:49] It's kind of like when the voltage is unreliable in the grid and uh the planet
[07:52] unreliable in the grid and uh the planet
[07:52] unreliable in the grid and uh the planet just gets dumber the more reliance we
[07:55] just gets dumber the more reliance we
[07:55] just gets dumber the more reliance we have on these models, which already is
[07:56] have on these models, which already is
[07:56] have on these models, which already is like really dramatic and I think will
[07:58] like really dramatic and I think will
[07:58] like really dramatic and I think will continue to grow. But LLM's don't only
[08:00] continue to grow. But LLM's don't only
[08:00] continue to grow. But LLM's don't only have properties of utilities. I think
[08:02] have properties of utilities. I think
[08:02] have properties of utilities. I think it's also fair to say that they have
[08:03] it's also fair to say that they have
[08:03] it's also fair to say that they have some properties of fabs. And the reason
[08:06] some properties of fabs. And the reason
[08:06] some properties of fabs. And the reason for this is that the capex required for
[08:09] for this is that the capex required for
[08:09] for this is that the capex required for building LLM is actually quite large. Uh
[08:12] building LLM is actually quite large. Uh
[08:12] building LLM is actually quite large. Uh it's not just like building some uh
[08:14] it's not just like building some uh
[08:14] it's not just like building some uh power station or something like that,
[08:15] power station or something like that,
[08:15] power station or something like that, right? You're investing a huge amount of
[08:17] right? You're investing a huge amount of
[08:17] right? You're investing a huge amount of money and I think the tech tree and uh
[08:19] money and I think the tech tree and uh
[08:20] money and I think the tech tree and uh for the technology is growing quite
[08:22] for the technology is growing quite
[08:22] for the technology is growing quite rapidly. So we're in a world where we
[08:24] rapidly. So we're in a world where we
[08:24] rapidly. So we're in a world where we have sort of deep tech trees, research
[08:26] have sort of deep tech trees, research
[08:26] have sort of deep tech trees, research and development secrets that are
[08:28] and development secrets that are
[08:28] and development secrets that are centralizing inside the LLM labs. Um and
[08:32] centralizing inside the LLM labs. Um and
[08:32] centralizing inside the LLM labs. Um and but I think the analogy muddies a little
[08:34] but I think the analogy muddies a little
[08:34] but I think the analogy muddies a little bit also because as I mentioned this is
[08:36] bit also because as I mentioned this is
[08:36] bit also because as I mentioned this is software and software is a bit less
[08:38] software and software is a bit less
[08:38] software and software is a bit less defensible because it is so malleable.
[08:40] defensible because it is so malleable.
[08:40] defensible because it is so malleable. And so um I think it's just an
[08:43] And so um I think it's just an
[08:43] And so um I think it's just an interesting kind of thing to think about
[08:44] interesting kind of thing to think about
[08:44] interesting kind of thing to think about potentially. There's many analogy
[08:46] potentially. There's many analogy
[08:46] potentially. There's many analogy analogies you can make like a 4
[08:48] analogies you can make like a 4
[08:48] analogies you can make like a 4 nanometer process node maybe is
[08:49] nanometer process node maybe is
[08:49] nanometer process node maybe is something like a cluster with certain
[08:51] something like a cluster with certain
[08:51] something like a cluster with certain max flops. You can think about when
[08:53] max flops. You can think about when
[08:53] max flops. You can think about when you're use when you're using Nvidia GPUs
[08:54] you're use when you're using Nvidia GPUs
[08:54] you're use when you're using Nvidia GPUs and you're only doing the software and
[08:56] and you're only doing the software and
[08:56] and you're only doing the software and you're not doing the hardware. That's
[08:57] you're not doing the hardware. That's
[08:57] you're not doing the hardware. That's kind of like the fabless model. But if
[08:59] kind of like the fabless model. But if
[08:59] kind of like the fabless model. But if you're actually also building your own
[09:00] you're actually also building your own
[09:00] you're actually also building your own hardware and you're training on TPUs if
[09:01] hardware and you're training on TPUs if
[09:02] hardware and you're training on TPUs if you're Google, that's kind of like the
[09:03] you're Google, that's kind of like the
[09:03] you're Google, that's kind of like the Intel model where you own your fab. So I
[09:05] Intel model where you own your fab. So I
[09:05] Intel model where you own your fab. So I think there's some analogies here that
[09:06] think there's some analogies here that
[09:06] think there's some analogies here that make sense. But actually I think the
[09:08] make sense. But actually I think the
[09:08] make sense. But actually I think the analogy that makes the most sense
[09:09] analogy that makes the most sense
[09:09] analogy that makes the most sense perhaps is that in my mind LLM have very
[09:12] perhaps is that in my mind LLM have very
[09:12] perhaps is that in my mind LLM have very strong kind of analogies to operating
[09:15] strong kind of analogies to operating
[09:15] strong kind of analogies to operating systems. Uh in that this is not just
[09:17] systems. Uh in that this is not just
[09:17] systems. Uh in that this is not just electricity or water. It's not something
[09:19] electricity or water. It's not something
[09:19] electricity or water. It's not something that comes out of the tap as a
[09:20] that comes out of the tap as a
[09:20] that comes out of the tap as a commodity. uh this is these are now
[09:22] commodity. uh this is these are now
[09:22] commodity. uh this is these are now increasingly complex software ecosystems
[09:25] increasingly complex software ecosystems
[09:25] increasingly complex software ecosystems right so uh they're not just like simple
[09:28] right so uh they're not just like simple
[09:28] right so uh they're not just like simple commodities like electricity and it's
[09:30] commodities like electricity and it's
[09:30] commodities like electricity and it's kind of interesting to me that the
[09:31] kind of interesting to me that the
[09:32] kind of interesting to me that the ecosystem is shaping in a very similar
[09:33] ecosystem is shaping in a very similar
[09:33] ecosystem is shaping in a very similar kind of way where you have a few closed
[09:36] kind of way where you have a few closed
[09:36] kind of way where you have a few closed source providers like Windows or Mac OS
[09:38] source providers like Windows or Mac OS
[09:38] source providers like Windows or Mac OS and then you have an open source
[09:39] and then you have an open source
[09:39] and then you have an open source alternative like Linux and I think for u
[09:42] alternative like Linux and I think for u
[09:42] alternative like Linux and I think for u neural for LLMs as well we have a kind
[09:45] neural for LLMs as well we have a kind
[09:45] neural for LLMs as well we have a kind of a few competing closed source
[09:47] of a few competing closed source
[09:47] of a few competing closed source providers and then maybe the llama
[09:49] providers and then maybe the llama
[09:49] providers and then maybe the llama ecosystem is currently like maybe a
[09:51] ecosystem is currently like maybe a
[09:51] ecosystem is currently like maybe a close approximation to something that
[09:53] close approximation to something that
[09:53] close approximation to something that may grow into something like Linux.
[09:55] may grow into something like Linux.
[09:55] may grow into something like Linux. Again, I think it's still very early
[09:56] Again, I think it's still very early
[09:56] Again, I think it's still very early because these are just simple LLMs, but
[09:58] because these are just simple LLMs, but
[09:58] because these are just simple LLMs, but we're starting to see that these are
[09:59] we're starting to see that these are
[09:59] we're starting to see that these are going to get a lot more complicated.
[10:01] going to get a lot more complicated.
[10:01] going to get a lot more complicated. It's not just about the LLM itself. It's
[10:02] It's not just about the LLM itself. It's
[10:02] It's not just about the LLM itself. It's about all the tool use and the
[10:03] about all the tool use and the
[10:03] about all the tool use and the multiodalities and how all of that
[10:05] multiodalities and how all of that
[10:05] multiodalities and how all of that works. And so when I sort of had this
[10:07] works. And so when I sort of had this
[10:07] works. And so when I sort of had this realization a while back, I tried to
[10:09] realization a while back, I tried to
[10:09] realization a while back, I tried to sketch it out and it kind of seemed to
[10:11] sketch it out and it kind of seemed to
[10:11] sketch it out and it kind of seemed to me like LLMs are kind of like a new
[10:12] me like LLMs are kind of like a new
[10:12] me like LLMs are kind of like a new operating system, right? So the LLM is a
[10:15] operating system, right? So the LLM is a
[10:15] operating system, right? So the LLM is a new kind of a computer. It's sitting
[10:17] new kind of a computer. It's sitting
[10:17] new kind of a computer. It's sitting it's kind of like the CPU equivalent. uh
[10:19] it's kind of like the CPU equivalent. uh
[10:19] it's kind of like the CPU equivalent. uh the context windows are kind of like the
[10:21] the context windows are kind of like the
[10:21] the context windows are kind of like the memory and then the LLM is orchestrating
[10:24] memory and then the LLM is orchestrating
[10:24] memory and then the LLM is orchestrating memory and compute uh for problem
[10:26] memory and compute uh for problem
[10:26] memory and compute uh for problem solving um using all of these uh
[10:29] solving um using all of these uh
[10:29] solving um using all of these uh capabilities here and so definitely if
[10:32] capabilities here and so definitely if
[10:32] capabilities here and so definitely if you look at it looks very much like
[10:34] you look at it looks very much like
[10:34] you look at it looks very much like operating system from that perspective.
[10:36] operating system from that perspective.
[10:36] operating system from that perspective. Um, a few more analogies. For example,
[10:38] Um, a few more analogies. For example,
[10:38] Um, a few more analogies. For example, if you want to download an app, say I go
[10:41] if you want to download an app, say I go
[10:41] if you want to download an app, say I go to VS Code and I go to download, you can
[10:43] to VS Code and I go to download, you can
[10:43] to VS Code and I go to download, you can download VS Code and you can run it on
[10:46] download VS Code and you can run it on
[10:46] download VS Code and you can run it on Windows, Linux or or Mac in the same way
[10:50] Windows, Linux or or Mac in the same way
[10:50] Windows, Linux or or Mac in the same way as you can take an LLM app like cursor
[10:53] as you can take an LLM app like cursor
[10:53] as you can take an LLM app like cursor and you can run it on GPT or cloud or
[10:55] and you can run it on GPT or cloud or
[10:55] and you can run it on GPT or cloud or Gemini series, right? It's just a drop
[10:57] Gemini series, right? It's just a drop
[10:57] Gemini series, right? It's just a drop down. So, it's kind of like similar in
[10:59] down. So, it's kind of like similar in
[10:59] down. So, it's kind of like similar in that way as well.
[11:00] that way as well.
[11:00] that way as well. uh more analogies that I think strike me
[11:02] uh more analogies that I think strike me
[11:02] uh more analogies that I think strike me is that we're kind of like in this
[11:04] is that we're kind of like in this
[11:04] is that we're kind of like in this 1960sish
[11:05] 1960sish
[11:05] 1960sish era where LLM compute is still very
[11:09] era where LLM compute is still very
[11:09] era where LLM compute is still very expensive for this new kind of a
[11:10] expensive for this new kind of a
[11:10] expensive for this new kind of a computer and that forces the LLMs to be
[11:13] computer and that forces the LLMs to be
[11:13] computer and that forces the LLMs to be centralized in the cloud and we're all
[11:15] centralized in the cloud and we're all
[11:15] centralized in the cloud and we're all just uh sort of thing clients that
[11:18] just uh sort of thing clients that
[11:18] just uh sort of thing clients that interact with it over the network and
[11:20] interact with it over the network and
[11:20] interact with it over the network and none of us have full utilization of
[11:22] none of us have full utilization of
[11:22] none of us have full utilization of these computers and therefore it makes
[11:24] these computers and therefore it makes
[11:24] these computers and therefore it makes sense to use time sharing where we're
[11:26] sense to use time sharing where we're
[11:26] sense to use time sharing where we're all just you know a dimension of the
[11:28] all just you know a dimension of the
[11:28] all just you know a dimension of the batch when they're running the computer
[11:29] batch when they're running the computer
[11:30] batch when they're running the computer in the cloud. And this is very much what
[11:31] in the cloud. And this is very much what
[11:32] in the cloud. And this is very much what computers used to look like at during
[11:33] computers used to look like at during
[11:33] computers used to look like at during this time. The operating systems were in
[11:35] this time. The operating systems were in
[11:35] this time. The operating systems were in the cloud. Everything was streamed
[11:36] the cloud. Everything was streamed
[11:36] the cloud. Everything was streamed around and there was batching. And so
[11:39] around and there was batching. And so
[11:39] around and there was batching. And so the p the personal computing revolution
[11:41] the p the personal computing revolution
[11:41] the p the personal computing revolution hasn't happened yet because it's just
[11:42] hasn't happened yet because it's just
[11:42] hasn't happened yet because it's just not economical. It doesn't make sense.
[11:44] not economical. It doesn't make sense.
[11:44] not economical. It doesn't make sense. But I think some people are trying. And
[11:46] But I think some people are trying. And
[11:46] But I think some people are trying. And it turns out that Mac minis, for
[11:48] it turns out that Mac minis, for
[11:48] it turns out that Mac minis, for example, are a very good fit for some of
[11:50] example, are a very good fit for some of
[11:50] example, are a very good fit for some of the LLMs because it's all if you're
[11:52] the LLMs because it's all if you're
[11:52] the LLMs because it's all if you're doing batch one inference, this is all
[11:53] doing batch one inference, this is all
[11:53] doing batch one inference, this is all super memory bound. So this actually
[11:55] super memory bound. So this actually
[11:55] super memory bound. So this actually works.
[11:56] works.
[11:56] works. And uh I think these are some early
[11:58] And uh I think these are some early
[11:58] And uh I think these are some early indications maybe of personal computing.
[12:00] indications maybe of personal computing.
[12:00] indications maybe of personal computing. Uh but this hasn't really happened yet.
[12:02] Uh but this hasn't really happened yet.
[12:02] Uh but this hasn't really happened yet. It's not clear what this looks like.
[12:03] It's not clear what this looks like.
[12:03] It's not clear what this looks like. Maybe some of you get to invent what
[12:05] Maybe some of you get to invent what
[12:05] Maybe some of you get to invent what what this is or how it works or uh what
[12:08] what this is or how it works or uh what
[12:08] what this is or how it works or uh what this should what this should be. Maybe
[12:10] this should what this should be. Maybe
[12:10] this should what this should be. Maybe one more analogy that I'll mention is
[12:12] one more analogy that I'll mention is
[12:12] one more analogy that I'll mention is whenever I talk to Chach or some LLM
[12:14] whenever I talk to Chach or some LLM
[12:14] whenever I talk to Chach or some LLM directly in text, I feel like I'm
[12:16] directly in text, I feel like I'm
[12:16] directly in text, I feel like I'm talking to an operating system through
[12:18] talking to an operating system through
[12:18] talking to an operating system through the terminal. Like it's just it's it's
[12:21] the terminal. Like it's just it's it's
[12:21] the terminal. Like it's just it's it's text. It's direct access to the
[12:22] text. It's direct access to the
[12:22] text. It's direct access to the operating system. And I think a guey
[12:24] operating system. And I think a guey
[12:24] operating system. And I think a guey hasn't yet really been invented in like
[12:26] hasn't yet really been invented in like
[12:26] hasn't yet really been invented in like a general way like should chatt have a
[12:29] a general way like should chatt have a
[12:29] a general way like should chatt have a guey like different than just a tech
[12:31] guey like different than just a tech
[12:31] guey like different than just a tech bubbles. Uh certainly some of the apps
[12:33] bubbles. Uh certainly some of the apps
[12:33] bubbles. Uh certainly some of the apps that we're going to go into in a bit
[12:35] that we're going to go into in a bit
[12:35] that we're going to go into in a bit have guey but there's no like guey
[12:38] have guey but there's no like guey
[12:38] have guey but there's no like guey across all the tasks if that makes
[12:40] across all the tasks if that makes
[12:40] across all the tasks if that makes sense. Um there are some ways in which
[12:43] sense. Um there are some ways in which
[12:43] sense. Um there are some ways in which LLMs are different from kind of
[12:45] LLMs are different from kind of
[12:45] LLMs are different from kind of operating systems in some fairly unique
[12:47] operating systems in some fairly unique
[12:47] operating systems in some fairly unique way and from early computing. And I
[12:49] way and from early computing. And I
[12:49] way and from early computing. And I wrote about uh this one particular
[12:52] wrote about uh this one particular
[12:52] wrote about uh this one particular property that strikes me as very
[12:54] property that strikes me as very
[12:54] property that strikes me as very different uh this time around. It's that
[12:57] different uh this time around. It's that
[12:57] different uh this time around. It's that LLMs like flip they flip the direction
[12:59] LLMs like flip they flip the direction
[12:59] LLMs like flip they flip the direction of technology diffusion uh that is
[13:01] of technology diffusion uh that is
[13:02] of technology diffusion uh that is usually uh present in technology. So for
[13:05] usually uh present in technology. So for
[13:05] usually uh present in technology. So for example with electricity, cryptography,
[13:07] example with electricity, cryptography,
[13:07] example with electricity, cryptography, computing, flight, internet, GPS, lots
[13:09] computing, flight, internet, GPS, lots
[13:09] computing, flight, internet, GPS, lots of new transformative technologies that
[13:10] of new transformative technologies that
[13:10] of new transformative technologies that have not been around. Typically it is
[13:12] have not been around. Typically it is
[13:12] have not been around. Typically it is the government and corporations that are
[13:14] the government and corporations that are
[13:14] the government and corporations that are the first users because it's new and
[13:16] the first users because it's new and
[13:16] the first users because it's new and expensive etc. and it only later
[13:18] expensive etc. and it only later
[13:18] expensive etc. and it only later diffuses to consumer. Uh, but I feel
[13:20] diffuses to consumer. Uh, but I feel
[13:20] diffuses to consumer. Uh, but I feel like LLMs are kind of like flipped
[13:22] like LLMs are kind of like flipped
[13:22] like LLMs are kind of like flipped around. So maybe with early computers,
[13:23] around. So maybe with early computers,
[13:24] around. So maybe with early computers, it was all about ballistics and military
[13:25] it was all about ballistics and military
[13:26] it was all about ballistics and military use, but with LLMs, it's all about how
[13:29] use, but with LLMs, it's all about how
[13:29] use, but with LLMs, it's all about how do you boil an egg or something like
[13:30] do you boil an egg or something like
[13:30] do you boil an egg or something like that. This is certainly like a lot of my
[13:31] that. This is certainly like a lot of my
[13:32] that. This is certainly like a lot of my use. And so it's really fascinating to
[13:33] use. And so it's really fascinating to
[13:33] use. And so it's really fascinating to me that we have a new magical computer
[13:35] me that we have a new magical computer
[13:35] me that we have a new magical computer and it's like helping me boil an egg.
[13:37] and it's like helping me boil an egg.
[13:37] and it's like helping me boil an egg. It's not helping the government do
[13:38] It's not helping the government do
[13:38] It's not helping the government do something really crazy like some
[13:40] something really crazy like some
[13:40] something really crazy like some military ballistics or some special
[13:42] military ballistics or some special
[13:42] military ballistics or some special technology. Indeed, corporations are
[13:43] technology. Indeed, corporations are
[13:43] technology. Indeed, corporations are governments are lagging behind the
[13:45] governments are lagging behind the
[13:45] governments are lagging behind the adoption of all of us, of all of these
[13:47] adoption of all of us, of all of these
[13:47] adoption of all of us, of all of these technologies. So, it's just backwards
[13:48] technologies. So, it's just backwards
[13:48] technologies. So, it's just backwards and I think it informs maybe some of the
[13:50] and I think it informs maybe some of the
[13:50] and I think it informs maybe some of the uses of how we want to use this
[13:52] uses of how we want to use this
[13:52] uses of how we want to use this technology or like where are some of the
[13:53] technology or like where are some of the
[13:53] technology or like where are some of the first apps and so on.
[13:56] first apps and so on.
[13:56] first apps and so on. So, in summary so far, LLM labs LLMs. I
[14:01] So, in summary so far, LLM labs LLMs. I
[14:01] So, in summary so far, LLM labs LLMs. I think it's accurate language to use, but
[14:03] think it's accurate language to use, but
[14:03] think it's accurate language to use, but LLMs are complicated operating systems.
[14:06] LLMs are complicated operating systems.
[14:06] LLMs are complicated operating systems. They're circa 1960s in computing and
[14:08] They're circa 1960s in computing and
[14:08] They're circa 1960s in computing and we're redoing computing all over again.
[14:10] we're redoing computing all over again.
[14:10] we're redoing computing all over again. and they're currently available via time
[14:11] and they're currently available via time
[14:11] and they're currently available via time sharing and distributed like a utility.
[14:13] sharing and distributed like a utility.
[14:13] sharing and distributed like a utility. What is new and unprecedented is that
[14:15] What is new and unprecedented is that
[14:16] What is new and unprecedented is that they're not in the hands of a few
[14:17] they're not in the hands of a few
[14:17] they're not in the hands of a few governments and corporations. They're in
[14:18] governments and corporations. They're in
[14:18] governments and corporations. They're in the hands of all of us because we all
[14:20] the hands of all of us because we all
[14:20] the hands of all of us because we all have a computer and it's all just
[14:21] have a computer and it's all just
[14:21] have a computer and it's all just software and Chaship was beamed down to
[14:24] software and Chaship was beamed down to
[14:24] software and Chaship was beamed down to our computers like billions of people
[14:26] our computers like billions of people
[14:26] our computers like billions of people like instantly and overnight and this is
[14:28] like instantly and overnight and this is
[14:28] like instantly and overnight and this is insane. Uh and it's kind of insane to me
[14:30] insane. Uh and it's kind of insane to me
[14:30] insane. Uh and it's kind of insane to me that this is the case and now it is our
[14:33] that this is the case and now it is our
[14:33] that this is the case and now it is our time to enter the industry and program
[14:34] time to enter the industry and program
[14:34] time to enter the industry and program these computers. This is crazy. So I
[14:37] these computers. This is crazy. So I
[14:37] these computers. This is crazy. So I think this is quite remarkable. Before
[14:39] think this is quite remarkable. Before
[14:39] think this is quite remarkable. Before we program LLMs, we have to kind of like
[14:42] we program LLMs, we have to kind of like
[14:42] we program LLMs, we have to kind of like spend some time to think about what
[14:43] spend some time to think about what
[14:43] spend some time to think about what these things are. And I especially like
[14:45] these things are. And I especially like
[14:45] these things are. And I especially like to kind of talk about their psychology.
[14:48] to kind of talk about their psychology.
[14:48] to kind of talk about their psychology. So the way I like to think about LLMs is
[14:50] So the way I like to think about LLMs is
[14:50] So the way I like to think about LLMs is that they're kind of like people
[14:51] that they're kind of like people
[14:51] that they're kind of like people spirits. Um they are stoastic
[14:54] spirits. Um they are stoastic
[14:54] spirits. Um they are stoastic simulations of people. Um and the
[14:56] simulations of people. Um and the
[14:56] simulations of people. Um and the simulator in this case happens to be an
[14:57] simulator in this case happens to be an
[14:58] simulator in this case happens to be an auto reggressive transformer. So
[14:59] auto reggressive transformer. So
[14:59] auto reggressive transformer. So transformer is a neural net. Uh it's and
[15:02] transformer is a neural net. Uh it's and
[15:02] transformer is a neural net. Uh it's and it just kind of like is goes on the
[15:04] it just kind of like is goes on the
[15:04] it just kind of like is goes on the level of tokens. It goes chunk chunk
[15:06] level of tokens. It goes chunk chunk
[15:06] level of tokens. It goes chunk chunk chunk chunk chunk. And there's an almost
[15:08] chunk chunk chunk. And there's an almost
[15:08] chunk chunk chunk. And there's an almost equal amount of compute for every single
[15:10] equal amount of compute for every single
[15:10] equal amount of compute for every single chunk. Um and um this simulator of
[15:14] chunk. Um and um this simulator of
[15:14] chunk. Um and um this simulator of course is is just is basically there's
[15:16] course is is just is basically there's
[15:16] course is is just is basically there's some weights involved and we fit it to
[15:19] some weights involved and we fit it to
[15:19] some weights involved and we fit it to all of text that we have on the internet
[15:20] all of text that we have on the internet
[15:20] all of text that we have on the internet and so on. And you end up with this kind
[15:22] and so on. And you end up with this kind
[15:22] and so on. And you end up with this kind of a simulator and because it is trained
[15:24] of a simulator and because it is trained
[15:24] of a simulator and because it is trained on humans, it's got this emergent
[15:26] on humans, it's got this emergent
[15:26] on humans, it's got this emergent psychology that is humanlike. So the
[15:28] psychology that is humanlike. So the
[15:28] psychology that is humanlike. So the first thing you'll notice is of course
[15:30] first thing you'll notice is of course
[15:30] first thing you'll notice is of course uh LLM have encyclopedic knowledge and
[15:32] uh LLM have encyclopedic knowledge and
[15:32] uh LLM have encyclopedic knowledge and memory. uh and they can remember lots of
[15:34] memory. uh and they can remember lots of
[15:34] memory. uh and they can remember lots of things, a lot more than any single
[15:36] things, a lot more than any single
[15:36] things, a lot more than any single individual human can because they read
[15:37] individual human can because they read
[15:37] individual human can because they read so many things. It's it actually kind of
[15:39] so many things. It's it actually kind of
[15:39] so many things. It's it actually kind of reminds me of this movie Rainman, which
[15:41] reminds me of this movie Rainman, which
[15:41] reminds me of this movie Rainman, which I actually really recommend people
[15:43] I actually really recommend people
[15:43] I actually really recommend people watch. It's an amazing movie. I love
[15:44] watch. It's an amazing movie. I love
[15:44] watch. It's an amazing movie. I love this movie. Um and Dustin Hoffman here
[15:46] this movie. Um and Dustin Hoffman here
[15:46] this movie. Um and Dustin Hoffman here is an autistic savant who has almost
[15:49] is an autistic savant who has almost
[15:49] is an autistic savant who has almost perfect memory. So, he can read a he can
[15:51] perfect memory. So, he can read a he can
[15:51] perfect memory. So, he can read a he can read like a phone book and remember all
[15:53] read like a phone book and remember all
[15:53] read like a phone book and remember all of the names and phone numbers. And I
[15:55] of the names and phone numbers. And I
[15:55] of the names and phone numbers. And I kind of feel like LM are kind of like
[15:57] kind of feel like LM are kind of like
[15:57] kind of feel like LM are kind of like very similar. They can remember Shaw
[15:58] very similar. They can remember Shaw
[15:58] very similar. They can remember Shaw hashes and lots of different kinds of
[16:00] hashes and lots of different kinds of
[16:00] hashes and lots of different kinds of things very very easily. So they
[16:02] things very very easily. So they
[16:02] things very very easily. So they certainly have superpowers in some set
[16:04] certainly have superpowers in some set
[16:04] certainly have superpowers in some set in some respects. But they also have a
[16:06] in some respects. But they also have a
[16:06] in some respects. But they also have a bunch of I would say cognitive deficits.
[16:08] bunch of I would say cognitive deficits.
[16:08] bunch of I would say cognitive deficits. So they hallucinate quite a bit. Um and
[16:11] So they hallucinate quite a bit. Um and
[16:11] So they hallucinate quite a bit. Um and they kind of make up stuff and don't
[16:13] they kind of make up stuff and don't
[16:13] they kind of make up stuff and don't have a very good uh sort of internal
[16:15] have a very good uh sort of internal
[16:15] have a very good uh sort of internal model of self-nowledge, not sufficient
[16:17] model of self-nowledge, not sufficient
[16:17] model of self-nowledge, not sufficient at least. And this has gotten better but
[16:19] at least. And this has gotten better but
[16:19] at least. And this has gotten better but not perfect. They display jagged
[16:21] not perfect. They display jagged
[16:21] not perfect. They display jagged intelligence. So they're going to be
[16:22] intelligence. So they're going to be
[16:22] intelligence. So they're going to be superhuman in some problems solving
[16:24] superhuman in some problems solving
[16:24] superhuman in some problems solving domains. And then they're going to make
[16:25] domains. And then they're going to make
[16:26] domains. And then they're going to make mistakes that basically no human will
[16:27] mistakes that basically no human will
[16:27] mistakes that basically no human will make. like you know they will insist
[16:29] make. like you know they will insist
[16:29] make. like you know they will insist that 9.11 is greater than 9.9 or that
[16:32] that 9.11 is greater than 9.9 or that
[16:32] that 9.11 is greater than 9.9 or that there are two Rs in strawberry these are
[16:34] there are two Rs in strawberry these are
[16:34] there are two Rs in strawberry these are some famous examples but basically there
[16:36] some famous examples but basically there
[16:36] some famous examples but basically there are rough edges that you can trip on so
[16:38] are rough edges that you can trip on so
[16:38] are rough edges that you can trip on so that's kind of I think also kind of
[16:40] that's kind of I think also kind of
[16:40] that's kind of I think also kind of unique um they also kind of suffer from
[16:43] unique um they also kind of suffer from
[16:43] unique um they also kind of suffer from entrograde amnesia um so uh and I think
[16:46] entrograde amnesia um so uh and I think
[16:46] entrograde amnesia um so uh and I think I'm alluding to the fact that if you
[16:48] I'm alluding to the fact that if you
[16:48] I'm alluding to the fact that if you have a co-orker who joins your
[16:49] have a co-orker who joins your
[16:49] have a co-orker who joins your organization this co-orker will over
[16:51] organization this co-orker will over
[16:51] organization this co-orker will over time learn your organization and uh they
[16:54] time learn your organization and uh they
[16:54] time learn your organization and uh they will understand and gain like a huge
[16:55] will understand and gain like a huge
[16:55] will understand and gain like a huge amount of context on the organization
[16:57] amount of context on the organization
[16:57] amount of context on the organization and they go home and they sleep and they
[16:59] and they go home and they sleep and they
[16:59] and they go home and they sleep and they consolidate knowledge and they develop
[17:01] consolidate knowledge and they develop
[17:01] consolidate knowledge and they develop expertise over time. LLMs don't natively
[17:03] expertise over time. LLMs don't natively
[17:03] expertise over time. LLMs don't natively do this and this is not something that
[17:04] do this and this is not something that
[17:04] do this and this is not something that has really been solved in the R&D of
[17:06] has really been solved in the R&D of
[17:06] has really been solved in the R&D of LLM. I think um and so context windows
[17:09] LLM. I think um and so context windows
[17:09] LLM. I think um and so context windows are really kind of like working memory
[17:10] are really kind of like working memory
[17:10] are really kind of like working memory and you have to sort of program the
[17:11] and you have to sort of program the
[17:12] and you have to sort of program the working memory quite directly because
[17:13] working memory quite directly because
[17:13] working memory quite directly because they don't just kind of like get smarter
[17:15] they don't just kind of like get smarter
[17:15] they don't just kind of like get smarter by uh by default and I think a lot of
[17:17] by uh by default and I think a lot of
[17:17] by uh by default and I think a lot of people get tripped up by the analogies
[17:19] people get tripped up by the analogies
[17:19] people get tripped up by the analogies uh in this way. Uh in popular culture I
[17:22] uh in this way. Uh in popular culture I
[17:22] uh in this way. Uh in popular culture I recommend people watch these two movies
[17:23] recommend people watch these two movies
[17:23] recommend people watch these two movies uh Momento and 51st dates. In both of
[17:26] uh Momento and 51st dates. In both of
[17:26] uh Momento and 51st dates. In both of these movies, the protagonists, their
[17:27] these movies, the protagonists, their
[17:27] these movies, the protagonists, their weights are fixed and their context
[17:29] weights are fixed and their context
[17:29] weights are fixed and their context windows gets wiped every single morning
[17:32] windows gets wiped every single morning
[17:32] windows gets wiped every single morning and it's really problematic to go to
[17:34] and it's really problematic to go to
[17:34] and it's really problematic to go to work or have relationships when this
[17:35] work or have relationships when this
[17:35] work or have relationships when this happens and this happens to all the
[17:37] happens and this happens to all the
[17:37] happens and this happens to all the time. I guess one more thing I would
[17:39] time. I guess one more thing I would
[17:39] time. I guess one more thing I would point to is security kind of related
[17:42] point to is security kind of related
[17:42] point to is security kind of related limitations of the use of LLM. So for
[17:44] limitations of the use of LLM. So for
[17:44] limitations of the use of LLM. So for example, LLMs are quite gullible. Uh
[17:46] example, LLMs are quite gullible. Uh
[17:46] example, LLMs are quite gullible. Uh they are susceptible to prompt injection
[17:48] they are susceptible to prompt injection
[17:48] they are susceptible to prompt injection risks. They might leak your data etc.
[17:50] risks. They might leak your data etc.
[17:50] risks. They might leak your data etc. And so um and there's many other
[17:52] And so um and there's many other
[17:52] And so um and there's many other considerations uh security related. So,
[17:55] considerations uh security related. So,
[17:55] considerations uh security related. So, so basically long story short, you have
[17:57] so basically long story short, you have
[17:57] so basically long story short, you have to load your you have to load your you
[17:59] to load your you have to load your you
[18:00] to load your you have to load your you have to simultaneously think through
[18:01] have to simultaneously think through
[18:01] have to simultaneously think through this superhuman thing that has a bunch
[18:03] this superhuman thing that has a bunch
[18:03] this superhuman thing that has a bunch of cognitive deficits and issues. How do
[18:05] of cognitive deficits and issues. How do
[18:05] of cognitive deficits and issues. How do we and yet they are extremely like
[18:07] we and yet they are extremely like
[18:07] we and yet they are extremely like useful and so how do we program them and
[18:10] useful and so how do we program them and
[18:10] useful and so how do we program them and how do we work around their deficits and
[18:12] how do we work around their deficits and
[18:12] how do we work around their deficits and enjoy their superhuman powers.
[18:15] enjoy their superhuman powers.
[18:15] enjoy their superhuman powers. So what I want to switch to now is talk
[18:17] So what I want to switch to now is talk
[18:17] So what I want to switch to now is talk about the opportunities of how do we use
[18:18] about the opportunities of how do we use
[18:18] about the opportunities of how do we use these models and what are some of the
[18:20] these models and what are some of the
[18:20] these models and what are some of the biggest opportunities. This is not a
[18:22] biggest opportunities. This is not a
[18:22] biggest opportunities. This is not a comprehensive list just some of the
[18:23] comprehensive list just some of the
[18:23] comprehensive list just some of the things that I thought were interesting
[18:24] things that I thought were interesting
[18:24] things that I thought were interesting for this talk. The first thing I'm kind
[18:26] for this talk. The first thing I'm kind
[18:26] for this talk. The first thing I'm kind of excited about is what I would call
[18:29] of excited about is what I would call
[18:29] of excited about is what I would call partial autonomy apps. So for example,
[18:32] partial autonomy apps. So for example,
[18:32] partial autonomy apps. So for example, let's work with the example of coding.
[18:34] let's work with the example of coding.
[18:34] let's work with the example of coding. You can certainly go to chacht directly
[18:36] You can certainly go to chacht directly
[18:36] You can certainly go to chacht directly and you can start copy pasting code
[18:38] and you can start copy pasting code
[18:38] and you can start copy pasting code around and copyping bug reports and
[18:40] around and copyping bug reports and
[18:40] around and copyping bug reports and stuff around and getting code and copy
[18:42] stuff around and getting code and copy
[18:42] stuff around and getting code and copy pasting everything around. Why would you
[18:44] pasting everything around. Why would you
[18:44] pasting everything around. Why would you why would you do that? Why would you go
[18:45] why would you do that? Why would you go
[18:45] why would you do that? Why would you go directly to the operating system? It
[18:47] directly to the operating system? It
[18:47] directly to the operating system? It makes a lot more sense to have an app
[18:48] makes a lot more sense to have an app
[18:48] makes a lot more sense to have an app dedicated for this. And so I think many
[18:50] dedicated for this. And so I think many
[18:50] dedicated for this. And so I think many of you uh use uh cursor. I do as well.
[18:53] of you uh use uh cursor. I do as well.
[18:53] of you uh use uh cursor. I do as well. And uh cursor is kind of like the thing
[18:56] And uh cursor is kind of like the thing
[18:56] And uh cursor is kind of like the thing you want instead. You don't want to just
[18:57] you want instead. You don't want to just
[18:57] you want instead. You don't want to just directly go to the chash apt. And I
[18:59] directly go to the chash apt. And I
[18:59] directly go to the chash apt. And I think cursor is a very good example of
[19:01] think cursor is a very good example of
[19:01] think cursor is a very good example of an early LLM app that has a bunch of
[19:03] an early LLM app that has a bunch of
[19:03] an early LLM app that has a bunch of properties that I think are um useful
[19:06] properties that I think are um useful
[19:06] properties that I think are um useful across all the LLM apps. So in
[19:07] across all the LLM apps. So in
[19:08] across all the LLM apps. So in particular, you will notice that we have
[19:09] particular, you will notice that we have
[19:09] particular, you will notice that we have a traditional interface that allows a
[19:11] a traditional interface that allows a
[19:12] a traditional interface that allows a human to go in and do all the work
[19:13] human to go in and do all the work
[19:13] human to go in and do all the work manually just as before. But in addition
[19:16] manually just as before. But in addition
[19:16] manually just as before. But in addition to that, we now have this LLM
[19:17] to that, we now have this LLM
[19:17] to that, we now have this LLM integration that allows us to go in
[19:19] integration that allows us to go in
[19:19] integration that allows us to go in bigger chunks. And so some of the
[19:21] bigger chunks. And so some of the
[19:21] bigger chunks. And so some of the properties of LLM apps that I think are
[19:23] properties of LLM apps that I think are
[19:23] properties of LLM apps that I think are shared and useful to point out. Number
[19:25] shared and useful to point out. Number
[19:25] shared and useful to point out. Number one, the LLMs basically do a ton of the
[19:28] one, the LLMs basically do a ton of the
[19:28] one, the LLMs basically do a ton of the context management. Um, number two, they
[19:31] context management. Um, number two, they
[19:31] context management. Um, number two, they orchestrate multiple calls to LLMs,
[19:33] orchestrate multiple calls to LLMs,
[19:33] orchestrate multiple calls to LLMs, right? So in the case of cursor, there's
[19:34] right? So in the case of cursor, there's
[19:34] right? So in the case of cursor, there's under the hood embedding models for all
[19:36] under the hood embedding models for all
[19:36] under the hood embedding models for all your files, the actual chat models,
[19:39] your files, the actual chat models,
[19:39] your files, the actual chat models, models that apply diffs to the code, and
[19:41] models that apply diffs to the code, and
[19:41] models that apply diffs to the code, and this is all orchestrated for you. A
[19:43] this is all orchestrated for you. A
[19:43] this is all orchestrated for you. A really big one that uh I think also
[19:46] really big one that uh I think also
[19:46] really big one that uh I think also maybe not fully appreciated always is
[19:48] maybe not fully appreciated always is
[19:48] maybe not fully appreciated always is application specific uh GUI and the
[19:50] application specific uh GUI and the
[19:50] application specific uh GUI and the importance of it. Um because you don't
[19:53] importance of it. Um because you don't
[19:53] importance of it. Um because you don't just want to talk to the operating
[19:54] just want to talk to the operating
[19:54] just want to talk to the operating system directly in text. Text is very
[19:56] system directly in text. Text is very
[19:56] system directly in text. Text is very hard to read, interpret, understand and
[19:59] hard to read, interpret, understand and
[19:59] hard to read, interpret, understand and also like you don't want to take some of
[20:00] also like you don't want to take some of
[20:00] also like you don't want to take some of these actions natively in text. So it's
[20:03] these actions natively in text. So it's
[20:03] these actions natively in text. So it's much better to just see a diff as like
[20:05] much better to just see a diff as like
[20:05] much better to just see a diff as like red and green change and you can see
[20:06] red and green change and you can see
[20:06] red and green change and you can see what's being added is subtracted. It's
[20:08] what's being added is subtracted. It's
[20:08] what's being added is subtracted. It's much easier to just do command Y to
[20:10] much easier to just do command Y to
[20:10] much easier to just do command Y to accept or command N to reject. I
[20:11] accept or command N to reject. I
[20:11] accept or command N to reject. I shouldn't have to type it in text,
[20:13] shouldn't have to type it in text,
[20:13] shouldn't have to type it in text, right? So, a guey allows a human to
[20:15] right? So, a guey allows a human to
[20:15] right? So, a guey allows a human to audit the work of these fallible systems
[20:17] audit the work of these fallible systems
[20:17] audit the work of these fallible systems and to go faster. I'm going to come back
[20:19] and to go faster. I'm going to come back
[20:20] and to go faster. I'm going to come back to this point a little bit uh later as
[20:21] to this point a little bit uh later as
[20:21] to this point a little bit uh later as well. And the last kind of feature I
[20:23] well. And the last kind of feature I
[20:23] well. And the last kind of feature I want to point out is that there's what I
[20:25] want to point out is that there's what I
[20:25] want to point out is that there's what I call the autonomy slider. So, for
[20:27] call the autonomy slider. So, for
[20:27] call the autonomy slider. So, for example, in cursor, you can just do tap
[20:29] example, in cursor, you can just do tap
[20:29] example, in cursor, you can just do tap completion. You're mostly in charge. You
[20:31] completion. You're mostly in charge. You
[20:31] completion. You're mostly in charge. You can select a chunk of code and command K
[20:33] can select a chunk of code and command K
[20:33] can select a chunk of code and command K to change just that chunk of code. You
[20:35] to change just that chunk of code. You
[20:36] to change just that chunk of code. You can do command L to change the entire
[20:37] can do command L to change the entire
[20:37] can do command L to change the entire file. Or you can do command I which just
[20:40] file. Or you can do command I which just
[20:40] file. Or you can do command I which just you know let it rip do whatever you want
[20:42] you know let it rip do whatever you want
[20:42] you know let it rip do whatever you want in the entire repo and that's the sort
[20:44] in the entire repo and that's the sort
[20:44] in the entire repo and that's the sort of full autonomy agent agentic version
[20:46] of full autonomy agent agentic version
[20:46] of full autonomy agent agentic version and so you are in charge of the autonomy
[20:48] and so you are in charge of the autonomy
[20:48] and so you are in charge of the autonomy slider and depending on the complexity
[20:50] slider and depending on the complexity
[20:50] slider and depending on the complexity of the task at hand you can uh tune the
[20:53] of the task at hand you can uh tune the
[20:53] of the task at hand you can uh tune the amount of autonomy that you're willing
[20:54] amount of autonomy that you're willing
[20:54] amount of autonomy that you're willing to give up uh for that task maybe to
[20:57] to give up uh for that task maybe to
[20:57] to give up uh for that task maybe to show one more example of a fairly
[20:58] show one more example of a fairly
[20:58] show one more example of a fairly successful LLM app uh perplexity um it
[21:03] successful LLM app uh perplexity um it
[21:03] successful LLM app uh perplexity um it also has very similar features to what
[21:04] also has very similar features to what
[21:04] also has very similar features to what I've just pointed out to in cursor uh it
[21:07] I've just pointed out to in cursor uh it
[21:07] I've just pointed out to in cursor uh it packages up a lot of the information. It
[21:08] packages up a lot of the information. It
[21:08] packages up a lot of the information. It orchestrates multiple LLMs. It's got a
[21:10] orchestrates multiple LLMs. It's got a
[21:10] orchestrates multiple LLMs. It's got a GUI that allows you to audit some of its
[21:13] GUI that allows you to audit some of its
[21:13] GUI that allows you to audit some of its work. So, for example, it will site
[21:15] work. So, for example, it will site
[21:15] work. So, for example, it will site sources and you can imagine inspecting
[21:17] sources and you can imagine inspecting
[21:17] sources and you can imagine inspecting them. And it's got an autonomy slider.
[21:18] them. And it's got an autonomy slider.
[21:18] them. And it's got an autonomy slider. You can either just do a quick search or
[21:20] You can either just do a quick search or
[21:20] You can either just do a quick search or you can do research or you can do deep
[21:22] you can do research or you can do deep
[21:22] you can do research or you can do deep research and come back 10 minutes later.
[21:24] research and come back 10 minutes later.
[21:24] research and come back 10 minutes later. So, this is all just varying levels of
[21:25] So, this is all just varying levels of
[21:25] So, this is all just varying levels of autonomy that you give up to the tool.
[21:27] autonomy that you give up to the tool.
[21:27] autonomy that you give up to the tool. So, I guess my question is I feel like a
[21:30] So, I guess my question is I feel like a
[21:30] So, I guess my question is I feel like a lot of software will become partially
[21:31] lot of software will become partially
[21:32] lot of software will become partially autonomous. I'm trying to think through
[21:33] autonomous. I'm trying to think through
[21:33] autonomous. I'm trying to think through like what does that look like? And for
[21:35] like what does that look like? And for
[21:35] like what does that look like? And for many of you who maintain products and
[21:36] many of you who maintain products and
[21:36] many of you who maintain products and services, how are you going to make your
[21:38] services, how are you going to make your
[21:38] services, how are you going to make your products and services partially
[21:40] products and services partially
[21:40] products and services partially autonomous? Can an LLM see everything
[21:42] autonomous? Can an LLM see everything
[21:42] autonomous? Can an LLM see everything that a human can see? Can an LLM act in
[21:45] that a human can see? Can an LLM act in
[21:45] that a human can see? Can an LLM act in all the ways that a human could act? And
[21:47] all the ways that a human could act? And
[21:47] all the ways that a human could act? And can humans supervise and stay in the
[21:49] can humans supervise and stay in the
[21:49] can humans supervise and stay in the loop of this activity? Because again,
[21:50] loop of this activity? Because again,
[21:50] loop of this activity? Because again, these are fallible systems that aren't
[21:52] these are fallible systems that aren't
[21:52] these are fallible systems that aren't yet perfect. And what does a diff look
[21:54] yet perfect. And what does a diff look
[21:54] yet perfect. And what does a diff look like in Photoshop or something like
[21:56] like in Photoshop or something like
[21:56] like in Photoshop or something like that? You know, and also a lot of the
[21:58] that? You know, and also a lot of the
[21:58] that? You know, and also a lot of the traditional software right now, it has
[22:00] traditional software right now, it has
[22:00] traditional software right now, it has all these switches and all this kind of
[22:01] all these switches and all this kind of
[22:01] all these switches and all this kind of stuff that's all designed for human. All
[22:03] stuff that's all designed for human. All
[22:03] stuff that's all designed for human. All of this has to change and become
[22:04] of this has to change and become
[22:04] of this has to change and become accessible to LLMs.
[22:07] accessible to LLMs.
[22:07] accessible to LLMs. So, one thing I want to stress with a
[22:09] So, one thing I want to stress with a
[22:09] So, one thing I want to stress with a lot of these LLM apps that I'm not sure
[22:11] lot of these LLM apps that I'm not sure
[22:11] lot of these LLM apps that I'm not sure gets as much attention as it should is
[22:14] gets as much attention as it should is
[22:14] gets as much attention as it should is um we we're now kind of like cooperating
[22:16] um we we're now kind of like cooperating
[22:16] um we we're now kind of like cooperating with AIS and usually they are doing the
[22:18] with AIS and usually they are doing the
[22:18] with AIS and usually they are doing the generation and we as humans are doing
[22:20] generation and we as humans are doing
[22:20] generation and we as humans are doing the verification. It is in our interest
[22:22] the verification. It is in our interest
[22:22] the verification. It is in our interest to make this loop go as fast as
[22:24] to make this loop go as fast as
[22:24] to make this loop go as fast as possible. So, we're getting a lot of
[22:25] possible. So, we're getting a lot of
[22:25] possible. So, we're getting a lot of work done. There are two major ways that
[22:27] work done. There are two major ways that
[22:28] work done. There are two major ways that I think uh this can be done. Number one,
[22:30] I think uh this can be done. Number one,
[22:30] I think uh this can be done. Number one, you can speed up verification a lot. Um,
[22:32] you can speed up verification a lot. Um,
[22:32] you can speed up verification a lot. Um, and I think guies, for example, are
[22:34] and I think guies, for example, are
[22:34] and I think guies, for example, are extremely important to this because a
[22:36] extremely important to this because a
[22:36] extremely important to this because a guey utilizes your computer vision GPU
[22:39] guey utilizes your computer vision GPU
[22:39] guey utilizes your computer vision GPU in all of our head. Reading text is
[22:41] in all of our head. Reading text is
[22:41] in all of our head. Reading text is effortful and it's not fun, but looking
[22:43] effortful and it's not fun, but looking
[22:43] effortful and it's not fun, but looking at stuff is fun and it's it's just a
[22:45] at stuff is fun and it's it's just a
[22:45] at stuff is fun and it's it's just a kind of like a highway to your brain.
[22:47] kind of like a highway to your brain.
[22:47] kind of like a highway to your brain. So, I think guies are very useful for
[22:49] So, I think guies are very useful for
[22:49] So, I think guies are very useful for auditing systems and visual
[22:51] auditing systems and visual
[22:51] auditing systems and visual representations in general. And number
[22:53] representations in general. And number
[22:53] representations in general. And number two, I would say is we have to keep the
[22:56] two, I would say is we have to keep the
[22:56] two, I would say is we have to keep the AI on the leash. We I think a lot of
[22:58] AI on the leash. We I think a lot of
[22:58] AI on the leash. We I think a lot of people are getting way over excited with
[23:00] people are getting way over excited with
[23:00] people are getting way over excited with AI agents and uh it's not useful to me
[23:03] AI agents and uh it's not useful to me
[23:03] AI agents and uh it's not useful to me to get a diff of 10,000 lines of code to
[23:05] to get a diff of 10,000 lines of code to
[23:05] to get a diff of 10,000 lines of code to my repo. Like I have to I'm still the
[23:07] my repo. Like I have to I'm still the
[23:07] my repo. Like I have to I'm still the bottleneck, right? Even though that
[23:09] bottleneck, right? Even though that
[23:09] bottleneck, right? Even though that 10,00 lines come out instantly, I have
[23:11] 10,00 lines come out instantly, I have
[23:11] 10,00 lines come out instantly, I have to make sure that this thing is not
[23:12] to make sure that this thing is not
[23:12] to make sure that this thing is not introducing bugs. It's just like and
[23:15] introducing bugs. It's just like and
[23:15] introducing bugs. It's just like and that it's doing the correct thing,
[23:16] that it's doing the correct thing,
[23:16] that it's doing the correct thing, right? And that there's no security
[23:17] right? And that there's no security
[23:17] right? And that there's no security issues and so on. So um I think that um
[23:22] issues and so on. So um I think that um
[23:22] issues and so on. So um I think that um yeah basically you we have to sort of
[23:25] yeah basically you we have to sort of
[23:25] yeah basically you we have to sort of like it's in our interest to make the
[23:28] like it's in our interest to make the
[23:28] like it's in our interest to make the the flow of these two go very very fast
[23:30] the flow of these two go very very fast
[23:30] the flow of these two go very very fast and we have to somehow keep the AI on
[23:32] and we have to somehow keep the AI on
[23:32] and we have to somehow keep the AI on the leash because it gets way too
[23:33] the leash because it gets way too
[23:33] the leash because it gets way too overreactive. It's uh it's kind of like
[23:35] overreactive. It's uh it's kind of like
[23:35] overreactive. It's uh it's kind of like this. This is how I feel when I do AI
[23:37] this. This is how I feel when I do AI
[23:37] this. This is how I feel when I do AI assisted coding. If I'm just bite coding
[23:39] assisted coding. If I'm just bite coding
[23:39] assisted coding. If I'm just bite coding everything is nice and great but if I'm
[23:40] everything is nice and great but if I'm
[23:40] everything is nice and great but if I'm actually trying to get work done it's
[23:42] actually trying to get work done it's
[23:42] actually trying to get work done it's not so great to have an overreactive uh
[23:44] not so great to have an overreactive uh
[23:44] not so great to have an overreactive uh agent doing all this kind of stuff. So
[23:47] agent doing all this kind of stuff. So
[23:47] agent doing all this kind of stuff. So this slide is not very good. I'm sorry,
[23:48] this slide is not very good. I'm sorry,
[23:48] this slide is not very good. I'm sorry, but I guess I'm trying to develop like
[23:51] but I guess I'm trying to develop like
[23:51] but I guess I'm trying to develop like many of you some ways of utilizing these
[23:53] many of you some ways of utilizing these
[23:53] many of you some ways of utilizing these agents in my coding workflow and to do
[23:55] agents in my coding workflow and to do
[23:55] agents in my coding workflow and to do AI assisted coding. And in my own work,
[23:58] AI assisted coding. And in my own work,
[23:58] AI assisted coding. And in my own work, I'm always scared to get way too big
[23:59] I'm always scared to get way too big
[23:59] I'm always scared to get way too big diffs. I always go in small incremental
[24:02] diffs. I always go in small incremental
[24:02] diffs. I always go in small incremental chunks. I want to make sure that
[24:04] chunks. I want to make sure that
[24:04] chunks. I want to make sure that everything is good. I want to spin this
[24:06] everything is good. I want to spin this
[24:06] everything is good. I want to spin this loop very very fast and um I sort of
[24:09] loop very very fast and um I sort of
[24:09] loop very very fast and um I sort of work on small chunks of single concrete
[24:10] work on small chunks of single concrete
[24:10] work on small chunks of single concrete thing. Uh and so I think many of you
[24:13] thing. Uh and so I think many of you
[24:13] thing. Uh and so I think many of you probably are developing similar ways of
[24:14] probably are developing similar ways of
[24:14] probably are developing similar ways of working with the with LLMs.
[24:17] working with the with LLMs.
[24:17] working with the with LLMs. Um, I also saw a number of blog posts
[24:19] Um, I also saw a number of blog posts
[24:19] Um, I also saw a number of blog posts that try to develop these best practices
[24:22] that try to develop these best practices
[24:22] that try to develop these best practices for working with LLMs. And here's one
[24:23] for working with LLMs. And here's one
[24:24] for working with LLMs. And here's one that I read recently and I thought was
[24:25] that I read recently and I thought was
[24:25] that I read recently and I thought was quite good. And it kind of discussed
[24:26] quite good. And it kind of discussed
[24:26] quite good. And it kind of discussed some techniques and some of them have to
[24:28] some techniques and some of them have to
[24:28] some techniques and some of them have to do with how you keep the AI on the
[24:29] do with how you keep the AI on the
[24:29] do with how you keep the AI on the leash. And so, as an example, if you are
[24:31] leash. And so, as an example, if you are
[24:32] leash. And so, as an example, if you are prompting, if your prompt is vague, then
[24:34] prompting, if your prompt is vague, then
[24:34] prompting, if your prompt is vague, then uh the AI might not do exactly what you
[24:36] uh the AI might not do exactly what you
[24:36] uh the AI might not do exactly what you wanted and in that case, verification
[24:38] wanted and in that case, verification
[24:38] wanted and in that case, verification will fail. You're going to ask for
[24:40] will fail. You're going to ask for
[24:40] will fail. You're going to ask for something else. If a verification fails,
[24:42] something else. If a verification fails,
[24:42] something else. If a verification fails, then you're going to start spinning. So
[24:43] then you're going to start spinning. So
[24:43] then you're going to start spinning. So it makes a lot more sense to spend a bit
[24:45] it makes a lot more sense to spend a bit
[24:45] it makes a lot more sense to spend a bit more time to be more concrete in your
[24:46] more time to be more concrete in your
[24:46] more time to be more concrete in your prompts which increases the probability
[24:48] prompts which increases the probability
[24:48] prompts which increases the probability of successful verification and you can
[24:50] of successful verification and you can
[24:50] of successful verification and you can move forward. And so I think a lot of us
[24:52] move forward. And so I think a lot of us
[24:52] move forward. And so I think a lot of us are going to end up finding um kind of
[24:54] are going to end up finding um kind of
[24:54] are going to end up finding um kind of techniques like this. I think in my own
[24:56] techniques like this. I think in my own
[24:56] techniques like this. I think in my own work as well I'm currently interested in
[24:57] work as well I'm currently interested in
[24:57] work as well I'm currently interested in uh what education looks like in um
[25:00] uh what education looks like in um
[25:00] uh what education looks like in um together with kind of like now that we
[25:01] together with kind of like now that we
[25:01] together with kind of like now that we have AI uh and LLMs what does education
[25:04] have AI uh and LLMs what does education
[25:04] have AI uh and LLMs what does education look like? And I think a a large amount
[25:07] look like? And I think a a large amount
[25:07] look like? And I think a a large amount of thought for me goes into how we keep
[25:09] of thought for me goes into how we keep
[25:09] of thought for me goes into how we keep AI on the leash. I don't think it just
[25:11] AI on the leash. I don't think it just
[25:11] AI on the leash. I don't think it just works to go to chat and be like, "Hey,
[25:13] works to go to chat and be like, "Hey,
[25:13] works to go to chat and be like, "Hey, teach me physics." I don't think this
[25:14] teach me physics." I don't think this
[25:14] teach me physics." I don't think this works because the AI is like gets lost
[25:16] works because the AI is like gets lost
[25:16] works because the AI is like gets lost in the woods. And so for me, this is
[25:18] in the woods. And so for me, this is
[25:18] in the woods. And so for me, this is actually two separate apps. For example,
[25:20] actually two separate apps. For example,
[25:20] actually two separate apps. For example, there's an app for a teacher that
[25:22] there's an app for a teacher that
[25:22] there's an app for a teacher that creates courses and then there's an app
[25:24] creates courses and then there's an app
[25:24] creates courses and then there's an app that takes courses and serves them to
[25:26] that takes courses and serves them to
[25:26] that takes courses and serves them to students. And in both cases, we now have
[25:29] students. And in both cases, we now have
[25:29] students. And in both cases, we now have this intermediate artifact of a course
[25:31] this intermediate artifact of a course
[25:31] this intermediate artifact of a course that is auditable and we can make sure
[25:32] that is auditable and we can make sure
[25:32] that is auditable and we can make sure it's good. We can make sure it's
[25:33] it's good. We can make sure it's
[25:33] it's good. We can make sure it's consistent. and the AI is kept on the
[25:35] consistent. and the AI is kept on the
[25:35] consistent. and the AI is kept on the leash with respect to a certain
[25:37] leash with respect to a certain
[25:37] leash with respect to a certain syllabus, a certain like um progression
[25:40] syllabus, a certain like um progression
[25:40] syllabus, a certain like um progression of projects and so on. And so this is
[25:42] of projects and so on. And so this is
[25:42] of projects and so on. And so this is one way of keeping the AI on leash and I
[25:44] one way of keeping the AI on leash and I
[25:44] one way of keeping the AI on leash and I think has a much higher likelihood of
[25:45] think has a much higher likelihood of
[25:45] think has a much higher likelihood of working and the AI is not getting lost
[25:47] working and the AI is not getting lost
[25:47] working and the AI is not getting lost in the woods.
[25:49] in the woods.
[25:49] in the woods. One more kind of analogy I wanted to
[25:51] One more kind of analogy I wanted to
[25:51] One more kind of analogy I wanted to sort of allude to is I'm not I'm no
[25:54] sort of allude to is I'm not I'm no
[25:54] sort of allude to is I'm not I'm no stranger to partial autonomy and I kind
[25:56] stranger to partial autonomy and I kind
[25:56] stranger to partial autonomy and I kind of worked on this I think for five years
[25:57] of worked on this I think for five years
[25:57] of worked on this I think for five years at Tesla and this is also a partial
[26:00] at Tesla and this is also a partial
[26:00] at Tesla and this is also a partial autonomy product and shares a lot of the
[26:01] autonomy product and shares a lot of the
[26:01] autonomy product and shares a lot of the features like for example right there in
[26:03] features like for example right there in
[26:03] features like for example right there in the instrument panel is the GUI of the
[26:05] the instrument panel is the GUI of the
[26:05] the instrument panel is the GUI of the autopilot so it's showing me what the
[26:07] autopilot so it's showing me what the
[26:07] autopilot so it's showing me what the what the neural network sees and so on
[26:09] what the neural network sees and so on
[26:09] what the neural network sees and so on and we have the autonomy slider where
[26:10] and we have the autonomy slider where
[26:10] and we have the autonomy slider where over the course of my tenure there we
[26:13] over the course of my tenure there we
[26:13] over the course of my tenure there we did more and more autonomous tasks for
[26:15] did more and more autonomous tasks for
[26:15] did more and more autonomous tasks for the user and maybe the story that I
[26:18] the user and maybe the story that I
[26:18] the user and maybe the story that I wanted to tell very briefly is uh
[26:21] wanted to tell very briefly is uh
[26:21] wanted to tell very briefly is uh actually the first time I drove a
[26:22] actually the first time I drove a
[26:22] actually the first time I drove a self-driving vehicle was in 2013 and I
[26:25] self-driving vehicle was in 2013 and I
[26:25] self-driving vehicle was in 2013 and I had a friend who worked at Whimo and uh
[26:27] had a friend who worked at Whimo and uh
[26:27] had a friend who worked at Whimo and uh he offered to give me a drive around
[26:29] he offered to give me a drive around
[26:29] he offered to give me a drive around Palo Alto. I took this picture using
[26:31] Palo Alto. I took this picture using
[26:31] Palo Alto. I took this picture using Google Glass at the time and many of you
[26:33] Google Glass at the time and many of you
[26:33] Google Glass at the time and many of you are so young that you might not even
[26:35] are so young that you might not even
[26:35] are so young that you might not even know what that is. Uh but uh yeah, this
[26:37] know what that is. Uh but uh yeah, this
[26:37] know what that is. Uh but uh yeah, this was like all the rage at the time. And
[26:39] was like all the rage at the time. And
[26:39] was like all the rage at the time. And we got into this car and we went for
[26:40] we got into this car and we went for
[26:40] we got into this car and we went for about a 30-minute drive around Palo Alto
[26:42] about a 30-minute drive around Palo Alto
[26:42] about a 30-minute drive around Palo Alto highways uh streets and so on. And this
[26:45] highways uh streets and so on. And this
[26:45] highways uh streets and so on. And this drive was perfect. There was zero
[26:46] drive was perfect. There was zero
[26:46] drive was perfect. There was zero interventions and this was 2013 which is
[26:49] interventions and this was 2013 which is
[26:49] interventions and this was 2013 which is now 12 years ago. And it kind of struck
[26:52] now 12 years ago. And it kind of struck
[26:52] now 12 years ago. And it kind of struck me because at the time when I had this
[26:53] me because at the time when I had this
[26:54] me because at the time when I had this perfect drive, this perfect demo, I felt
[26:56] perfect drive, this perfect demo, I felt
[26:56] perfect drive, this perfect demo, I felt like, wow, self-driving is imminent
[26:59] like, wow, self-driving is imminent
[26:59] like, wow, self-driving is imminent because this just worked. This is
[27:00] because this just worked. This is
[27:00] because this just worked. This is incredible. Um, but here we are 12 years
[27:03] incredible. Um, but here we are 12 years
[27:03] incredible. Um, but here we are 12 years later and we are still working on
[27:04] later and we are still working on
[27:04] later and we are still working on autonomy. Um, we are still working on
[27:07] autonomy. Um, we are still working on
[27:07] autonomy. Um, we are still working on driving agents and even now we haven't
[27:09] driving agents and even now we haven't
[27:09] driving agents and even now we haven't actually like really solved the problem.
[27:10] actually like really solved the problem.
[27:10] actually like really solved the problem. like you may see Whimos going around and
[27:12] like you may see Whimos going around and
[27:12] like you may see Whimos going around and they look driverless but you know
[27:14] they look driverless but you know
[27:14] they look driverless but you know there's still a lot of teleoperation and
[27:16] there's still a lot of teleoperation and
[27:16] there's still a lot of teleoperation and a lot of human in the loop of a lot of
[27:18] a lot of human in the loop of a lot of
[27:18] a lot of human in the loop of a lot of this driving so we still haven't even
[27:20] this driving so we still haven't even
[27:20] this driving so we still haven't even like declared success but I think it's
[27:22] like declared success but I think it's
[27:22] like declared success but I think it's definitely like going to succeed at this
[27:24] definitely like going to succeed at this
[27:24] definitely like going to succeed at this point but it just took a long time and
[27:26] point but it just took a long time and
[27:26] point but it just took a long time and so I think like like this is software is
[27:29] so I think like like this is software is
[27:29] so I think like like this is software is really tricky I think in the same way
[27:31] really tricky I think in the same way
[27:31] really tricky I think in the same way that driving is tricky and so when I see
[27:34] that driving is tricky and so when I see
[27:34] that driving is tricky and so when I see things like oh 2025 is the year of
[27:36] things like oh 2025 is the year of
[27:36] things like oh 2025 is the year of agents I get very concerned and I kind
[27:38] agents I get very concerned and I kind
[27:38] agents I get very concerned and I kind of feel like you know this is the decade
[27:41] of feel like you know this is the decade
[27:41] of feel like you know this is the decade of agents and this is going to be quite
[27:44] of agents and this is going to be quite
[27:44] of agents and this is going to be quite some time. We need humans in the loop.
[27:45] some time. We need humans in the loop.
[27:45] some time. We need humans in the loop. We need to do this carefully. This is
[27:47] We need to do this carefully. This is
[27:47] We need to do this carefully. This is software. Let's be serious here. One
[27:51] software. Let's be serious here. One
[27:51] software. Let's be serious here. One more kind of analogy that I always think
[27:52] more kind of analogy that I always think
[27:52] more kind of analogy that I always think through is the Iron Man suit. Uh I think
[27:56] through is the Iron Man suit. Uh I think
[27:56] through is the Iron Man suit. Uh I think this is I always love Iron Man. I think
[27:58] this is I always love Iron Man. I think
[27:58] this is I always love Iron Man. I think it's like so um correct in a bunch of
[28:01] it's like so um correct in a bunch of
[28:01] it's like so um correct in a bunch of ways with respect to technology and how
[28:02] ways with respect to technology and how
[28:02] ways with respect to technology and how it will play out. And what I love about
[28:04] it will play out. And what I love about
[28:04] it will play out. And what I love about the Iron Man suit is that it's both an
[28:05] the Iron Man suit is that it's both an
[28:05] the Iron Man suit is that it's both an augmentation and Tony Stark can drive it
[28:08] augmentation and Tony Stark can drive it
[28:08] augmentation and Tony Stark can drive it and it's also an agent. And in some of
[28:10] and it's also an agent. And in some of
[28:10] and it's also an agent. And in some of the movies, the Iron Man suit is quite
[28:11] the movies, the Iron Man suit is quite
[28:11] the movies, the Iron Man suit is quite autonomous and can fly around and find
[28:13] autonomous and can fly around and find
[28:13] autonomous and can fly around and find Tony and all this kind of stuff. And so
[28:15] Tony and all this kind of stuff. And so
[28:15] Tony and all this kind of stuff. And so this is the autonomy slider is we can be
[28:17] this is the autonomy slider is we can be
[28:17] this is the autonomy slider is we can be we can build augmentations or we can
[28:19] we can build augmentations or we can
[28:19] we can build augmentations or we can build agents and we kind of want to do a
[28:21] build agents and we kind of want to do a
[28:21] build agents and we kind of want to do a bit of both. But at this stage I would
[28:23] bit of both. But at this stage I would
[28:23] bit of both. But at this stage I would say working with fallible LLMs and so
[28:25] say working with fallible LLMs and so
[28:25] say working with fallible LLMs and so on. I would say you know it's less Iron
[28:29] on. I would say you know it's less Iron
[28:29] on. I would say you know it's less Iron Man robots and more Iron Man suits that
[28:31] Man robots and more Iron Man suits that
[28:31] Man robots and more Iron Man suits that you want to build. It's less like
[28:33] you want to build. It's less like
[28:33] you want to build. It's less like building flashy demos of autonomous
[28:35] building flashy demos of autonomous
[28:35] building flashy demos of autonomous agents and more building partial
[28:36] agents and more building partial
[28:36] agents and more building partial autonomy products. And these products
[28:39] autonomy products. And these products
[28:39] autonomy products. And these products have custom gueies and UIUX. And we're
[28:41] have custom gueies and UIUX. And we're
[28:41] have custom gueies and UIUX. And we're trying to um and this is done so that
[28:43] trying to um and this is done so that
[28:43] trying to um and this is done so that the generation verification loop of the
[28:45] the generation verification loop of the
[28:45] the generation verification loop of the human is very very fast. But we are not
[28:48] human is very very fast. But we are not
[28:48] human is very very fast. But we are not losing the sight of the fact that it is
[28:49] losing the sight of the fact that it is
[28:49] losing the sight of the fact that it is in principle possible to automate this
[28:51] in principle possible to automate this
[28:51] in principle possible to automate this work. And there should be an autonomy
[28:52] work. And there should be an autonomy
[28:52] work. And there should be an autonomy slider in your product. And you should
[28:54] slider in your product. And you should
[28:54] slider in your product. And you should be thinking about how you can slide that
[28:55] be thinking about how you can slide that
[28:55] be thinking about how you can slide that autonomy slider and make your product uh
[28:58] autonomy slider and make your product uh
[28:58] autonomy slider and make your product uh sort of um more autonomous over time.
[29:01] sort of um more autonomous over time.
[29:01] sort of um more autonomous over time. But this is kind of how I think there's
[29:02] But this is kind of how I think there's
[29:02] But this is kind of how I think there's lots of opportunities in these kinds of
[29:04] lots of opportunities in these kinds of
[29:04] lots of opportunities in these kinds of products. I want to now switch gears a
[29:06] products. I want to now switch gears a
[29:06] products. I want to now switch gears a little bit and talk about one other
[29:08] little bit and talk about one other
[29:08] little bit and talk about one other dimension that I think is very unique.
[29:09] dimension that I think is very unique.
[29:09] dimension that I think is very unique. Not only is there a new type of
[29:11] Not only is there a new type of
[29:11] Not only is there a new type of programming language that allows for
[29:12] programming language that allows for
[29:12] programming language that allows for autonomy in software but also as I
[29:15] autonomy in software but also as I
[29:15] autonomy in software but also as I mentioned it's programmed in English
[29:16] mentioned it's programmed in English
[29:16] mentioned it's programmed in English which is this natural interface and
[29:19] which is this natural interface and
[29:19] which is this natural interface and suddenly everyone is a programmer
[29:20] suddenly everyone is a programmer
[29:20] suddenly everyone is a programmer because everyone speaks natural language
[29:22] because everyone speaks natural language
[29:22] because everyone speaks natural language like English. So this is extremely
[29:24] like English. So this is extremely
[29:24] like English. So this is extremely bullish and very interesting to me and
[29:26] bullish and very interesting to me and
[29:26] bullish and very interesting to me and also completely unprecedented. I would
[29:27] also completely unprecedented. I would
[29:28] also completely unprecedented. I would say it it used to be the case that you
[29:29] say it it used to be the case that you
[29:29] say it it used to be the case that you need to spend five to 10 years studying
[29:31] need to spend five to 10 years studying
[29:31] need to spend five to 10 years studying something to be able to do something in
[29:32] something to be able to do something in
[29:32] something to be able to do something in software. this is not the case anymore.
[29:35] software. this is not the case anymore.
[29:35] software. this is not the case anymore. So, I don't know if by any chance anyone
[29:37] So, I don't know if by any chance anyone
[29:37] So, I don't know if by any chance anyone has heard of vibe coding.
[29:40] has heard of vibe coding.
[29:40] has heard of vibe coding. Uh, this this is the tweet that kind of
[29:42] Uh, this this is the tweet that kind of
[29:42] Uh, this this is the tweet that kind of like introduced this, but I'm told that
[29:44] like introduced this, but I'm told that
[29:44] like introduced this, but I'm told that this is now like a major meme. Um, fun
[29:46] this is now like a major meme. Um, fun
[29:46] this is now like a major meme. Um, fun story about this is that I've been on
[29:49] story about this is that I've been on
[29:49] story about this is that I've been on Twitter for like 15 years or something
[29:51] Twitter for like 15 years or something
[29:51] Twitter for like 15 years or something like that at this point and I still have
[29:53] like that at this point and I still have
[29:53] like that at this point and I still have no clue which tweet will become viral
[29:56] no clue which tweet will become viral
[29:56] no clue which tweet will become viral and which tweet like fizzles and no one
[29:57] and which tweet like fizzles and no one
[29:58] and which tweet like fizzles and no one cares. And I thought that this tweet was
[30:00] cares. And I thought that this tweet was
[30:00] cares. And I thought that this tweet was going to be the latter. I don't know. It
[30:01] going to be the latter. I don't know. It
[30:01] going to be the latter. I don't know. It was just like a shower of thoughts. But
[30:03] was just like a shower of thoughts. But
[30:03] was just like a shower of thoughts. But this became like a total meme and I
[30:05] this became like a total meme and I
[30:05] this became like a total meme and I really just can't tell. But I guess like
[30:06] really just can't tell. But I guess like
[30:06] really just can't tell. But I guess like it struck a chord and it gave a name to
[30:08] it struck a chord and it gave a name to
[30:08] it struck a chord and it gave a name to something that everyone was feeling but
[30:10] something that everyone was feeling but
[30:10] something that everyone was feeling but couldn't quite say in words. So now
[30:13] couldn't quite say in words. So now
[30:13] couldn't quite say in words. So now there's a Wikipedia page and everything.
[30:17] there's a Wikipedia page and everything.
[30:17] there's a Wikipedia page and everything. This is like
[30:18] This is like
[30:18] This is like [Applause]
[30:25] [Applause]
[30:25] [Applause] yeah this is like a major contribution
[30:27] yeah this is like a major contribution
[30:27] yeah this is like a major contribution now or something like that. So,
[30:30] now or something like that. So,
[30:30] now or something like that. So, um, so Tom Wolf from HuggingFace shared
[30:32] um, so Tom Wolf from HuggingFace shared
[30:32] um, so Tom Wolf from HuggingFace shared this beautiful video that I really love.
[30:34] this beautiful video that I really love.
[30:34] this beautiful video that I really love. Um,
[30:37] Um,
[30:37] Um, these are kids vibe coding.
[30:42] And I find that this is such a wholesome
[30:44] And I find that this is such a wholesome
[30:44] And I find that this is such a wholesome video. Like, I love this video. Like,
[30:46] video. Like, I love this video. Like,
[30:46] video. Like, I love this video. Like, how can you look at this video and feel
[30:48] how can you look at this video and feel
[30:48] how can you look at this video and feel bad about the future? The future is
[30:49] bad about the future? The future is
[30:49] bad about the future? The future is great.
[30:52] great.
[30:52] great. I think this will end up being like a
[30:53] I think this will end up being like a
[30:53] I think this will end up being like a gateway drug to software development.
[30:56] gateway drug to software development.
[30:56] gateway drug to software development. Um, I'm not a doomer about the future of
[30:59] Um, I'm not a doomer about the future of
[30:59] Um, I'm not a doomer about the future of the generation and I think yeah, I love
[31:02] the generation and I think yeah, I love
[31:02] the generation and I think yeah, I love this video. So, I tried by coding a
[31:04] this video. So, I tried by coding a
[31:04] this video. So, I tried by coding a little bit uh as well because it's so
[31:07] little bit uh as well because it's so
[31:07] little bit uh as well because it's so fun. Uh, so bike coding is so great when
[31:09] fun. Uh, so bike coding is so great when
[31:09] fun. Uh, so bike coding is so great when you want to build something super duper
[31:10] you want to build something super duper
[31:10] you want to build something super duper custom that doesn't appear to exist and
[31:12] custom that doesn't appear to exist and
[31:12] custom that doesn't appear to exist and you just want to wing it because it's a
[31:13] you just want to wing it because it's a
[31:13] you just want to wing it because it's a Saturday or something like that. So, I
[31:15] Saturday or something like that. So, I
[31:15] Saturday or something like that. So, I built this uh iOS app and I don't I
[31:18] built this uh iOS app and I don't I
[31:18] built this uh iOS app and I don't I can't actually program in Swift, but I
[31:20] can't actually program in Swift, but I
[31:20] can't actually program in Swift, but I was really shocked that I was able to
[31:21] was really shocked that I was able to
[31:21] was really shocked that I was able to build like a super basic app and I'm not
[31:23] build like a super basic app and I'm not
[31:23] build like a super basic app and I'm not going to explain it. It's really uh
[31:24] going to explain it. It's really uh
[31:24] going to explain it. It's really uh dumb, but uh I kind of like this was
[31:27] dumb, but uh I kind of like this was
[31:27] dumb, but uh I kind of like this was just like a day of work and this was
[31:28] just like a day of work and this was
[31:28] just like a day of work and this was running on my phone like later that day
[31:30] running on my phone like later that day
[31:30] running on my phone like later that day and I was like, "Wow, this is amazing."
[31:32] and I was like, "Wow, this is amazing."
[31:32] and I was like, "Wow, this is amazing." I didn't have to like read through Swift
[31:33] I didn't have to like read through Swift
[31:33] I didn't have to like read through Swift for like five days or something like
[31:35] for like five days or something like
[31:35] for like five days or something like that to like get started. I also
[31:38] that to like get started. I also
[31:38] that to like get started. I also vipcoded this app called Menu Genen. And
[31:40] vipcoded this app called Menu Genen. And
[31:40] vipcoded this app called Menu Genen. And this is live. You can try it in
[31:41] this is live. You can try it in
[31:41] this is live. You can try it in menu.app. And I basically had this
[31:44] menu.app. And I basically had this
[31:44] menu.app. And I basically had this problem where I show up at a restaurant,
[31:45] problem where I show up at a restaurant,
[31:45] problem where I show up at a restaurant, I read through the menu, and I have no
[31:46] I read through the menu, and I have no
[31:46] I read through the menu, and I have no idea what any of the things are. And I
[31:48] idea what any of the things are. And I
[31:48] idea what any of the things are. And I need pictures. So this doesn't exist. So
[31:51] need pictures. So this doesn't exist. So
[31:51] need pictures. So this doesn't exist. So I was like, "Hey, I'm going to bite code
[31:52] I was like, "Hey, I'm going to bite code
[31:52] I was like, "Hey, I'm going to bite code it." So, um, this is what it looks like.
[31:55] it." So, um, this is what it looks like.
[31:55] it." So, um, this is what it looks like. You go to menu.app,
[31:58] You go to menu.app,
[31:58] You go to menu.app, um, and, uh, you take a picture of a of
[32:01] um, and, uh, you take a picture of a of
[32:01] um, and, uh, you take a picture of a of a menu and then menu generates the
[32:03] a menu and then menu generates the
[32:03] a menu and then menu generates the images and everyone gets $5 in credits
[32:06] images and everyone gets $5 in credits
[32:06] images and everyone gets $5 in credits for free when you sign up. And
[32:07] for free when you sign up. And
[32:08] for free when you sign up. And therefore, this is a major cost center
[32:10] therefore, this is a major cost center
[32:10] therefore, this is a major cost center in my life. So, this is a negative
[32:13] in my life. So, this is a negative
[32:13] in my life. So, this is a negative negative uh, revenue app for me right
[32:16] negative uh, revenue app for me right
[32:16] negative uh, revenue app for me right now.
[32:17] now.
[32:17] now. I've lost a huge amount of money on
[32:19] I've lost a huge amount of money on
[32:19] I've lost a huge amount of money on menu.
[32:21] menu.
[32:21] menu. Okay. But the fascinating thing about
[32:23] Okay. But the fascinating thing about
[32:23] Okay. But the fascinating thing about menu genen for me is that the code of
[32:28] menu genen for me is that the code of
[32:28] menu genen for me is that the code of the v the vite coding part the code was
[32:30] the v the vite coding part the code was
[32:30] the v the vite coding part the code was actually the easy part of v of v coding
[32:32] actually the easy part of v of v coding
[32:32] actually the easy part of v of v coding menu and most of it actually was when I
[32:35] menu and most of it actually was when I
[32:35] menu and most of it actually was when I tried to make it real so that you can
[32:36] tried to make it real so that you can
[32:36] tried to make it real so that you can actually have authentication and
[32:37] actually have authentication and
[32:37] actually have authentication and payments and the domain name and averal
[32:39] payments and the domain name and averal
[32:39] payments and the domain name and averal deployment. This was really hard and all
[32:41] deployment. This was really hard and all
[32:41] deployment. This was really hard and all of this was not code. All of this devops
[32:44] of this was not code. All of this devops
[32:44] of this was not code. All of this devops stuff was in me in the browser clicking
[32:47] stuff was in me in the browser clicking
[32:47] stuff was in me in the browser clicking stuff and this was extreme slo and took
[32:49] stuff and this was extreme slo and took
[32:49] stuff and this was extreme slo and took another week. So it was really
[32:51] another week. So it was really
[32:51] another week. So it was really fascinating that I had the menu genen um
[32:54] fascinating that I had the menu genen um
[32:54] fascinating that I had the menu genen um basically demo working on my laptop in a
[32:57] basically demo working on my laptop in a
[32:57] basically demo working on my laptop in a few hours and then it took me a week
[32:59] few hours and then it took me a week
[32:59] few hours and then it took me a week because I was trying to make it real and
[33:01] because I was trying to make it real and
[33:01] because I was trying to make it real and the reason for this is this was just
[33:02] the reason for this is this was just
[33:02] the reason for this is this was just really annoying. Um, so for example, if
[33:05] really annoying. Um, so for example, if
[33:05] really annoying. Um, so for example, if you try to add Google login to your web
[33:07] you try to add Google login to your web
[33:07] you try to add Google login to your web page, I know this is very small, but
[33:09] page, I know this is very small, but
[33:09] page, I know this is very small, but just a huge amount of instructions of
[33:11] just a huge amount of instructions of
[33:11] just a huge amount of instructions of this clerk library telling me how to
[33:13] this clerk library telling me how to
[33:13] this clerk library telling me how to integrate this. And this is crazy. Like
[33:15] integrate this. And this is crazy. Like
[33:15] integrate this. And this is crazy. Like it's telling me go to this URL, click on
[33:17] it's telling me go to this URL, click on
[33:17] it's telling me go to this URL, click on this dropdown, choose this, go to this,
[33:19] this dropdown, choose this, go to this,
[33:19] this dropdown, choose this, go to this, and click on that. And it's like telling
[33:21] and click on that. And it's like telling
[33:21] and click on that. And it's like telling me what to do. Like a computer is
[33:22] me what to do. Like a computer is
[33:22] me what to do. Like a computer is telling me the actions I should be
[33:24] telling me the actions I should be
[33:24] telling me the actions I should be taking. Like you do it. Why am I doing
[33:26] taking. Like you do it. Why am I doing
[33:26] taking. Like you do it. Why am I doing this?
[33:28] this?
[33:28] this? What the hell?
[33:31] What the hell?
[33:31] What the hell? I had to follow all these instructions.
[33:33] I had to follow all these instructions.
[33:33] I had to follow all these instructions. This was crazy. So I think the last part
[33:36] This was crazy. So I think the last part
[33:36] This was crazy. So I think the last part of my talk therefore focuses on can we
[33:39] of my talk therefore focuses on can we
[33:39] of my talk therefore focuses on can we just build for agents? I don't want to
[33:41] just build for agents? I don't want to
[33:41] just build for agents? I don't want to do this work. Can agents do this? Thank
[33:44] do this work. Can agents do this? Thank
[33:44] do this work. Can agents do this? Thank you.
[33:46] you.
[33:46] you. Okay. So roughly speaking, I think
[33:48] Okay. So roughly speaking, I think
[33:48] Okay. So roughly speaking, I think there's a new category of consumer and
[33:50] there's a new category of consumer and
[33:50] there's a new category of consumer and manipulator of digital information. It
[33:53] manipulator of digital information. It
[33:53] manipulator of digital information. It used to be just humans through GUIs or
[33:55] used to be just humans through GUIs or
[33:55] used to be just humans through GUIs or computers through APIs. And now we have
[33:57] computers through APIs. And now we have
[33:57] computers through APIs. And now we have a completely new thing and agents are
[34:00] a completely new thing and agents are
[34:00] a completely new thing and agents are they're computers but they are humanlike
[34:02] they're computers but they are humanlike
[34:02] they're computers but they are humanlike kind of right they're people spirits
[34:04] kind of right they're people spirits
[34:04] kind of right they're people spirits there's people spirits on the internet
[34:05] there's people spirits on the internet
[34:05] there's people spirits on the internet and they need to interact with our
[34:06] and they need to interact with our
[34:06] and they need to interact with our software infrastructure like can we
[34:08] software infrastructure like can we
[34:08] software infrastructure like can we build for them it's a new thing so as an
[34:10] build for them it's a new thing so as an
[34:10] build for them it's a new thing so as an example you can have robots.txt on your
[34:12] example you can have robots.txt on your
[34:12] example you can have robots.txt on your domain and you can instruct uh or like
[34:15] domain and you can instruct uh or like
[34:15] domain and you can instruct uh or like advise I suppose um uh web crawlers on
[34:18] advise I suppose um uh web crawlers on
[34:18] advise I suppose um uh web crawlers on how to behave on your website in the
[34:19] how to behave on your website in the
[34:19] how to behave on your website in the same way you can have maybe lm.txt txt
[34:21] same way you can have maybe lm.txt txt
[34:21] same way you can have maybe lm.txt txt file which is just a simple markdown
[34:23] file which is just a simple markdown
[34:23] file which is just a simple markdown that's telling LLMs what this domain is
[34:25] that's telling LLMs what this domain is
[34:25] that's telling LLMs what this domain is about and this is very readable to a to
[34:28] about and this is very readable to a to
[34:28] about and this is very readable to a to an LLM. If it had to instead get the
[34:30] an LLM. If it had to instead get the
[34:30] an LLM. If it had to instead get the HTML of your web page and try to parse
[34:32] HTML of your web page and try to parse
[34:32] HTML of your web page and try to parse it, this is very errorprone and
[34:33] it, this is very errorprone and
[34:33] it, this is very errorprone and difficult and will screw it up and it's
[34:35] difficult and will screw it up and it's
[34:35] difficult and will screw it up and it's not going to work. So we can just
[34:36] not going to work. So we can just
[34:36] not going to work. So we can just directly speak to the LLM. It's worth
[34:38] directly speak to the LLM. It's worth
[34:38] directly speak to the LLM. It's worth it. Um a huge amount of documentation is
[34:41] it. Um a huge amount of documentation is
[34:41] it. Um a huge amount of documentation is currently written for people. So you
[34:42] currently written for people. So you
[34:42] currently written for people. So you will see things like lists and bold and
[34:45] will see things like lists and bold and
[34:45] will see things like lists and bold and pictures and this is not directly
[34:47] pictures and this is not directly
[34:47] pictures and this is not directly accessible by an LLM. So I see some of
[34:51] accessible by an LLM. So I see some of
[34:51] accessible by an LLM. So I see some of the services now are transitioning a lot
[34:52] the services now are transitioning a lot
[34:52] the services now are transitioning a lot of the their docs to be specifically for
[34:54] of the their docs to be specifically for
[34:54] of the their docs to be specifically for LLMs. So Versell and Stripe as an
[34:57] LLMs. So Versell and Stripe as an
[34:57] LLMs. So Versell and Stripe as an example are early movers here but there
[34:59] example are early movers here but there
[34:59] example are early movers here but there are a few more that I've seen already
[35:01] are a few more that I've seen already
[35:01] are a few more that I've seen already and they offer their documentation in
[35:04] and they offer their documentation in
[35:04] and they offer their documentation in markdown. Markdown is super easy for LMS
[35:06] markdown. Markdown is super easy for LMS
[35:06] markdown. Markdown is super easy for LMS to understand. This is great. Um maybe
[35:10] to understand. This is great. Um maybe
[35:10] to understand. This is great. Um maybe one simple example from from uh my
[35:12] one simple example from from uh my
[35:12] one simple example from from uh my experience as well. Maybe some of you
[35:14] experience as well. Maybe some of you
[35:14] experience as well. Maybe some of you know three blue one brown. He makes
[35:15] know three blue one brown. He makes
[35:15] know three blue one brown. He makes beautiful animation videos on YouTube.
[35:19] beautiful animation videos on YouTube.
[35:19] beautiful animation videos on YouTube. [Applause]
[35:23] Yeah, I love this library. So that he
[35:25] Yeah, I love this library. So that he
[35:25] Yeah, I love this library. So that he wrote uh Manon and I wanted to make my
[35:27] wrote uh Manon and I wanted to make my
[35:27] wrote uh Manon and I wanted to make my own and uh there's extensive
[35:30] own and uh there's extensive
[35:30] own and uh there's extensive documentations on how to use manon and
[35:32] documentations on how to use manon and
[35:32] documentations on how to use manon and so I didn't want to actually read
[35:33] so I didn't want to actually read
[35:34] so I didn't want to actually read through it. So I copy pasted the whole
[35:35] through it. So I copy pasted the whole
[35:35] through it. So I copy pasted the whole thing to an LLM and I described what I
[35:37] thing to an LLM and I described what I
[35:37] thing to an LLM and I described what I wanted and it just worked out of the box
[35:39] wanted and it just worked out of the box
[35:39] wanted and it just worked out of the box like LLM just bcoded me an animation
[35:41] like LLM just bcoded me an animation
[35:41] like LLM just bcoded me an animation exactly what I wanted and I was like wow
[35:43] exactly what I wanted and I was like wow
[35:43] exactly what I wanted and I was like wow this is amazing. So if we can make docs
[35:45] this is amazing. So if we can make docs
[35:45] this is amazing. So if we can make docs legible to LLMs, it's going to unlock a
[35:48] legible to LLMs, it's going to unlock a
[35:48] legible to LLMs, it's going to unlock a huge amount of um kind of use and um I
[35:51] huge amount of um kind of use and um I
[35:51] huge amount of um kind of use and um I think this is wonderful and should
[35:52] think this is wonderful and should
[35:52] think this is wonderful and should should happen more. The other thing I
[35:55] should happen more. The other thing I
[35:55] should happen more. The other thing I wanted to point out is that you do
[35:56] wanted to point out is that you do
[35:56] wanted to point out is that you do unfortunately have to it's not just
[35:57] unfortunately have to it's not just
[35:57] unfortunately have to it's not just about taking your docs and making them
[35:58] about taking your docs and making them
[35:58] about taking your docs and making them appear in markdown. That's the easy
[36:00] appear in markdown. That's the easy
[36:00] appear in markdown. That's the easy part. We actually have to change the
[36:01] part. We actually have to change the
[36:01] part. We actually have to change the docs because anytime your docs say click
[36:04] docs because anytime your docs say click
[36:04] docs because anytime your docs say click this is bad. An LLM will not be able to
[36:06] this is bad. An LLM will not be able to
[36:06] this is bad. An LLM will not be able to natively take this action right now. So,
[36:09] natively take this action right now. So,
[36:09] natively take this action right now. So, Verscell, for example, is replacing
[36:11] Verscell, for example, is replacing
[36:11] Verscell, for example, is replacing every occurrence of click with an
[36:13] every occurrence of click with an
[36:13] every occurrence of click with an equivalent curl command that your LM
[36:15] equivalent curl command that your LM
[36:15] equivalent curl command that your LM agent could take on your behalf. Um, and
[36:18] agent could take on your behalf. Um, and
[36:18] agent could take on your behalf. Um, and so I think this is very interesting. And
[36:19] so I think this is very interesting. And
[36:19] so I think this is very interesting. And then, of course, there's a model context
[36:21] then, of course, there's a model context
[36:21] then, of course, there's a model context protocol from Enthropic. And this is
[36:23] protocol from Enthropic. And this is
[36:23] protocol from Enthropic. And this is also another way, it's a protocol of
[36:24] also another way, it's a protocol of
[36:24] also another way, it's a protocol of speaking directly to agents as this new
[36:26] speaking directly to agents as this new
[36:26] speaking directly to agents as this new consumer and manipulator of digital
[36:28] consumer and manipulator of digital
[36:28] consumer and manipulator of digital information. So, I'm very bullish on
[36:29] information. So, I'm very bullish on
[36:29] information. So, I'm very bullish on these ideas. The other thing I really
[36:31] these ideas. The other thing I really
[36:31] these ideas. The other thing I really like is a number of little tools here
[36:33] like is a number of little tools here
[36:33] like is a number of little tools here and there that are helping ingest data
[36:36] and there that are helping ingest data
[36:36] and there that are helping ingest data that in like very LLM friendly formats.
[36:38] that in like very LLM friendly formats.
[36:38] that in like very LLM friendly formats. So for example, when I go to a GitHub
[36:40] So for example, when I go to a GitHub
[36:40] So for example, when I go to a GitHub repo like my nanoGPT repo, I can't feed
[36:42] repo like my nanoGPT repo, I can't feed
[36:42] repo like my nanoGPT repo, I can't feed this to an LLM and ask questions about
[36:44] this to an LLM and ask questions about
[36:44] this to an LLM and ask questions about it uh because it's you know this is a
[36:46] it uh because it's you know this is a
[36:46] it uh because it's you know this is a human interface on GitHub. So when you
[36:48] human interface on GitHub. So when you
[36:48] human interface on GitHub. So when you just change the URL from GitHub to get
[36:50] just change the URL from GitHub to get
[36:50] just change the URL from GitHub to get ingest then uh this will actually
[36:52] ingest then uh this will actually
[36:52] ingest then uh this will actually concatenate all the files into a single
[36:54] concatenate all the files into a single
[36:54] concatenate all the files into a single giant text and it will create a
[36:55] giant text and it will create a
[36:55] giant text and it will create a directory structure etc. And this is
[36:57] directory structure etc. And this is
[36:57] directory structure etc. And this is ready to be copy pasted into your
[36:59] ready to be copy pasted into your
[36:59] ready to be copy pasted into your favorite LLM and you can do stuff. Maybe
[37:01] favorite LLM and you can do stuff. Maybe
[37:01] favorite LLM and you can do stuff. Maybe even more dramatic example of this is
[37:03] even more dramatic example of this is
[37:03] even more dramatic example of this is deep wiki where it's not just the raw
[37:05] deep wiki where it's not just the raw
[37:05] deep wiki where it's not just the raw content of these files. uh this is from
[37:08] content of these files. uh this is from
[37:08] content of these files. uh this is from Devon but also like they have Devon
[37:10] Devon but also like they have Devon
[37:10] Devon but also like they have Devon basically do analysis of the GitHub repo
[37:12] basically do analysis of the GitHub repo
[37:12] basically do analysis of the GitHub repo and Devon basically builds up a whole
[37:14] and Devon basically builds up a whole
[37:14] and Devon basically builds up a whole docs uh pages just for your repo and you
[37:17] docs uh pages just for your repo and you
[37:18] docs uh pages just for your repo and you can imagine that this is even more
[37:19] can imagine that this is even more
[37:19] can imagine that this is even more helpful to copy paste into your LLM. So
[37:22] helpful to copy paste into your LLM. So
[37:22] helpful to copy paste into your LLM. So I love all the little tools that
[37:23] I love all the little tools that
[37:23] I love all the little tools that basically where you just change the URL
[37:24] basically where you just change the URL
[37:24] basically where you just change the URL and it makes something accessible to an
[37:26] and it makes something accessible to an
[37:26] and it makes something accessible to an LLM. So this is all well and great and u
[37:29] LLM. So this is all well and great and u
[37:29] LLM. So this is all well and great and u I think there should be a lot more of
[37:30] I think there should be a lot more of
[37:30] I think there should be a lot more of it. One more note I wanted to make is
[37:32] it. One more note I wanted to make is
[37:32] it. One more note I wanted to make is that it is absolutely possible that in
[37:35] that it is absolutely possible that in
[37:35] that it is absolutely possible that in the future LLMs will be able to this is
[37:37] the future LLMs will be able to this is
[37:38] the future LLMs will be able to this is not even future this is today they'll be
[37:39] not even future this is today they'll be
[37:39] not even future this is today they'll be able to go around and they'll be able to
[37:40] able to go around and they'll be able to
[37:40] able to go around and they'll be able to click stuff and so on but I still think
[37:42] click stuff and so on but I still think
[37:42] click stuff and so on but I still think it's very worth u basically meeting LLM
[37:46] it's very worth u basically meeting LLM
[37:46] it's very worth u basically meeting LLM halfway LLM's halfway and making it
[37:48] halfway LLM's halfway and making it
[37:48] halfway LLM's halfway and making it easier for them to access all this
[37:49] easier for them to access all this
[37:49] easier for them to access all this information uh because this is still
[37:51] information uh because this is still
[37:51] information uh because this is still fairly expensive I would say to use and
[37:54] fairly expensive I would say to use and
[37:54] fairly expensive I would say to use and uh a lot more difficult and so I do
[37:56] uh a lot more difficult and so I do
[37:56] uh a lot more difficult and so I do think that lots of software there will
[37:58] think that lots of software there will
[37:58] think that lots of software there will be a long tail where it won't like adapt
[38:00] be a long tail where it won't like adapt
[38:00] be a long tail where it won't like adapt apps because these are not like live
[38:02] apps because these are not like live
[38:02] apps because these are not like live player sort of repositories or digital
[38:04] player sort of repositories or digital
[38:04] player sort of repositories or digital infrastructure and we will need these
[38:06] infrastructure and we will need these
[38:06] infrastructure and we will need these tools. Uh but I think for everyone else
[38:08] tools. Uh but I think for everyone else
[38:08] tools. Uh but I think for everyone else I think it's very worth kind of like
[38:09] I think it's very worth kind of like
[38:09] I think it's very worth kind of like meeting in some middle point. So I'm
[38:11] meeting in some middle point. So I'm
[38:11] meeting in some middle point. So I'm bullish on both if that makes sense.
[38:14] bullish on both if that makes sense.
[38:14] bullish on both if that makes sense. So in summary, what an amazing time to
[38:17] So in summary, what an amazing time to
[38:17] So in summary, what an amazing time to get into the industry. We need to
[38:18] get into the industry. We need to
[38:18] get into the industry. We need to rewrite a ton of code. A ton of code
[38:20] rewrite a ton of code. A ton of code
[38:20] rewrite a ton of code. A ton of code will be written by professionals and by
[38:23] will be written by professionals and by
[38:23] will be written by professionals and by coders. These LLMs are kind of like
[38:25] coders. These LLMs are kind of like
[38:25] coders. These LLMs are kind of like utilities, kind of like fabs, but
[38:27] utilities, kind of like fabs, but
[38:27] utilities, kind of like fabs, but they're kind of especially like
[38:28] they're kind of especially like
[38:28] they're kind of especially like operating systems. But it's so early.
[38:30] operating systems. But it's so early.
[38:30] operating systems. But it's so early. It's like 1960s of operating systems and
[38:34] It's like 1960s of operating systems and
[38:34] It's like 1960s of operating systems and uh and I think a lot of the analogies
[38:36] uh and I think a lot of the analogies
[38:36] uh and I think a lot of the analogies cross over. Um and these LMS are kind of
[38:38] cross over. Um and these LMS are kind of
[38:38] cross over. Um and these LMS are kind of like these fallible uh you know people
[38:41] like these fallible uh you know people
[38:41] like these fallible uh you know people spirits that we have to learn to work
[38:43] spirits that we have to learn to work
[38:43] spirits that we have to learn to work with. And in order to do that properly,
[38:45] with. And in order to do that properly,
[38:45] with. And in order to do that properly, we need to adjust our infrastructure
[38:47] we need to adjust our infrastructure
[38:47] we need to adjust our infrastructure towards it. So when you're building
[38:48] towards it. So when you're building
[38:48] towards it. So when you're building these LLM apps, I describe some of the
[38:50] these LLM apps, I describe some of the
[38:50] these LLM apps, I describe some of the ways of working effectively with these
[38:52] ways of working effectively with these
[38:52] ways of working effectively with these LLMs and some of the tools that make
[38:54] LLMs and some of the tools that make
[38:54] LLMs and some of the tools that make that uh kind of possible and how you can
[38:57] that uh kind of possible and how you can
[38:57] that uh kind of possible and how you can spin this loop very very quickly and
[38:59] spin this loop very very quickly and
[38:59] spin this loop very very quickly and basically create partial tunneling
[39:00] basically create partial tunneling
[39:00] basically create partial tunneling products and then um yeah, a lot of code
[39:03] products and then um yeah, a lot of code
[39:03] products and then um yeah, a lot of code has to also be written for the agents
[39:04] has to also be written for the agents
[39:04] has to also be written for the agents more directly. But in any case, going
[39:07] more directly. But in any case, going
[39:07] more directly. But in any case, going back to the Iron Man suit analogy, I
[39:09] back to the Iron Man suit analogy, I
[39:09] back to the Iron Man suit analogy, I think what we'll see over the next
[39:10] think what we'll see over the next
[39:10] think what we'll see over the next decade roughly is we're going to take
[39:12] decade roughly is we're going to take
[39:12] decade roughly is we're going to take the slider from left to right. And I'm
[39:15] the slider from left to right. And I'm
[39:15] the slider from left to right. And I'm very interesting. It's going to be very
[39:17] very interesting. It's going to be very
[39:17] very interesting. It's going to be very interesting to see what that looks like.
[39:19] interesting to see what that looks like.
[39:19] interesting to see what that looks like. And I can't wait to build it with all of
[39:21] And I can't wait to build it with all of
[39:21] And I can't wait to build it with all of you. Thank you.


## Quality Analysis

- **Total Lines:** 2273
- **Unique Lines:** 2273
- **Duplicate Lines:** 0
- **Quality Score:** 100.0%

### ✅ High Quality Transcript

No duplicate lines detected.



## MCP Resource Usage

This transcript can be used as an MCP resource:

### Resource URI
```
transcript://LCEmiRjPEtQ
```

### Programmatic Access
```python
# In your MCP server
async def get_transcript(video_id: str):
    return await load_transcript_resource(video_id)
```

### Use Cases
- **Content Analysis:** Analyze themes, topics, and sentiment
- **Quote Extraction:** Find specific quotes or statements  
- **Study Notes:** Generate structured educational notes
- **Search & Discovery:** Full-text search within video content
- **Summarization:** Create abstracts and key points
- **Fact Checking:** Verify claims and statements

---

*Generated by YouTube to MCP Resource Tool v1.0*  
*For more information: https://github.com/your-repo/mcp-youtube-transcript*
