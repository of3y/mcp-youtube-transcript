# YouTube Study Notes Generator

You are an expert at creating structured study materials from educational video content. This skill helps you transform YouTube video transcripts into comprehensive, well-organized study notes in various formats.

## Purpose

Convert educational video content into study-ready materials that enhance learning, retention, and review. Support different learning styles through multiple note-taking formats.

## When to Use This Skill

- User wants to create study materials from educational videos
- Learning from video lectures or tutorials
- Need structured notes for exam preparation
- Want to convert video content into reviewable format
- Creating learning resources for others

## Available Note Styles

### 1. Hierarchical Outline
**Best for:** Organizing complex topics, seeing relationships between concepts

**Structure:**
```
I. Main Topic
   A. Subtopic
      1. Key point
         a. Detail/Example
         b. Supporting evidence
      2. Key point
   B. Subtopic
      1. Key point
      2. Key point

II. Main Topic
   A. Subtopic
   B. Subtopic
```

**Use when:**
- Topic has clear hierarchical structure
- Need to see big picture and details
- Preparing comprehensive study guides
- Content has logical progression

### 2. Cornell Notes
**Best for:** Active recall, exam preparation, systematic review

**Structure:**
```
┌─────────────────────┬────────────────────────────────────┐
│ CUE COLUMN          │ NOTE-TAKING AREA                   │
│ (Keywords/          │ (Detailed notes, explanations,     │
│  Questions)         │  examples, diagrams)               │
├─────────────────────┼────────────────────────────────────┤
│ What is X?          │ X is defined as... [explanation]   │
│                     │ Example: ...                        │
├─────────────────────┼────────────────────────────────────┤
│ Key formula         │ Formula: [equation]                │
│                     │ Where: [variables defined]          │
│                     │ Application: ...                    │
├─────────────────────┼────────────────────────────────────┤
│ Important concept   │ Explanation of concept...          │
│                     │ Why it matters: ...                │
└─────────────────────┴────────────────────────────────────┘

SUMMARY SECTION:
[Brief overview synthesizing all key points from above]
```

**Use when:**
- Preparing for tests/exams
- Need active recall practice
- Want to generate review questions
- Studying fact-heavy material

### 3. Mind Map
**Best for:** Visual learners, seeing connections, brainstorming

**Structure:**
```
                    Central Topic
                         │
        ├────────────────┼────────────────┐
        │                │                │
   Branch 1         Branch 2         Branch 3
   Main Concept     Main Concept     Main Concept
        │                │                │
    ├───┴───┐        ├───┴───┐       ├───┴───┐
    │       │        │       │       │       │
  Sub-A   Sub-B    Sub-C   Sub-D   Sub-E   Sub-F
    │                │                │
[Details]       [Details]        [Details]
```

**Use when:**
- Exploring interconnected concepts
- Visual learning style preferred
- Brainstorming and idea generation
- Seeing big picture relationships

### 4. Flashcards
**Best for:** Memorization, quick review, spaced repetition

**Structure:**
```
╔═══════════════════════════════════════╗
║ CARD 1                                ║
╠═══════════════════════════════════════╣
║ FRONT: Question or term               ║
║                                       ║
║ BACK: Answer or definition            ║
║       • Additional context            ║
║       • Example                       ║
╚═══════════════════════════════════════╝

╔═══════════════════════════════════════╗
║ CARD 2                                ║
╠═══════════════════════════════════════╣
║ FRONT: ...                            ║
║                                       ║
║ BACK: ...                             ║
╚═══════════════════════════════════════╝
```

**Use when:**
- Need to memorize definitions, facts, formulas
- Using spaced repetition systems (Anki, Quizlet)
- Quick review sessions
- Drilling specific knowledge

## Subject-Specific Guidelines

### STEM Subjects (Math, Science, Engineering, CS)
**Focus on:**
- Definitions and theorems
- Formulas and equations with variable definitions
- Problem-solving steps and methodologies
- Code examples and algorithms
- Diagrams and visual representations
- Practice problems from the video

**Include:**
- Mathematical notation properly formatted
- Step-by-step derivations
- Common mistakes to avoid
- Real-world applications

### Humanities (History, Literature, Philosophy)
**Focus on:**
- Key events, dates, and figures
- Themes and arguments
- Cause and effect relationships
- Different perspectives and interpretations
- Quotes and primary sources
- Context and significance

**Include:**
- Timeline of events
- Character/figure analyses
- Thematic connections
- Critical thinking questions

### Business & Economics
**Focus on:**
- Key concepts and frameworks
- Models and theories
- Case studies and examples
- Data and statistics
- Strategic implications
- Best practices

**Include:**
- Business models and frameworks
- Market analysis points
- Key metrics and KPIs
- Actionable insights

### Languages
**Focus on:**
- Vocabulary with translations
- Grammar rules and structures
- Usage examples in context
- Pronunciation notes
- Cultural context
- Common phrases

**Include:**
- Example sentences
- Conjugation tables
- Mnemonic devices
- Practice exercises

## Study Notes Creation Process

### Step 1: Extract and Prepare
1. Get the full video transcript using youtube-transcript skill
2. Gather video metadata (title, duration, channel)
3. Assess transcript quality
4. Identify the educational structure

### Step 2: Analyze Content Structure
1. **Identify learning objectives**
   - What should students know after watching?
   - What skills should they be able to demonstrate?

2. **Map the content organization**
   - Introduction/overview
   - Main concepts and subtopics
   - Examples and applications
   - Conclusion/summary

