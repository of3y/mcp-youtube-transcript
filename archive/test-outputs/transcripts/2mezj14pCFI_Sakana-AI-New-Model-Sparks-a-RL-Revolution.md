# Sakana AI New Model Sparks a RL Revolution

## Video Information

- **Video ID:** `2mezj14pCFI`
- **URL:** https://www.youtube.com/watch?v=2mezj14pCFI
- **Title:** Sakana AI New Model Sparks a RL Revolution
- **Channel:** Wes Roth
- **Duration:** 17:45 (1065 seconds)
- **Upload Date:** 20250624
- **View Count:** 15,976 views

## Transcript Metadata

- **Extraction Method:** yt-dlp
- **Language:** en
- **Line Count:** 913
- **Generated:** 2025-06-24 13:04:36

## Available Languages

N/A

## Plain Text Script

So, Sakana AI is back. They're the people behind the Darwin Goal machine, a people behind the Darwin Goal machine, a self-improving coding agent.

They also self-improving coding agent. They also created the first AI that had a machine learning scientific paper that passed peer review.

And they're back with yet peer review. And they're back with yet another open-source project plus a another open-source project plus a research paper published, the research paper published, the implications of which seem potentially implications of which seem potentially revolutionary.

So, RL or reinforcement revolutionary. So, RL or reinforcement learning is where we attempt to teach learning is where we attempt to teach these AIs to do something.

And when they do well, we give them a reward. They get better at math or coding and we give them a virtual high five to let them know that they're getting better, that they're getting closer.

Basically, we say, "Whatever you've been doing, do more of that." We can also have negative reinforcement where we panalyze some reinforcement where we panalyze some actions or outcomes that tend to not to lead to the thing that we want them to do. For example, you might recall that game engine, that neural network that was able to basically replicate the game of Doom, right?

So, it played the game of Doom in real time, but without a single piece of code. It wasn't software.

It was a neural network kind of just dreaming it up into life as it went along. In order to get data for the game, they actually trained up a bunch of little AI agents that played Doom.

To do that, they used reinforcement learning RL to teach them to play Doom. learning RL to teach them to play Doom.

And here's the reward function that And here's the reward function that they've used. So, if the player got hit, that would be negative 100 points.

Its dying would be 5,000 points. hitting dying would be 5,000 points.

hitting enemies was worth 300 positive points, enemies was worth 300 positive points, right? So, a virtual high five, like right?

So, a virtual high five, like good job. Enemy kill a,000 points.

And various other things that improved their various other things that improved their gameplay or progressed the game forward gameplay or progressed the game forward also gave it points. And the AI went out there, played Doom, and tried to maximize the amount of points it would maximize the amount of points it would get by, you know, progressing the game get by, you know, progressing the game forward, shooting enemies, etc., while forward, shooting enemies, etc., while at the same time trying to avoid getting hit and especially avoid dying.

This paper flips this whole idea on its head just a little bit. Here they introduce the reinforcement learned teacher.

So we the reinforcement learned teacher. So we train a teacher model to generate train a teacher model to generate explanations from question answer pairs.

So this model is given a question and it knows the correct answer. It's not knows the correct answer.

It's not trying to figure out the correct answer. It already knows it and its goal is to output a great explanation for how to output a great explanation for how to arrive at that answer.

So this teacher model is optimized to improve a student model's understanding. With most RL training, the model we're training is usually the student, at least for usually the student, at least for reinforcement learning RL, right?

So, reinforcement learning RL, right? So, we're sort of giving it positive rewards we're sort of giving it positive rewards to the student for producing the correct to the student for producing the correct answers.

Similar to school in college, the student is the one that's being graded. If a student does poorly, we say that's a bad student.

If they do well, we say that's a good student. But what if we rather graded the teacher?

If the teacher taught well and the students teacher taught well and the students score improved, that's a good teacher. If the teacher through whatever lectures or solutions or whatever way choose to taught, if it decreased the scores of the student, then we say that's a bad the student, then we say that's a bad teacher.

So this model rather than solving problems from scratch, the teacher is rewarded based on how effectively its explanations help the student recover correct solutions. And student recover correct solutions.

And this done with reasoning models. So this done with reasoning models.

So for example, here they're using a for example, here they're using a DeepSseek R1, right? Because it's open DeepSseek R1, right?

Because it's open source, but of course it can be the 03 source, but of course it can be the 03 model from OpenAI. Google's Gemini 2.5 model from OpenAI.

Google's Gemini 2.5 Pro is a reasoning model. So most of this follow a two-step learning process.

First, you train up the teacher model. First, you train up the teacher model.

So for the DeepSeek R1, it was the V3. That was likely the teacher model.

And then off of the back of that you produced the reasoning model that was trained with reinforcement learning to trained with reinforcement learning to reason through things and arrive at the reason through things and arrive at the correct answer. Right?

So the teacher model is trained and then its outputs model is trained and then its outputs are used to train a student model which are used to train a student model which becomes the final product. So we produce the teacher and the teacher outputs lectures let's say or some sort of synthetic data information that then is used to teach the student and the student is the outcome of that.

the student is the one that's being graded, you know, through reinforcement learning. And these teacher models are learning.

And these teacher models are trained using expensive RL, trained using expensive RL, reinforcement learning, where the model reinforcement learning, where the model must learn to solve these problems from must learn to solve these problems from scratch and is rewarded only when it scratch and is rewarded only when it gets the right answer.

This process is slow, costly, and often narrowly focused, requiring carefully filtered focused, requiring carefully filtered outputs from the teacher to ensure the outputs from the teacher to ensure the student learns effectively. And so, student learns effectively.

And so, here's where they kind of flip around. here's where they kind of flip around.

So instead of teaching by solving, So instead of teaching by solving, they're instead approaching it through a they're instead approaching it through a learn to teach perspective. They have the questions, they have known solutions, and we're asking them to solutions, and we're asking them to output clear step-by-step explanations, output clear step-by-step explanations, just like great human instructors would, just like great human instructors would, and they are graded for how helpful and they are graded for how helpful their explanations are to the student.

their explanations are to the student. And of course, this aligns the teacher model to its true purpose, being helpful to the students.

But, and this very to the students. But, and this very interesting, it also allows us to use interesting, it also allows us to use small efficient models that wouldn't small efficient models that wouldn't otherwise be able to solve problems on otherwise be able to solve problems on their own.

So, to solve the problems, their own. So, to solve the problems, you need a large smart model that's expensive to run to produce excellent training materials for the student.

It training materials for the student. It sounds like they can use a small efficient models and the results are quite good.

So, as you can see here, this the sort of base model at 39. they add the red is the learning to they add the red is the learning to solve, right?

And so using that approach, they bump it up to 46.6, but with this new approach, the learning how to teach approach, they get it up to 49.5 and they use the AIM competition 49.5 and they use the AIM competition math and the GPQA. So a lot of the benchmarks that we see, this what they're sort of their benchmark on to they're sort of their benchmark on to see how well they perform.

And as I say see how well they perform. And as I say here, the result is surprising.

We had here, the result is surprising. We had multiple papers in the last few weeks that were surprising.

When we find new ways to approach some of these problems, these training methods, some of them have very surprising results in how have very surprising results in how effective they are. Even though effective they are.

Even though intuitively they might not make a lot of sense, these compact teachers with only the 7 billion parameters, so that's a the 7 billion parameters, so that's a very small model, are better at very small model, are better at teaching or reasoning skills than order teaching or reasoning skills than order of magnitude larger LLMs or orders of magnitude larger LLMs or orders of magnitude as they're saying here.

So 100 times bigger, thousand times bigger, thus making advanced AI more affordable and much faster to train. And here they have a pretty good diagram learning to have a pretty good diagram learning to solve.

So you have this base model, the solve. So you have this base model, the large and expensive DeepSeek V3 in this case.

So you have the various tasks that you sort of put into the teacher model, the DeepSeek R10. The answer data is uh graded so to speak, right?

So they're getting rewards for getting that correct, right? when they when they answer correctly, they get rewards, reinforcement learning.

get rewards, reinforcement learning. This process happens until the model This process happens until the model gets better and better at answering gets better and better at answering those questions correctly.

So this those questions correctly. So this its doggy treats when it does the right trick.

And finally, this cold start distillation process into the sort of final model. So it means cold start meaning that it might not have too much prior knowledge, right?

So we're kind of um using this reinforcement learning to um using this reinforcement learning to put all that knowledge into the model. put all that knowledge into the model.

distillation is kind of copying the distillation is kind of copying the previous model's behavior. So in effect, previous model's behavior.

So in effect, we're using what's produced by the we're using what's produced by the teacher model, the answers to make that final model that we're actually going to be using for the tasks. In this case, be using for the tasks.

In this case, DeepSeek R1 for example. So this kind of the normal process and this probably how all the labs are doing this to create their final reasoning models or some variations of this, but this or some variations of this, but this kind of is a big picture of what that looks like.

Notice everything kind of relies on the tasks and the answer data and the reinforcement learning is using those things. In the learning to teach approach, it's a little bit different because you know we take the small cheap because you know we take the small cheap and expensive in this case 7 billion parameter base model.

We use the tasks to create this teacher model that to create this teacher model that produces not the answers because it produces not the answers because it knows the answers but rather explanation knows the answers but rather explanation data. And importantly, the reward DRL data.

And importantly, the reward DRL loop comes from how well this loop comes from how well this explanation data helps the student model explanation data helps the student model perform on answering those questions. If perform on answering those questions.

If it does well, right, the reward feedback it does well, right, the reward feedback goes to the teacher model. So it knows okay these sort of explanations are better for these student models to better for these student models to understand how to do these tasks.

So this becomes the RL loop. Then finally once it's completed we take that once it's completed we take that explanation data and we use that to do the cold start distillation to the final model.

So as they continue here through our L expensive LMS learn to solve intricate math coding and logical intricate math coding and logical problems from scratch. They do this through trial and error through this process of reinforcement learning.

And this highly effective, but it has some drawbacks. Notably, these models some drawbacks.

Notably, these models tend to become nearly focused. They're tend to become nearly focused.

They're good at the task they have been trained on, but less capable of generalizing to broader applications. So, they're taught broader applications.

So, they're taught to arrive at the right answer, but not necessarily how to think about arriving at the right answer. And as they put it here, the unreasonable effectiveness of tiny specialized teachers.

and they're tiny specialized teachers. and they're putting their RLT model to test against putting their RLT model to test against the best known methods in the field.

Again, this RLT model is just 7 billion parameters. It's definitely small on the parameters.

It's definitely small on the tiny side and it's competing against tiny side and it's competing against much larger models like DeepSec R1 and much larger models like DeepSec R1 and QVQ. This Quen's reasoning model, one QVQ.

This Quen's reasoning model, one of them in the series of reasoning of them in the series of reasoning models, and they're using GPT4 mini to clean up the outputs before using them to train student models. Even so, the much smaller RLT outperformed them across multiple challenging benchmarks across multiple challenging benchmarks in math and science.

So, here at the top, we have the Deepseek R1 as the teacher with 671 teacher with 671 billion parameters, like a pretty hefty model. And we have our RLT teacher at 7 billion, much smaller, right?

They're both One10enth the size. They're both teaching Quen 7 billion how to do various tasks on the AIM math GPQA diamond.

So these complicated diamond. So these complicated benchmarks, right?

And so this top line is sort of how it starts. So as you can see here, it's it's not great.

It's a 39 point overall. If you kind of average all them together, if we're using the all them together, if we're using the big DeepC car 1 model as the trainer, big DeepC car 1 model as the trainer, well, it gets a lot better, right?

So it well, it gets a lot better, right? So it jumps to 46.6 overall.

So, this massive model gives it a good boost, a good improvement, but the tiny 7 billion improvement, but the tiny 7 billion model, as you can see, pushes even further to 49.5. So, keep in mind that these smaller models are going to be much faster, much cheaper.

It's going to be more possible to run it on even perhaps consumergrade hardware. Point being is you can get a hardware.

Point being is you can get a lot more done with the same amount of compute that you have and the results are better than these massive models. And here at the bottom they're answering the question, can the smaller teacher the question, can the smaller teacher teach the bigger student?

Right? So a 7 billion parameter teacher, can it teach the 32 billion parameter student?

And we still see excellent outcomes even though the student is a much larger model. They highlight what a big difference the cost of the models makes.

So since these models are much smaller from a cost perspective, the difference is dramatic. perspective, the difference is dramatic.

Train the 32 billion student with our method took less than a day on a single compute node. While traditional RL would compute node.

While traditional RL would have taken months on the same hardware. So while the results are better, it's much faster, much cheaper.

This much faster, much cheaper. This training also creates better reasoning training also creates better reasoning steps.

The explanations are more focused steps. The explanations are more focused and even managed to add additional and even managed to add additional logical steps omitted by R1 using a clear and direct language.

They mirror the conciseness and clarity of expert the conciseness and clarity of expert human educators. So the future, a new frontier of more advanced and cheaper reasoning models.

Again, as more people read this paper and begin applying this, we could see a revolution of sorts in we could see a revolution of sorts in how we train these models. Again, we're not going to see it for a while, but if this approach works as well as it seems this approach works as well as it seems to in this paper, I mean, think about to in this paper, I mean, think about the cost savings.

We went from months of the cost savings. We went from months of training down to a single day.

So to put that in perspective, that's the difference between training a model up for $10,000 using this approach where taking the traditional RL approach would cost something like half a million and that half a million model wouldn't perform as well as the $10,000 model. Again, this seems like a big deal.

If it's easily adaptable to how we train models, if adaptable to how we train models, if there's no downsides, this could be there's no downsides, this could be quite a big revolution of sorts. Also, as they point out here, this shift to their new approach makes it possible to their new approach makes it possible to apply reinforcement learning in areas apply reinforcement learning in areas once considered too difficult for once considered too difficult for language models to handle directly.

If language models to handle directly. If you think about it, there's a lot of you think about it, there's a lot of great teachers out there, perhaps math great teachers out there, perhaps math teachers, that are excellent at teachers, that are excellent at explaining how to do certain proofs or certain math problems.

Those people might not be that great coming up initially with that idea. So they might not have been able to solve that on not have been able to solve that on their own which is what we're asking their own which is what we're asking these models to do kind of from scratch these models to do kind of from scratch going all right how do you solve it figure it out right but those teachers might be excellent at explaining to might be excellent at explaining to students how to approach that problem so again if this holds this could be huge as they say here rlts could disrupt the as they say here rlts could disrupt the cost of training advanced models instead cost of training advanced models instead of relying on massive systems at every of relying on massive systems at every stage we can train small specialized stage we can train small specialized teachers and use them to teach much larger models efficiently.

This flips the traditional scaling paradigm. flips the traditional scaling paradigm.

The heaviest work is handled by compact, affordable models that unlock powerful capabilities in the students they train. capabilities in the students they train.

Looking ahead, this framework hints at Looking ahead, this framework hints at something even more intriguing. A model something even more intriguing.

A model that plays both the teacher and the that plays both the teacher and the student roles at once. By generating student roles at once.

By generating explanations for its own benefit, such a explanations for its own benefit, such a system could learn how to teach itself system could learn how to teach itself better over time. This idea echoes the better over time.

This idea echoes the vision of the Darwin Goal machine. vision of the Darwin Goal machine.

Again, Sakana AI is behind that one as well. They've created a self-evolving model that improves its own ability to model that improves its own ability to do various coding tasks.

It creates code that makes it better at coding. It's wild.

As I say here, it evolves through self-reflection and recursive learning. So, Sakana AI once again dropping huge papers that seem absolutely massive.

I've covered the Darvin go to machine in a different video, but the basic idea is it tries a lot of different approaches it tries a lot of different approaches to improve itself, typing up new tools for itself, new abilities, new approaches. And each time it kind of tests if that new approach or ability or whatever improves its ability to code.

whatever improves its ability to code. And they use the SUI bench, a benchmark in this case to see if it does better on it.

That means it improved. And over time it uses kind of this evolutionary approach, right?

So there's a certain approach, right? So there's a certain ideas that when they work, it continues ideas that when they work, it continues trying to find more ideas kind of in that direction.

And these form certain lineages. Some of them kind of go lineages.

Some of them kind of go extinct cuz they're dead ends. It it extinct cuz they're dead ends.

It it doesn't work to improve it. That's fine doesn't work to improve it.

That's fine because some of them are real champion because some of them are real champion lineages that come up to create the best possible outcomes. Here's the progress.

As you can see here, goes up. you know, test a bunch of different stuff and but every once in a while just jumps up in every once in a while just jumps up in its ability.

All this kind of its ability. All this kind of suggesting the same thing that we're beginning this self-recursive process of these models improving themselves.

these models improving themselves. Smaller models are better at teaching with certain scaffolding are better at creating tools for itself to improve creating tools for itself to improve itself.

And we're going to be seeing a lot more of this moving forwards because in effect we're now letting AI handle some of the AI research, some of the machine learning research. We're still in the early stages of that, but I feel like it's going to get faster and faster and kind of like build on itself.

It's going to start to snowball. Let me know going to start to snowball.

Let me know what you think about this. Will the what you think about this.

Will the markets react to this just like they did to the deepseek originally by losing a trillion dollars of global market caps in a day? Or is the fact that now a $7 billion model can train a much better model.