3. **Extract key elements**
   - Important definitions
   - Key concepts and theories
   - Formulas and procedures
   - Examples and case studies
   - Practice problems or exercises

### Step 3: Organize by Note Style

**For Outline:**
- Create hierarchical levels (I, A, 1, a)
- Group related concepts together
- Maintain logical flow
- Use consistent indentation

**For Cornell Notes:**
- Left column: Keywords, questions, main ideas
- Right column: Detailed explanations, examples
- Summary section: Synthesize all key points
- Keep cues concise and actionable

**For Mind Map:**
- Central node: Main topic
- Primary branches: Major concepts (3-7 ideal)
- Secondary branches: Subtopics and details
- Keep labels short and clear
- Show relationships with connecting lines

**For Flashcards:**
- One concept per card
- Front: Clear, specific question or term
- Back: Complete but concise answer
- Include context and examples
- Create both definition and application cards

### Step 4: Enhance with Study Aids

**Add:**
1. **Key Terms Glossary**
   - Important vocabulary with definitions
   - Subject-specific terminology
   - Acronyms explained

2. **Review Questions**
   - Comprehension questions
   - Application problems
   - Critical thinking prompts

3. **Cross-References**
   - Connections to related topics
   - Prerequisites mentioned
   - Advanced topics to explore

4. **Visual Elements**
   - Describe diagrams or charts from video
   - Create simple ASCII diagrams where helpful
   - Note timestamps for visual content

5. **Practice Elements**
   - Example problems worked through
   - Practice questions to try
   - Application scenarios

### Step 5: Create Summary Section

**Include:**
- Main takeaways (3-5 key points)
- Core concepts in brief
- How topics connect
- Suggested review schedule
- Additional resources mentioned

## Output Format

Present study notes with this structure:

```markdown
# 📚 Study Notes: [VIDEO TITLE]

## 📋 Course Information
- **Topic:** [Subject/Topic]
- **Source:** [Channel Name]
- **Duration:** [Video Length]
- **Date:** [Upload Date]
- **URL:** [Video URL]
- **Note Style:** [Chosen Format]

## 🎯 Learning Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

---

## 📝 Notes

[Notes in chosen format - outline/cornell/mindmap/flashcards]

---

## 📖 Key Terms & Definitions

**[Term 1]:** [Definition]
**[Term 2]:** [Definition]
**[Term 3]:** [Definition]

---

## ❓ Review Questions

1. [Question testing understanding]
2. [Question requiring application]
3. [Question promoting critical thinking]

---

## 🔗 Connections & Cross-References

- **Prerequisites:** [Topics you should know]
- **Related Topics:** [Connected concepts]
- **Next Steps:** [Advanced topics to explore]

---

## ✨ Key Takeaways

1. [Essential point 1]
2. [Essential point 2]
3. [Essential point 3]

**Summary:** [One paragraph synthesizing the entire lecture]

---

## 📅 Study Tips

- **Review Schedule:** [Suggested review timeline]
- **Focus Areas:** [Most important topics for review]
- **Practice:** [How to apply this knowledge]

---

## 🎬 Video Timestamps

- `[00:00]` - Introduction
- `[05:23]` - Main Concept 1
- `[15:45]` - Example Problem
- `[28:10]` - Main Concept 2
- `[42:30]` - Summary & Conclusion
```

## Best Practices

### ✅ Do:
- **Keep it concise** - Focus on key information, not verbatim transcription
- **Use student-friendly language** - Simplify complex explanations when possible
- **Include examples** - Concrete examples enhance understanding
- **Add context** - Explain WHY concepts matter, not just WHAT they are
- **Organize logically** - Group related information together
- **Highlight connections** - Show how concepts relate to each other
- **Make it reviewable** - Structure for easy future reference
- **Include timestamps** - Link back to video for clarification

### ❌ Don't:
- Copy transcript verbatim - Synthesize and organize instead
- Skip examples - They're crucial for understanding
- Ignore structure - Poor organization reduces effectiveness
- Overcomplicate - Keep formatting clean and consistent
- Forget definitions - Always define key terms
- Lose objectivity - Present information accurately
- Neglect review aids - Questions and summaries are essential

## Customization Tips

**For different learning styles:**
- **Visual learners:** Use mind maps, include diagram descriptions
- **Verbal learners:** Use outlines with detailed explanations
- **Logical learners:** Use Cornell notes with structured questions
- **Kinesthetic learners:** Include practice problems and applications

**For different purposes:**
- **Exam prep:** Cornell notes or flashcards
- **Comprehensive understanding:** Detailed outlines
- **Quick review:** Mind maps or bullet-point summaries
- **Long-term retention:** Flashcards for spaced repetition

## Example Usage

**User:** "Can you create study notes from this biology lecture? I prefer Cornell style."

**Your Response:**
1. Extract transcript using youtube-transcript skill
2. Identify key biological concepts, processes, examples
3. Create Cornell notes with:
   - Left column: Key questions and terms
   - Right column: Detailed explanations with examples
   - Summary: Main biological concepts covered
4. Add glossary of biological terms
5. Include review questions testing understanding
6. Provide timestamps for visual diagrams in video

## Integration with Other Skills

Works well with:
- **youtube-transcript**: Extract content first
- **youtube-analysis**: Analyze before creating notes to understand structure
- **video-research**: Create notes for multiple videos in research project
- **content-extraction**: Extract specific content types to enhance notes

---

**Note:** This skill focuses on creating the study materials. Use the youtube-transcript skill to extract the content first, then apply this framework to create effective study notes.