Could that also imply that it's going to be a lot more accessible to everyday people and more researchers and smaller labs? It's going to allow them to jump in and start training their own models using Sakana AI's approach.

Let models using Sakana AI's approach. Let me know what you think.

I'm curious to me know what you think. I'm curious to know what you think of this, how big it is.

Again, we've yet to see how the other labs sort of react to this. They other labs sort of react to this.

They announced it just within the last 24 announced it just within the last 24 hours. And since they're not as well known as Google and OpenAI and Anthropic, maybe it'll take a while for Anthropic, maybe it'll take a while for this news to kind of percolate through this news to kind of percolate through the industry.

But make no mistake, the industry. But make no mistake, Sakana AI tends to hit above their weight.

Notice they've published everything on GitHub. This open source.

This code, this everything is available to everyone. It even has the available to everyone.

It even has the one thing that none of us can resist, and that is the cutesy anime characters. Not sure why they made this one look Not sure why they made this one look sad.

Let me know what you think. My name is Wes Roth and I'll see you next

## Timestamped Transcript

[00:00] So, Sakana AI is back. They're the
[00:02] So, Sakana AI is back. They're the
[00:02] So, Sakana AI is back. They're the people behind the Darwin Goal machine, a
[00:05] people behind the Darwin Goal machine, a
[00:05] people behind the Darwin Goal machine, a self-improving coding agent. They also
[00:07] self-improving coding agent. They also
[00:07] self-improving coding agent. They also created the first AI that had a machine
[00:10] created the first AI that had a machine
[00:10] created the first AI that had a machine learning scientific paper that passed
[00:12] learning scientific paper that passed
[00:12] learning scientific paper that passed peer review. And they're back with yet
[00:14] peer review. And they're back with yet
[00:14] peer review. And they're back with yet another open-source project plus a
[00:16] another open-source project plus a
[00:16] another open-source project plus a research paper published, the
[00:18] research paper published, the
[00:18] research paper published, the implications of which seem potentially
[00:22] implications of which seem potentially
[00:22] implications of which seem potentially revolutionary. So, RL or reinforcement
[00:25] revolutionary. So, RL or reinforcement
[00:25] revolutionary. So, RL or reinforcement learning is where we attempt to teach
[00:27] learning is where we attempt to teach
[00:27] learning is where we attempt to teach these AIs to do something. And when they
[00:30] these AIs to do something. And when they
[00:30] these AIs to do something. And when they do well, we give them a reward. They get
[00:32] do well, we give them a reward. They get
[00:32] do well, we give them a reward. They get better at math or coding and we give
[00:34] better at math or coding and we give
[00:34] better at math or coding and we give them a virtual high five to let them
[00:36] them a virtual high five to let them
[00:36] them a virtual high five to let them know that they're getting better, that
[00:38] know that they're getting better, that
[00:38] know that they're getting better, that they're getting closer. Basically, we
[00:39] they're getting closer. Basically, we
[00:39] they're getting closer. Basically, we say, "Whatever you've been doing, do
[00:41] say, "Whatever you've been doing, do
[00:41] say, "Whatever you've been doing, do more of that." We can also have negative
[00:43] more of that." We can also have negative
[00:43] more of that." We can also have negative reinforcement where we panalyze some
[00:46] reinforcement where we panalyze some
[00:46] reinforcement where we panalyze some actions or outcomes that tend to not to
[00:48] actions or outcomes that tend to not to
[00:48] actions or outcomes that tend to not to lead to the thing that we want them to
[00:50] lead to the thing that we want them to
[00:50] lead to the thing that we want them to do. For example, you might recall that
[00:51] do. For example, you might recall that
[00:51] do. For example, you might recall that game engine, that neural network that
[00:54] game engine, that neural network that
[00:54] game engine, that neural network that was able to basically replicate the game
[00:56] was able to basically replicate the game
[00:56] was able to basically replicate the game of Doom, right? So, it played the game
[00:58] of Doom, right? So, it played the game
[00:58] of Doom, right? So, it played the game of Doom in real time, but without a
[01:01] of Doom in real time, but without a
[01:01] of Doom in real time, but without a single piece of code. It wasn't
[01:02] single piece of code. It wasn't
[01:02] single piece of code. It wasn't software. It was a neural network kind
[01:04] software. It was a neural network kind
[01:04] software. It was a neural network kind of just dreaming it up into life as it
[01:07] of just dreaming it up into life as it
[01:07] of just dreaming it up into life as it went along. In order to get data for the
[01:09] went along. In order to get data for the
[01:09] went along. In order to get data for the game, they actually trained up a bunch
[01:10] game, they actually trained up a bunch
[01:10] game, they actually trained up a bunch of little AI agents that played Doom. To
[01:13] of little AI agents that played Doom. To
[01:13] of little AI agents that played Doom. To do that, they used reinforcement
[01:15] do that, they used reinforcement
[01:15] do that, they used reinforcement learning RL to teach them to play Doom.
[01:18] learning RL to teach them to play Doom.
[01:18] learning RL to teach them to play Doom. And here's the reward function that
[01:20] And here's the reward function that
[01:20] And here's the reward function that they've used. So, if the player got hit,
[01:22] they've used. So, if the player got hit,
[01:22] they've used. So, if the player got hit, that would be negative 100 points. Its
[01:24] that would be negative 100 points. Its
[01:24] that would be negative 100 points. Its dying would be 5,000 points. hitting
[01:27] dying would be 5,000 points. hitting
[01:27] dying would be 5,000 points. hitting enemies was worth 300 positive points,
[01:29] enemies was worth 300 positive points,
[01:29] enemies was worth 300 positive points, right? So, a virtual high five, like
[01:30] right? So, a virtual high five, like
[01:30] right? So, a virtual high five, like good job. Enemy kill a,000 points. And
[01:33] good job. Enemy kill a,000 points. And
[01:33] good job. Enemy kill a,000 points. And various other things that improved their
[01:35] various other things that improved their
[01:35] various other things that improved their gameplay or progressed the game forward
[01:37] gameplay or progressed the game forward
[01:37] gameplay or progressed the game forward also gave it points. And the AI went out
[01:40] also gave it points. And the AI went out
[01:40] also gave it points. And the AI went out there, played Doom, and tried to
[01:42] there, played Doom, and tried to
[01:42] there, played Doom, and tried to maximize the amount of points it would
[01:43] maximize the amount of points it would
[01:43] maximize the amount of points it would get by, you know, progressing the game
[01:45] get by, you know, progressing the game
[01:45] get by, you know, progressing the game forward, shooting enemies, etc., while
[01:47] forward, shooting enemies, etc., while
[01:47] forward, shooting enemies, etc., while at the same time trying to avoid getting
[01:49] at the same time trying to avoid getting
[01:49] at the same time trying to avoid getting hit and especially avoid dying. This
[01:52] hit and especially avoid dying. This
[01:52] hit and especially avoid dying. This paper flips this whole idea on its head
[01:54] paper flips this whole idea on its head
[01:54] paper flips this whole idea on its head just a little bit. Here they introduce
[01:56] just a little bit. Here they introduce
[01:56] just a little bit. Here they introduce the reinforcement learned teacher. So we
[01:59] the reinforcement learned teacher. So we
[01:59] the reinforcement learned teacher. So we train a teacher model to generate
[02:01] train a teacher model to generate
[02:01] train a teacher model to generate explanations from question answer pairs.
[02:05] explanations from question answer pairs.
[02:05] explanations from question answer pairs. So this model is given a question and it
[02:07] So this model is given a question and it
[02:07] So this model is given a question and it knows the correct answer. It's not
[02:09] knows the correct answer. It's not
[02:09] knows the correct answer. It's not trying to figure out the correct answer.
[02:11] trying to figure out the correct answer.
[02:11] trying to figure out the correct answer. It already knows it and its goal is to
[02:14] It already knows it and its goal is to
[02:14] It already knows it and its goal is to output a great explanation for how to
[02:17] output a great explanation for how to
[02:17] output a great explanation for how to arrive at that answer. So this teacher
[02:20] arrive at that answer. So this teacher
[02:20] arrive at that answer. So this teacher model is optimized to improve a student
[02:22] model is optimized to improve a student
[02:22] model is optimized to improve a student model's understanding. With most RL
[02:25] model's understanding. With most RL
[02:25] model's understanding. With most RL training, the model we're training is
[02:27] training, the model we're training is
[02:27] training, the model we're training is usually the student, at least for
[02:29] usually the student, at least for
[02:29] usually the student, at least for reinforcement learning RL, right? So,
[02:31] reinforcement learning RL, right? So,
[02:31] reinforcement learning RL, right? So, we're sort of giving it positive rewards
[02:33] we're sort of giving it positive rewards
[02:33] we're sort of giving it positive rewards to the student for producing the correct
[02:35] to the student for producing the correct
[02:35] to the student for producing the correct answers. Similar to school in college,
[02:37] answers. Similar to school in college,
[02:37] answers. Similar to school in college, the student is the one that's being
[02:39] the student is the one that's being
[02:39] the student is the one that's being graded. If a student does poorly, we say
[02:42] graded. If a student does poorly, we say
[02:42] graded. If a student does poorly, we say that's a bad student. If they do well,
[02:44] that's a bad student. If they do well,
[02:44] that's a bad student. If they do well, we say that's a good student. But what
[02:46] we say that's a good student. But what
[02:46] we say that's a good student. But what if we rather graded the teacher? If the
[02:49] if we rather graded the teacher? If the
[02:49] if we rather graded the teacher? If the teacher taught well and the students
[02:51] teacher taught well and the students
[02:51] teacher taught well and the students score improved, that's a good teacher.
[02:54] score improved, that's a good teacher.
[02:54] score improved, that's a good teacher. If the teacher through whatever lectures
[02:56] If the teacher through whatever lectures
[02:56] If the teacher through whatever lectures or solutions or whatever way choose to
[02:59] or solutions or whatever way choose to
[02:59] or solutions or whatever way choose to taught, if it decreased the scores of
[03:01] taught, if it decreased the scores of
[03:01] taught, if it decreased the scores of the student, then we say that's a bad
[03:03] the student, then we say that's a bad
[03:03] the student, then we say that's a bad teacher. So this model rather than
[03:05] teacher. So this model rather than
[03:05] teacher. So this model rather than solving problems from scratch, the
[03:07] solving problems from scratch, the
[03:07] solving problems from scratch, the teacher is rewarded based on how
[03:08] teacher is rewarded based on how
[03:08] teacher is rewarded based on how effectively its explanations help the
[03:11] effectively its explanations help the
[03:11] effectively its explanations help the student recover correct solutions. And
[03:13] student recover correct solutions. And
[03:13] student recover correct solutions. And this is done with reasoning models. So
[03:16] this is done with reasoning models. So
[03:16] this is done with reasoning models. So for example, here they're using a
[03:17] for example, here they're using a
[03:17] for example, here they're using a DeepSseek R1, right? Because it's open
[03:19] DeepSseek R1, right? Because it's open
[03:19] DeepSseek R1, right? Because it's open source, but of course it can be the 03
[03:22] source, but of course it can be the 03
[03:22] source, but of course it can be the 03 model from OpenAI. Google's Gemini 2.5
[03:25] model from OpenAI. Google's Gemini 2.5
[03:26] model from OpenAI. Google's Gemini 2.5 Pro is a reasoning model. So most of
[03:28] Pro is a reasoning model. So most of
[03:28] Pro is a reasoning model. So most of this follow a two-step learning process.
[03:31] this follow a two-step learning process.
[03:31] this follow a two-step learning process. First, you train up the teacher model.
[03:33] First, you train up the teacher model.
[03:33] First, you train up the teacher model. So for the DeepSeek R1, it was the V3.
[03:37] So for the DeepSeek R1, it was the V3.
[03:37] So for the DeepSeek R1, it was the V3. That was likely the teacher model. And
[03:39] That was likely the teacher model. And
[03:39] That was likely the teacher model. And then off of the back of that you
[03:41] then off of the back of that you
[03:41] then off of the back of that you produced the reasoning model that was
[03:43] produced the reasoning model that was
[03:43] produced the reasoning model that was trained with reinforcement learning to
[03:45] trained with reinforcement learning to
[03:45] trained with reinforcement learning to reason through things and arrive at the
[03:47] reason through things and arrive at the
[03:47] reason through things and arrive at the correct answer. Right? So the teacher
[03:49] correct answer. Right? So the teacher
[03:49] correct answer. Right? So the teacher model is trained and then its outputs
[03:51] model is trained and then its outputs
[03:51] model is trained and then its outputs are used to train a student model which
[03:53] are used to train a student model which
[03:53] are used to train a student model which becomes the final product. So we produce
[03:55] becomes the final product. So we produce
[03:55] becomes the final product. So we produce the teacher and the teacher outputs
[03:58] the teacher and the teacher outputs
[03:58] the teacher and the teacher outputs lectures let's say or some sort of
[03:59] lectures let's say or some sort of
[04:00] lectures let's say or some sort of synthetic data information that then is
[04:01] synthetic data information that then is
[04:01] synthetic data information that then is used to teach the student and the
[04:03] used to teach the student and the
[04:03] used to teach the student and the student is the outcome of that. the
[04:05] student is the outcome of that. the
[04:05] student is the outcome of that. the student is the one that's being graded,
[04:07] student is the one that's being graded,
[04:07] student is the one that's being graded, you know, through reinforcement
[04:08] you know, through reinforcement
[04:08] you know, through reinforcement learning. And these teacher models are
[04:10] learning. And these teacher models are
[04:10] learning. And these teacher models are trained using expensive RL,
[04:12] trained using expensive RL,
[04:12] trained using expensive RL, reinforcement learning, where the model
[04:14] reinforcement learning, where the model
[04:14] reinforcement learning, where the model must learn to solve these problems from
[04:16] must learn to solve these problems from
[04:16] must learn to solve these problems from scratch and is rewarded only when it
[04:18] scratch and is rewarded only when it
[04:18] scratch and is rewarded only when it gets the right answer. This process is
[04:20] gets the right answer. This process is
[04:20] gets the right answer. This process is slow, costly, and often narrowly
[04:22] slow, costly, and often narrowly
[04:22] slow, costly, and often narrowly focused, requiring carefully filtered
[04:24] focused, requiring carefully filtered
[04:24] focused, requiring carefully filtered outputs from the teacher to ensure the
[04:26] outputs from the teacher to ensure the
[04:26] outputs from the teacher to ensure the student learns effectively. And so,
[04:28] student learns effectively. And so,
[04:28] student learns effectively. And so, here's where they kind of flip around.
[04:30] here's where they kind of flip around.
[04:30] here's where they kind of flip around. So instead of teaching by solving,
[04:33] So instead of teaching by solving,
[04:33] So instead of teaching by solving, they're instead approaching it through a
[04:34] they're instead approaching it through a
[04:34] they're instead approaching it through a learn to teach perspective. They have
[04:37] learn to teach perspective. They have
[04:37] learn to teach perspective. They have the questions, they have known
[04:38] the questions, they have known
[04:38] the questions, they have known solutions, and we're asking them to
[04:40] solutions, and we're asking them to
[04:40] solutions, and we're asking them to output clear step-by-step explanations,
[04:42] output clear step-by-step explanations,
[04:42] output clear step-by-step explanations, just like great human instructors would,
[04:45] just like great human instructors would,
[04:45] just like great human instructors would, and they are graded for how helpful
[04:47] and they are graded for how helpful
[04:47] and they are graded for how helpful their explanations are to the student.
[04:50] their explanations are to the student.
[04:50] their explanations are to the student. And of course, this aligns the teacher
[04:52] And of course, this aligns the teacher
[04:52] And of course, this aligns the teacher model to its true purpose, being helpful
[04:54] model to its true purpose, being helpful
[04:54] model to its true purpose, being helpful to the students. But, and this is very
[04:56] to the students. But, and this is very
[04:56] to the students. But, and this is very interesting, it also allows us to use
[04:58] interesting, it also allows us to use
[04:58] interesting, it also allows us to use small efficient models that wouldn't
[05:00] small efficient models that wouldn't
[05:00] small efficient models that wouldn't otherwise be able to solve problems on
[05:03] otherwise be able to solve problems on
[05:03] otherwise be able to solve problems on their own. So, to solve the problems,
[05:04] their own. So, to solve the problems,
[05:04] their own. So, to solve the problems, you need a large smart model that's
[05:07] you need a large smart model that's
[05:07] you need a large smart model that's expensive to run to produce excellent
[05:10] expensive to run to produce excellent
[05:10] expensive to run to produce excellent training materials for the student. It
[05:12] training materials for the student. It
[05:12] training materials for the student. It sounds like they can use a small
[05:13] sounds like they can use a small
[05:13] sounds like they can use a small efficient models and the results are
[05:16] efficient models and the results are
[05:16] efficient models and the results are quite good. So, as you can see here,
[05:18] quite good. So, as you can see here,
[05:18] quite good. So, as you can see here, this is the sort of base model at 39.
[05:21] this is the sort of base model at 39.
[05:21] this is the sort of base model at 39. they add the red is the learning to
[05:24] they add the red is the learning to
[05:24] they add the red is the learning to solve, right? And so using that
[05:26] solve, right? And so using that
[05:26] solve, right? And so using that approach, they bump it up to 46.6, but
[05:29] approach, they bump it up to 46.6, but
[05:29] approach, they bump it up to 46.6, but with this new approach, the learning how
[05:31] with this new approach, the learning how
[05:32] with this new approach, the learning how to teach approach, they get it up to
[05:34] to teach approach, they get it up to
[05:34] to teach approach, they get it up to 49.5 and they use the AIM competition
[05:38] 49.5 and they use the AIM competition
[05:38] 49.5 and they use the AIM competition math and the GPQA. So a lot of the
[05:41] math and the GPQA. So a lot of the
[05:41] math and the GPQA. So a lot of the benchmarks that we see, this is what
[05:42] benchmarks that we see, this is what
[05:42] benchmarks that we see, this is what they're sort of their benchmark on to
[05:44] they're sort of their benchmark on to
[05:44] they're sort of their benchmark on to see how well they perform. And as I say
[05:46] see how well they perform. And as I say
[05:46] see how well they perform. And as I say here, the result is surprising. We had
[05:49] here, the result is surprising. We had
[05:49] here, the result is surprising. We had multiple papers in the last few weeks
[05:51] multiple papers in the last few weeks
[05:51] multiple papers in the last few weeks that were surprising. When we find new
[05:54] that were surprising. When we find new
[05:54] that were surprising. When we find new ways to approach some of these problems,
[05:55] ways to approach some of these problems,
[05:56] ways to approach some of these problems, these training methods, some of them
[05:58] these training methods, some of them
[05:58] these training methods, some of them have very surprising results in how
[06:00] have very surprising results in how
[06:00] have very surprising results in how effective they are. Even though
[06:01] effective they are. Even though
[06:01] effective they are. Even though intuitively they might not make a lot of
[06:03] intuitively they might not make a lot of
[06:03] intuitively they might not make a lot of sense, these compact teachers with only
[06:06] sense, these compact teachers with only
[06:06] sense, these compact teachers with only the 7 billion parameters, so that's a
[06:09] the 7 billion parameters, so that's a
[06:09] the 7 billion parameters, so that's a very very small model, are better at
[06:11] very very small model, are better at
[06:11] very very small model, are better at teaching or reasoning skills than order
[06:13] teaching or reasoning skills than order
[06:13] teaching or reasoning skills than order of magnitude larger LLMs or orders of
[06:17] of magnitude larger LLMs or orders of
[06:17] of magnitude larger LLMs or orders of magnitude as they're saying here. So 100
[06:19] magnitude as they're saying here. So 100
[06:19] magnitude as they're saying here. So 100 times bigger, thousand times bigger,
[06:21] times bigger, thousand times bigger,
[06:21] times bigger, thousand times bigger, thus making advanced AI more affordable
[06:23] thus making advanced AI more affordable
[06:23] thus making advanced AI more affordable and much faster to train. And here they
[06:26] and much faster to train. And here they
[06:26] and much faster to train. And here they have a pretty good diagram learning to
[06:28] have a pretty good diagram learning to
[06:28] have a pretty good diagram learning to solve. So you have this base model, the
[06:30] solve. So you have this base model, the
[06:30] solve. So you have this base model, the large and expensive DeepSeek V3 in this
[06:33] large and expensive DeepSeek V3 in this
[06:33] large and expensive DeepSeek V3 in this case. So you have the various tasks that
[06:35] case. So you have the various tasks that
[06:35] case. So you have the various tasks that you sort of put into the teacher model,
[06:38] you sort of put into the teacher model,
[06:38] you sort of put into the teacher model, the DeepSeek R10.
[06:40] the DeepSeek R10.
[06:40] the DeepSeek R10. The answer data is uh graded so to
[06:43] The answer data is uh graded so to
[06:43] The answer data is uh graded so to speak, right? So they're getting rewards
[06:44] speak, right? So they're getting rewards
[06:44] speak, right? So they're getting rewards for getting that correct, right? when
[06:46] for getting that correct, right? when
[06:46] for getting that correct, right? when they when they answer correctly, they
[06:48] they when they answer correctly, they
[06:48] they when they answer correctly, they get rewards, reinforcement learning.
[06:50] get rewards, reinforcement learning.
[06:50] get rewards, reinforcement learning. This process happens until the model
[06:52] This process happens until the model
[06:52] This process happens until the model gets better and better at answering
[06:54] gets better and better at answering
[06:54] gets better and better at answering those questions correctly. So this is
[06:56] those questions correctly. So this is
[06:56] those questions correctly. So this is its doggy treats when it does the right
[06:59] its doggy treats when it does the right
[06:59] its doggy treats when it does the right trick. And finally, this cold start
[07:01] trick. And finally, this cold start
[07:01] trick. And finally, this cold start distillation process into the sort of
[07:04] distillation process into the sort of
[07:04] distillation process into the sort of final model. So it means cold start
[07:06] final model. So it means cold start
[07:06] final model. So it means cold start meaning that it might not have too much
[07:09] meaning that it might not have too much
[07:09] meaning that it might not have too much prior knowledge, right? So we're kind of
[07:11] prior knowledge, right? So we're kind of
[07:11] prior knowledge, right? So we're kind of um using this reinforcement learning to
[07:13] um using this reinforcement learning to
[07:13] um using this reinforcement learning to put all that knowledge into the model.
[07:15] put all that knowledge into the model.
[07:15] put all that knowledge into the model. distillation is kind of copying the
[07:17] distillation is kind of copying the
[07:17] distillation is kind of copying the previous model's behavior. So in effect,
[07:19] previous model's behavior. So in effect,
[07:19] previous model's behavior. So in effect, we're using what's produced by the
[07:21] we're using what's produced by the
[07:21] we're using what's produced by the teacher model, the answers to make that
[07:23] teacher model, the answers to make that
[07:23] teacher model, the answers to make that final model that we're actually going to
[07:25] final model that we're actually going to
[07:25] final model that we're actually going to be using for the tasks. In this case,
[07:28] be using for the tasks. In this case,
[07:28] be using for the tasks. In this case, DeepSeek R1 for example. So this is kind
[07:31] DeepSeek R1 for example. So this is kind
[07:31] DeepSeek R1 for example. So this is kind of the normal process and this is
[07:33] of the normal process and this is
[07:33] of the normal process and this is probably how all the labs are doing this
[07:36] probably how all the labs are doing this
[07:36] probably how all the labs are doing this to create their final reasoning models
[07:38] to create their final reasoning models
[07:38] to create their final reasoning models or some variations of this, but this
[07:40] or some variations of this, but this
[07:40] or some variations of this, but this kind of is a big picture of what that
[07:42] kind of is a big picture of what that
[07:42] kind of is a big picture of what that looks like. Notice everything kind of
[07:43] looks like. Notice everything kind of
[07:43] looks like. Notice everything kind of relies on the tasks and the answer data
[07:47] relies on the tasks and the answer data
[07:47] relies on the tasks and the answer data and the reinforcement learning is using
[07:49] and the reinforcement learning is using
[07:49] and the reinforcement learning is using those things. In the learning to teach
[07:52] those things. In the learning to teach
[07:52] those things. In the learning to teach approach, it's a little bit different
[07:54] approach, it's a little bit different
[07:54] approach, it's a little bit different because you know we take the small cheap
[07:57] because you know we take the small cheap
[07:57] because you know we take the small cheap and expensive in this case 7 billion
[07:59] and expensive in this case 7 billion
[07:59] and expensive in this case 7 billion parameter base model. We use the tasks
[08:01] parameter base model. We use the tasks
[08:01] parameter base model. We use the tasks to create this teacher model that
[08:04] to create this teacher model that
[08:04] to create this teacher model that produces not the answers because it
[08:06] produces not the answers because it
[08:06] produces not the answers because it knows the answers but rather explanation
[08:09] knows the answers but rather explanation
[08:09] knows the answers but rather explanation data. And importantly, the reward DRL
[08:12] data. And importantly, the reward DRL
[08:12] data. And importantly, the reward DRL loop comes from how well this
[08:14] loop comes from how well this
[08:14] loop comes from how well this explanation data helps the student model
[08:18] explanation data helps the student model
[08:18] explanation data helps the student model perform on answering those questions. If
[08:21] perform on answering those questions. If
[08:21] perform on answering those questions. If it does well, right, the reward feedback
[08:23] it does well, right, the reward feedback
[08:23] it does well, right, the reward feedback goes to the teacher model. So it knows
[08:25] goes to the teacher model. So it knows
[08:25] goes to the teacher model. So it knows okay these sort of explanations are
[08:28] okay these sort of explanations are
[08:28] okay these sort of explanations are better for these student models to
[08:30] better for these student models to
[08:30] better for these student models to understand how to do these tasks. So
[08:33] understand how to do these tasks. So
[08:33] understand how to do these tasks. So this becomes the RL loop. Then finally
[08:36] this becomes the RL loop. Then finally
[08:36] this becomes the RL loop. Then finally once it's completed we take that
[08:38] once it's completed we take that
[08:38] once it's completed we take that explanation data and we use that to do
[08:39] explanation data and we use that to do
[08:39] explanation data and we use that to do the cold start distillation to the final
[08:42] the cold start distillation to the final
[08:42] the cold start distillation to the final model. So as they continue here through
[08:45] model. So as they continue here through
[08:45] model. So as they continue here through our L expensive LMS learn to solve
[08:47] our L expensive LMS learn to solve
[08:47] our L expensive LMS learn to solve intricate math coding and logical
[08:49] intricate math coding and logical
[08:49] intricate math coding and logical problems from scratch. They do this
[08:51] problems from scratch. They do this
[08:51] problems from scratch. They do this through trial and error through this
[08:53] through trial and error through this
[08:53] through trial and error through this process of reinforcement learning. And
[08:55] process of reinforcement learning. And
[08:55] process of reinforcement learning. And this is highly effective, but it has
[08:57] this is highly effective, but it has
[08:57] this is highly effective, but it has some drawbacks. Notably, these models
[08:59] some drawbacks. Notably, these models
[08:59] some drawbacks. Notably, these models tend to become nearly focused. They're
[09:01] tend to become nearly focused. They're
[09:01] tend to become nearly focused. They're good at the task they have been trained
[09:03] good at the task they have been trained
[09:03] good at the task they have been trained on, but less capable of generalizing to
[09:05] on, but less capable of generalizing to
[09:05] on, but less capable of generalizing to broader applications. So, they're taught
[09:07] broader applications. So, they're taught
[09:07] broader applications. So, they're taught to arrive at the right answer, but not
[09:09] to arrive at the right answer, but not
[09:09] to arrive at the right answer, but not necessarily how to think about arriving
[09:12] necessarily how to think about arriving
[09:12] necessarily how to think about arriving at the right answer. And as they put it
[09:14] at the right answer. And as they put it
[09:14] at the right answer. And as they put it here, the unreasonable effectiveness of
[09:17] here, the unreasonable effectiveness of
[09:17] here, the unreasonable effectiveness of tiny specialized teachers. and they're
[09:19] tiny specialized teachers. and they're
[09:20] tiny specialized teachers. and they're putting their RLT model to test against
[09:23] putting their RLT model to test against
[09:23] putting their RLT model to test against the best known methods in the field.
[09:25] the best known methods in the field.
[09:25] the best known methods in the field. Again, this RLT model is just 7 billion
[09:27] Again, this RLT model is just 7 billion
[09:28] Again, this RLT model is just 7 billion parameters. It's definitely small on the
[09:30] parameters. It's definitely small on the
[09:30] parameters. It's definitely small on the tiny side and it's competing against
[09:33] tiny side and it's competing against
[09:33] tiny side and it's competing against much larger models like DeepSec R1 and
[09:36] much larger models like DeepSec R1 and
[09:36] much larger models like DeepSec R1 and QVQ. This is Quen's reasoning model, one
[09:40] QVQ. This is Quen's reasoning model, one
[09:40] QVQ. This is Quen's reasoning model, one of them in the series of reasoning
[09:41] of them in the series of reasoning
[09:41] of them in the series of reasoning models, and they're using GPT4 mini to
[09:44] models, and they're using GPT4 mini to
[09:44] models, and they're using GPT4 mini to clean up the outputs before using them
[09:45] clean up the outputs before using them
[09:45] clean up the outputs before using them to train student models. Even so, the
[09:48] to train student models. Even so, the
[09:48] to train student models. Even so, the much smaller RLT outperformed them
[09:50] much smaller RLT outperformed them
[09:50] much smaller RLT outperformed them across multiple challenging benchmarks
[09:52] across multiple challenging benchmarks
[09:52] across multiple challenging benchmarks in math and science. So, here at the
[09:54] in math and science. So, here at the
[09:54] in math and science. So, here at the top, we have the Deepseek R1 as the
[09:58] top, we have the Deepseek R1 as the
[09:58] top, we have the Deepseek R1 as the teacher with 671
[10:01] teacher with 671
[10:02] teacher with 671 billion parameters, like a pretty hefty
[10:04] billion parameters, like a pretty hefty
[10:04] billion parameters, like a pretty hefty model. And we have our RLT teacher at 7
[10:07] model. And we have our RLT teacher at 7
[10:07] model. And we have our RLT teacher at 7 billion, much much smaller, right?
[10:09] billion, much much smaller, right?
[10:10] billion, much much smaller, right? One10enth the size. They're both
[10:11] One10enth the size. They're both
[10:11] One10enth the size. They're both teaching Quen 7 billion how to do
[10:14] teaching Quen 7 billion how to do
[10:14] teaching Quen 7 billion how to do various tasks on the AIM math GPQA
[10:18] various tasks on the AIM math GPQA
[10:18] various tasks on the AIM math GPQA diamond. So these complicated
[10:20] diamond. So these complicated
[10:20] diamond. So these complicated benchmarks, right? And so this top line
[10:22] benchmarks, right? And so this top line
[10:22] benchmarks, right? And so this top line is sort of how it starts. So as you can
[10:24] is sort of how it starts. So as you can
[10:24] is sort of how it starts. So as you can see here, it's it's not great. It's a 39
[10:28] see here, it's it's not great. It's a 39
[10:28] see here, it's it's not great. It's a 39 point overall. If you kind of average
[10:30] point overall. If you kind of average
[10:30] point overall. If you kind of average all them together, if we're using the
[10:32] all them together, if we're using the
[10:32] all them together, if we're using the big DeepC car 1 model as the trainer,
[10:34] big DeepC car 1 model as the trainer,
[10:34] big DeepC car 1 model as the trainer, well, it gets a lot better, right? So it
[10:36] well, it gets a lot better, right? So it
[10:36] well, it gets a lot better, right? So it jumps to 46.6 overall. So, this massive
[10:40] jumps to 46.6 overall. So, this massive
[10:40] jumps to 46.6 overall. So, this massive model gives it a good boost, a good
[10:43] model gives it a good boost, a good
[10:43] model gives it a good boost, a good improvement, but the tiny 7 billion
[10:45] improvement, but the tiny 7 billion
[10:45] improvement, but the tiny 7 billion model, as you can see, pushes even
[10:47] model, as you can see, pushes even
[10:47] model, as you can see, pushes even further to 49.5.
[10:50] further to 49.5.
[10:50] further to 49.5. So, keep in mind that these smaller
[10:52] So, keep in mind that these smaller
[10:52] So, keep in mind that these smaller models are going to be much faster, much
[10:55] models are going to be much faster, much
[10:55] models are going to be much faster, much cheaper. It's going to be more possible
[10:57] cheaper. It's going to be more possible
[10:57] cheaper. It's going to be more possible to run it on even perhaps consumergrade
[10:59] to run it on even perhaps consumergrade
[11:00] to run it on even perhaps consumergrade hardware. Point being is you can get a
[11:02] hardware. Point being is you can get a
[11:02] hardware. Point being is you can get a lot more done with the same amount of
[11:04] lot more done with the same amount of
[11:04] lot more done with the same amount of compute that you have and the results
[11:07] compute that you have and the results
[11:07] compute that you have and the results are better than these massive models.
[11:10] are better than these massive models.
[11:10] are better than these massive models. And here at the bottom they're answering
[11:11] And here at the bottom they're answering
[11:11] And here at the bottom they're answering the question, can the smaller teacher
[11:14] the question, can the smaller teacher
[11:14] the question, can the smaller teacher teach the bigger student? Right? So a 7
[11:17] teach the bigger student? Right? So a 7
[11:17] teach the bigger student? Right? So a 7 billion parameter teacher, can it teach
[11:19] billion parameter teacher, can it teach
[11:19] billion parameter teacher, can it teach the 32 billion parameter student? And we
[11:22] the 32 billion parameter student? And we
[11:22] the 32 billion parameter student? And we still see excellent outcomes even though
[11:25] still see excellent outcomes even though
[11:25] still see excellent outcomes even though the student is a much larger model. They
[11:28] the student is a much larger model. They
[11:28] the student is a much larger model. They highlight what a big difference the cost
[11:31] highlight what a big difference the cost
[11:31] highlight what a big difference the cost of the models makes. So since these
[11:33] of the models makes. So since these
[11:33] of the models makes. So since these models are much smaller from a cost
[11:35] models are much smaller from a cost
[11:35] models are much smaller from a cost perspective, the difference is dramatic.
[11:37] perspective, the difference is dramatic.
[11:38] perspective, the difference is dramatic. Train the 32 billion student with our
[11:40] Train the 32 billion student with our
[11:40] Train the 32 billion student with our method took less than a day on a single
[11:42] method took less than a day on a single
[11:42] method took less than a day on a single compute node. While traditional RL would
[11:45] compute node. While traditional RL would
[11:45] compute node. While traditional RL would have taken months on the same hardware.
[11:48] have taken months on the same hardware.
[11:48] have taken months on the same hardware. So while the results are better, it's
[11:51] So while the results are better, it's
[11:51] So while the results are better, it's much much faster, much cheaper. This
[11:53] much much faster, much cheaper. This
[11:53] much much faster, much cheaper. This training also creates better reasoning
[11:55] training also creates better reasoning
[11:56] training also creates better reasoning steps. The explanations are more focused
[11:58] steps. The explanations are more focused
[11:58] steps. The explanations are more focused and even managed to add additional
[12:00] and even managed to add additional
[12:00] and even managed to add additional logical steps omitted by R1 using a
[12:03] logical steps omitted by R1 using a
[12:03] logical steps omitted by R1 using a clear and direct language. They mirror
[12:06] clear and direct language. They mirror
[12:06] clear and direct language. They mirror the conciseness and clarity of expert
[12:08] the conciseness and clarity of expert
[12:08] the conciseness and clarity of expert human educators. So the future, a new
[12:11] human educators. So the future, a new
[12:11] human educators. So the future, a new frontier of more advanced and cheaper
[12:13] frontier of more advanced and cheaper
[12:13] frontier of more advanced and cheaper reasoning models. Again, as more people
[12:16] reasoning models. Again, as more people
[12:16] reasoning models. Again, as more people read this paper and begin applying this,
[12:18] read this paper and begin applying this,
[12:18] read this paper and begin applying this, we could see a revolution of sorts in
[12:21] we could see a revolution of sorts in
[12:21] we could see a revolution of sorts in how we train these models. Again, we're
[12:22] how we train these models. Again, we're
[12:22] how we train these models. Again, we're not going to see it for a while, but if
[12:25] not going to see it for a while, but if
[12:25] not going to see it for a while, but if this approach works as well as it seems
[12:28] this approach works as well as it seems
[12:28] this approach works as well as it seems to in this paper, I mean, think about
[12:30] to in this paper, I mean, think about
[12:30] to in this paper, I mean, think about the cost savings. We went from months of
[12:33] the cost savings. We went from months of
[12:33] the cost savings. We went from months of training down to a single day. So to put
[12:36] training down to a single day. So to put
[12:36] training down to a single day. So to put that in perspective, that's the
[12:37] that in perspective, that's the
[12:37] that in perspective, that's the difference between training a model up
[12:40] difference between training a model up
[12:40] difference between training a model up for $10,000
[12:42] for $10,000
[12:42] for $10,000 using this approach where taking the
[12:44] using this approach where taking the
[12:44] using this approach where taking the traditional RL approach would cost
[12:46] traditional RL approach would cost
[12:46] traditional RL approach would cost something like half a million and that
[12:48] something like half a million and that
[12:48] something like half a million and that half a million model wouldn't perform as
[12:51] half a million model wouldn't perform as
[12:51] half a million model wouldn't perform as well as the $10,000 model. Again, this
[12:54] well as the $10,000 model. Again, this
[12:54] well as the $10,000 model. Again, this seems like a big deal. If it's easily
[12:57] seems like a big deal. If it's easily
[12:57] seems like a big deal. If it's easily adaptable to how we train models, if
[12:59] adaptable to how we train models, if
[12:59] adaptable to how we train models, if there's no downsides, this could be
[13:01] there's no downsides, this could be
[13:01] there's no downsides, this could be quite a big revolution of sorts. Also,
[13:04] quite a big revolution of sorts. Also,
[13:04] quite a big revolution of sorts. Also, as they point out here, this shift to
[13:06] as they point out here, this shift to
[13:06] as they point out here, this shift to their new approach makes it possible to
[13:08] their new approach makes it possible to
[13:08] their new approach makes it possible to apply reinforcement learning in areas
[13:10] apply reinforcement learning in areas
[13:10] apply reinforcement learning in areas once considered too difficult for
[13:12] once considered too difficult for
[13:12] once considered too difficult for language models to handle directly. If
[13:15] language models to handle directly. If
[13:15] language models to handle directly. If you think about it, there's a lot of
[13:16] you think about it, there's a lot of
[13:16] you think about it, there's a lot of great teachers out there, perhaps math
[13:19] great teachers out there, perhaps math
[13:19] great teachers out there, perhaps math teachers, that are excellent at
[13:21] teachers, that are excellent at
[13:21] teachers, that are excellent at explaining how to do certain proofs or
[13:24] explaining how to do certain proofs or
[13:24] explaining how to do certain proofs or certain math problems. Those people
[13:26] certain math problems. Those people
[13:26] certain math problems. Those people might not be that great at coming up
[13:29] might not be that great at coming up
[13:29] might not be that great at coming up initially with that idea. So they might
[13:31] initially with that idea. So they might
[13:31] initially with that idea. So they might not have been able to solve that on
[13:33] not have been able to solve that on
[13:33] not have been able to solve that on their own which is what we're asking
[13:35] their own which is what we're asking
[13:35] their own which is what we're asking these models to do kind of from scratch
[13:37] these models to do kind of from scratch
[13:37] these models to do kind of from scratch going all right how do you solve it
[13:38] going all right how do you solve it
[13:38] going all right how do you solve it figure it out right but those teachers
[13:40] figure it out right but those teachers
[13:40] figure it out right but those teachers might be excellent at explaining to
[13:43] might be excellent at explaining to
[13:43] might be excellent at explaining to students how to approach that problem so
[13:45] students how to approach that problem so
[13:45] students how to approach that problem so again if this holds this could be huge
[13:47] again if this holds this could be huge
[13:47] again if this holds this could be huge as they say here rlts could disrupt the
[13:51] as they say here rlts could disrupt the
[13:51] as they say here rlts could disrupt the cost of training advanced models instead
[13:53] cost of training advanced models instead
[13:53] cost of training advanced models instead of relying on massive systems at every
[13:55] of relying on massive systems at every
[13:55] of relying on massive systems at every stage we can train small specialized
[13:57] stage we can train small specialized
[13:57] stage we can train small specialized teachers and use them to teach much
[13:59] teachers and use them to teach much
[13:59] teachers and use them to teach much larger models models efficiently. This
[14:01] larger models models efficiently. This
[14:01] larger models models efficiently. This flips the traditional scaling paradigm.
[14:04] flips the traditional scaling paradigm.
[14:04] flips the traditional scaling paradigm. The heaviest work is handled by compact,
[14:06] The heaviest work is handled by compact,
[14:06] The heaviest work is handled by compact, affordable models that unlock powerful
[14:09] affordable models that unlock powerful
[14:09] affordable models that unlock powerful capabilities in the students they train.
[14:11] capabilities in the students they train.
[14:11] capabilities in the students they train. Looking ahead, this framework hints at
[14:13] Looking ahead, this framework hints at
[14:13] Looking ahead, this framework hints at something even more intriguing. A model
[14:15] something even more intriguing. A model
[14:15] something even more intriguing. A model that plays both the teacher and the
[14:16] that plays both the teacher and the
[14:16] that plays both the teacher and the student roles at once. By generating
[14:19] student roles at once. By generating
[14:19] student roles at once. By generating explanations for its own benefit, such a
[14:21] explanations for its own benefit, such a
[14:21] explanations for its own benefit, such a system could learn how to teach itself
[14:24] system could learn how to teach itself
[14:24] system could learn how to teach itself better over time. This idea echoes the
[14:27] better over time. This idea echoes the
[14:27] better over time. This idea echoes the vision of the Darwin Goal machine.
[14:29] vision of the Darwin Goal machine.
[14:29] vision of the Darwin Goal machine. Again, Sakana AI is behind that one as
[14:32] Again, Sakana AI is behind that one as
[14:32] Again, Sakana AI is behind that one as well. They've created a self-evolving
[14:35] well. They've created a self-evolving
[14:35] well. They've created a self-evolving model that improves its own ability to
[14:38] model that improves its own ability to
[14:38] model that improves its own ability to do various coding tasks. It creates code
[14:41] do various coding tasks. It creates code
[14:41] do various coding tasks. It creates code that makes it better at coding. It's
[14:44] that makes it better at coding. It's
[14:44] that makes it better at coding. It's wild. As I say here, it evolves through
[14:46] wild. As I say here, it evolves through
[14:46] wild. As I say here, it evolves through self-reflection and recursive learning.
[14:49] self-reflection and recursive learning.
[14:49] self-reflection and recursive learning. So, Sakana AI once again dropping huge
[14:53] So, Sakana AI once again dropping huge
[14:54] So, Sakana AI once again dropping huge papers that seem absolutely massive.
[14:56] papers that seem absolutely massive.
[14:56] papers that seem absolutely massive. I've covered the Darvin go to machine in
[14:59] I've covered the Darvin go to machine in
[14:59] I've covered the Darvin go to machine in a different video, but the basic idea is
[15:02] a different video, but the basic idea is
[15:02] a different video, but the basic idea is it tries a lot of different approaches
[15:04] it tries a lot of different approaches
[15:04] it tries a lot of different approaches to improve itself, typing up new tools
[15:07] to improve itself, typing up new tools
[15:08] to improve itself, typing up new tools for itself, new abilities, new
[15:09] for itself, new abilities, new
[15:09] for itself, new abilities, new approaches. And each time it kind of
[15:11] approaches. And each time it kind of
[15:11] approaches. And each time it kind of tests if that new approach or ability or
[15:14] tests if that new approach or ability or
[15:14] tests if that new approach or ability or whatever improves its ability to code.
[15:16] whatever improves its ability to code.
[15:16] whatever improves its ability to code. And they use the SUI bench, a benchmark
[15:19] And they use the SUI bench, a benchmark
[15:19] And they use the SUI bench, a benchmark in this case to see if it does better on
[15:21] in this case to see if it does better on
[15:21] in this case to see if it does better on it. That means it improved. And over
[15:23] it. That means it improved. And over
[15:24] it. That means it improved. And over time it uses kind of this evolutionary
[15:25] time it uses kind of this evolutionary
[15:26] time it uses kind of this evolutionary approach, right? So there's a certain
[15:28] approach, right? So there's a certain
[15:28] approach, right? So there's a certain ideas that when they work, it continues
[15:30] ideas that when they work, it continues
[15:30] ideas that when they work, it continues trying to find more ideas kind of in
[15:32] trying to find more ideas kind of in
[15:32] trying to find more ideas kind of in that direction. And these form certain
[15:35] that direction. And these form certain
[15:35] that direction. And these form certain lineages. Some of them kind of go
[15:37] lineages. Some of them kind of go
[15:37] lineages. Some of them kind of go extinct cuz they're dead ends. It it
[15:39] extinct cuz they're dead ends. It it
[15:39] extinct cuz they're dead ends. It it doesn't work to improve it. That's fine
[15:41] doesn't work to improve it. That's fine
[15:41] doesn't work to improve it. That's fine because some of them are real champion
[15:44] because some of them are real champion
[15:44] because some of them are real champion lineages that come up to create the best
[15:46] lineages that come up to create the best
[15:46] lineages that come up to create the best possible outcomes. Here's the progress.
[15:48] possible outcomes. Here's the progress.
[15:48] possible outcomes. Here's the progress. As you can see here, goes up. you know,
[15:50] As you can see here, goes up. you know,
[15:50] As you can see here, goes up. you know, test a bunch of different stuff and but
[15:51] test a bunch of different stuff and but
[15:52] test a bunch of different stuff and but every once in a while just jumps up in
[15:54] every once in a while just jumps up in
[15:54] every once in a while just jumps up in its ability. All this is kind of
[15:55] its ability. All this is kind of
[15:56] its ability. All this is kind of suggesting the same thing that we're
[15:58] suggesting the same thing that we're
[15:58] suggesting the same thing that we're beginning this self-recursive process of
[16:01] beginning this self-recursive process of
[16:01] beginning this self-recursive process of these models improving themselves.
[16:03] these models improving themselves.
[16:03] these models improving themselves. Smaller models are better at teaching
[16:05] Smaller models are better at teaching
[16:05] Smaller models are better at teaching the next generation models. These models
[16:08] the next generation models. These models
[16:08] the next generation models. These models with certain scaffolding are better at
[16:10] with certain scaffolding are better at
[16:10] with certain scaffolding are better at creating tools for itself to improve
[16:12] creating tools for itself to improve
[16:12] creating tools for itself to improve itself. And we're going to be seeing a
[16:14] itself. And we're going to be seeing a
[16:14] itself. And we're going to be seeing a lot more of this moving forwards because
[16:16] lot more of this moving forwards because
[16:16] lot more of this moving forwards because in effect we're now letting AI handle
[16:20] in effect we're now letting AI handle
[16:20] in effect we're now letting AI handle some of the AI research, some of the
[16:22] some of the AI research, some of the
[16:22] some of the AI research, some of the machine learning research. We're still
[16:24] machine learning research. We're still
[16:24] machine learning research. We're still in the early stages of that, but I feel
[16:26] in the early stages of that, but I feel
[16:26] in the early stages of that, but I feel like it's going to get faster and faster
[16:28] like it's going to get faster and faster
[16:28] like it's going to get faster and faster and kind of like build on itself. It's
[16:30] and kind of like build on itself. It's
[16:30] and kind of like build on itself. It's going to start to snowball. Let me know
[16:32] going to start to snowball. Let me know
[16:32] going to start to snowball. Let me know what you think about this. Will the
[16:34] what you think about this. Will the
[16:34] what you think about this. Will the markets react to this just like they did
[16:36] markets react to this just like they did
[16:36] markets react to this just like they did to the deepseek originally by losing a
[16:39] to the deepseek originally by losing a
[16:39] to the deepseek originally by losing a trillion dollars of global market caps
[16:41] trillion dollars of global market caps
[16:41] trillion dollars of global market caps in a day? Or is the fact that now a $7
[16:44] in a day? Or is the fact that now a $7
[16:44] in a day? Or is the fact that now a $7 billion model can train a much better
[16:47] billion model can train a much better
[16:47] billion model can train a much better model. Could that also imply that it's
[16:49] model. Could that also imply that it's
[16:49] model. Could that also imply that it's going to be a lot more accessible to
[16:51] going to be a lot more accessible to
[16:51] going to be a lot more accessible to everyday people and more researchers and
[16:54] everyday people and more researchers and
[16:54] everyday people and more researchers and smaller labs? It's going to allow them
[16:56] smaller labs? It's going to allow them
[16:56] smaller labs? It's going to allow them to jump in and start training their own
[16:58] to jump in and start training their own
[16:58] to jump in and start training their own models using Sakana AI's approach. Let
[17:01] models using Sakana AI's approach. Let
[17:01] models using Sakana AI's approach. Let me know what you think. I'm curious to
[17:03] me know what you think. I'm curious to
[17:03] me know what you think. I'm curious to know what you think of this, how big it
[17:05] know what you think of this, how big it
[17:05] know what you think of this, how big it is. Again, we've yet to see how the
[17:06] is. Again, we've yet to see how the
[17:06] is. Again, we've yet to see how the other labs sort of react to this. They
[17:08] other labs sort of react to this. They
[17:08] other labs sort of react to this. They announced it just within the last 24
[17:11] announced it just within the last 24
[17:11] announced it just within the last 24 hours. And since they're not as well
[17:14] hours. And since they're not as well
[17:14] hours. And since they're not as well known as Google and OpenAI and
[17:17] known as Google and OpenAI and
[17:17] known as Google and OpenAI and Anthropic, maybe it'll take a while for
[17:19] Anthropic, maybe it'll take a while for
[17:19] Anthropic, maybe it'll take a while for this news to kind of percolate through
[17:21] this news to kind of percolate through
[17:21] this news to kind of percolate through the industry. But make no mistake,
[17:23] the industry. But make no mistake,
[17:23] the industry. But make no mistake, Sakana AI tends to hit above their
[17:26] Sakana AI tends to hit above their
[17:26] Sakana AI tends to hit above their weight. Notice they've published
[17:27] weight. Notice they've published
[17:27] weight. Notice they've published everything on GitHub. This is open
[17:30] everything on GitHub. This is open
[17:30] everything on GitHub. This is open source. This code, this everything is
[17:33] source. This code, this everything is
[17:33] source. This code, this everything is available to everyone. It even has the
[17:35] available to everyone. It even has the
[17:35] available to everyone. It even has the one thing that none of us can resist,
[17:37] one thing that none of us can resist,
[17:37] one thing that none of us can resist, and that is the cutesy anime characters.
[17:39] and that is the cutesy anime characters.
[17:39] and that is the cutesy anime characters. Not sure why they made this one look
[17:41] Not sure why they made this one look
[17:41] Not sure why they made this one look sad. Let me know what you think. My name
[17:42] sad. Let me know what you think. My name
[17:42] sad. Let me know what you think. My name is Wes Roth and I'll see you next


## Quality Analysis

- **Total Lines:** 913
- **Unique Lines:** 913
- **Duplicate Lines:** 0
- **Quality Score:** 100.0%

### ✅ High Quality Transcript

No duplicate lines detected.



## MCP Resource Usage

This transcript can be used as an MCP resource:

### Resource URI
```
transcript://2mezj14pCFI
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
