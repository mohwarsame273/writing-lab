# Writing Lab: Gamified Writing Grammar

Research-informed product proposal for BPP

Prepared for Mohamed Warsame, Head of AI Learning • 6 September 2026

## Decision in brief

Develop Writing Lab as a place where learners build useful written artefacts, practise the decisions behind them, and assemble evidence of increasing capability. Its central promise should be: **develop the judgement to compose, improve and defend writing, both independently and with AI.**

The strongest initial product is an academic and professional writing studio for BPP learners, with an accessible practice environment and a concise evidence portfolio. Start with evidence-based paragraphs and recommendations. Retain literary writing as a later extension of the same activity system. Trying to cover every genre, every language level and every BPP assessment immediately would dilute the curriculum and its evaluation.

Your sentence scaffold supplies a distinctive foundation: it connects rhetorical purpose, sentence construction and learner choice. Turn that into an activity grammar with reusable rules for what the learner does, what assistance is available, what artefact results and what later performance would demonstrate learning. Gamification should encourage those activities and make capability visible.

Three decisions follow. First, design **Practise, Co-create and Demonstrate** as connected experiences with explicitly different evidence conditions. Second, replace a single mastery percentage with supported performance, independent practice and verified demonstration records. Third, keep the Python learning engine and test a richer React editor; adopt Next.js for production only if its engineering advantages are demonstrated against an equivalent Reflex implementation.

This proposal is an evidence-informed design, not a validated intervention. It combines a review of the 14 application files and the supplied workbook with academic research, accessibility standards, institutional assessment guidance and current product documentation. It assumes UK adult HE and apprenticeship contexts. BPP strategy is taken from your brief; no unpublished institutional policy, learner interviews or platform performance tests were available.

## Personas: whose problem should the product solve?

These are **provisional, needs-based personas for validation**, not demographic stereotypes or diagnoses. A learner may fit several at different times. Ask what makes writing difficult and what support they prefer; do not require disclosure of a disability or infer ability from nationality, accent or writing speed. Jisc's student research supports the importance of clear course-specific AI guidance, equitable access and inclusive support, but does not validate these particular BPP personas. [Jisc, 2025](https://www.jisc.ac.uk/reports/student-perceptions-of-ai-2025)

| Persona and priority | Job to be done and barrier | Valuable experience and success evidence |
|---|---|---|
| Knowledgeable but blocked writer — primary | “I understand the topic but cannot turn it into a clear paragraph.” Blank-page anxiety; competing ideas; uncertain sentence purpose. | Begin with a claim, spoken note or fragment. Reveal one scaffold at a time. Success: a coherent new paragraph with less instructional help. |
| Multilingual / ESOL professional — primary | “My reasoning is stronger than my written English.” Needs genre conventions, collocations or qualification language without losing meaning or identity. | Optional bilingual planning and explanations; separate reasoning feedback from language feedback. Success: accurate expression of the same reasoning in a new English task. |
| Returning learner or apprentice — primary | “I can do the job but struggle to evidence and explain it.” Limited study time; experience does not automatically become an analytical account. | Short authentic case missions; convert workplace observations into evidence and justified recommendations. Success: clearer explanations in a different case, within a manageable routine. |
| Writer facing reading, attention or transcription barriers — primary access requirement | “I lose the thread, misread dense feedback or cannot comfortably type.” Needs vary; diagnosis alone does not identify the solution. | Focus view, read-aloud, dictation, stable layout, draft recovery and predictable steps. Success: completing the same intellectual task with appropriate access support. |
| Fluent writer who delegates too readily — primary pilot subgroup | “I produce polished work with AI but cannot always defend it.” May confuse output quality with understanding. | Audit plausible AI mistakes; justify a changed claim; tackle a fresh case. Success: detecting unsupported reasoning and independently correcting it. |
| Confident writer seeking precision — secondary | “Generic grammar advice is too basic.” Wants stronger synthesis, argument, judgement and audience adaptation. | Skip entry drills through a diagnostic; work with conflicting evidence and competing interpretations. Success: defensible synthesis, not merely shorter prose. |
| Creative or leisure writer — later expansion | “I want voice, image and rhythm without formulaic correction.” Literary goals differ from evidence-based professional prose. | Optional craft missions and free composition with contextual critique. Success: intentional choices and reader effects, using genre-specific criteria. |

The institutional users have different jobs. **Tutors** need a short account of misconceptions and consequential revisions, not every interaction. **Learning designers** need reusable activities that connect to programme outcomes. **Assessors** need appropriately bounded evidence and clear support conditions. **Accessibility and language specialists** need control over adaptations and routes for challenging harmful feedback. **BPP leaders and employer partners** need evidence of transferable capability, equitable participation and manageable delivery costs.

For the first pilot, recruit across the first five needs, including intersections: for example, an experienced multilingual apprentice who uses dictation. Include learners who dislike games and learners who already use AI confidently. “Would you use this?” interviews are insufficient; observe them completing an actual writing task and returning to it later.

## Value proposition and position in an AI-enabled education experience

Writing Lab should connect course learning, writing practice, authentic production and capability assurance. Its place is between studying material and submitting polished work. A learner might read a BPP case, discover that their conclusion overstates the evidence, practise qualification, revise the case recommendation and later demonstrate that skill on another case.

There are two outcomes to preserve: **learning to write** and **writing to learn the subject**. A student may improve grammar without understanding the subject better, or develop a stronger explanation while still needing language support. The app should make both visible without collapsing them into one score.

Writing is more than a by-product of thinking: composing can help people organise, examine and develop ideas. A meta-analysis of 56 school-based experiments found a positive effect of writing about subject content on learning, with an effect size of 0.30. It does not establish that reduced writing inevitably produces general cognitive deterioration, and it is not direct evidence about BPP adults. A higher-education-oriented research synthesis explains how prompted writing can support organisation, elaboration and self-monitoring. [Graham, Kiuhara and MacKay, 2020](https://doi.org/10.3102/0034654320914744); [Nückles et al., 2020](https://link.springer.com/article/10.1007/s10648-020-09541-1)

The design principle is therefore to preserve consequential intellectual activity: selecting a claim, connecting evidence, recognising uncertainty, choosing language and evaluating a revision. Speech, visual planning and assistive technology can support that activity. Requiring unaided keyboard transcription in every task would confuse the means of participation with the capability being developed.

Generic assistants already provide substantial overlap. ChatGPT Study Mode offers guided learning and knowledge checks; Claude Learning mode provides questions and writing templates; Microsoft's Study and Learn includes scaffolded conversations and interactive activities. Microsoft's May 2026 announcement states availability to education customers at no additional cost, subject to the relevant account arrangements. These are advertised capabilities, not independent efficacy findings. [OpenAI, 2025](https://openai.com/index/chatgpt-study-mode/); [Anthropic, 2025](https://www.anthropic.com/news/introducing-claude-for-education); [Microsoft, 2026](https://www.microsoft.com/en-us/education/blog/2026/05/study-and-learn-ai-built-for-your-student/)

| An assistant can already provide | Writing Lab's proposed additional value | Evidence needed to justify building |
|---|---|---|
| Exercises, explanations and coaching | An authored skill progression with known task objectives, misconceptions and return activities | Better independent transfer than equal-time use of a well-configured study assistant |
| Drafts, revisions and templates | A persistent artefact workspace joining purpose, sources, sentence choices and revision comparisons | Learners make useful revisions with less navigation and less lost context |
| Conversation history | A compact, permissioned record linking assistance, decisions, artefacts and later demonstrations | Tutors can interpret the record accurately without excessive review time |
| Personalised suggestions | Support that changes according to demonstrated skill, with access adjustments tracked separately | Scaffolds help novices and can fade without excluding users |
| Uploads and institutional integrations | BPP-owned outcomes, task bank, rubrics, moderation and evaluation | Reliable educational quality and a sustainable content-maintenance cost |

These are system-level differentiators, not capabilities competitors could never implement. If the pilot produces only a chat interface with points, extending BPP's existing assistant provision is likely to be the better investment. Stand-alone value means a coherent dedicated learning experience; it need not require a separate account, disconnected LMS or replacement of familiar document tools.

## The learning framework behind the design

Use a small set of complementary frameworks with distinct responsibilities. Avoid treating a collection of academic names as validation of the finished app.

| Framework or evidence | What it contributes | Design consequence and limit |
|---|---|---|
| Self-Regulated Strategy Development | Explicit strategies, modelling, goal setting, self-monitoring, supported practice and independence | Model one writing decision; let the learner practise and self-check it. Much of the evidence concerns school learners; validate adult adaptation. [Harris and Graham, 2016](https://doi.org/10.1177/2372732215624216) |
| ICAP | Distinguishes receiving, manipulating, generating and jointly developing ideas | Require an inference or explanation where useful. Clicking cards or chatting does not automatically constitute deep engagement. [Chi and Wylie, 2014](https://education.asu.edu/sites/g/files/litvpz656/files/lcl/chiwylie2014icap_2.pdf) |
| Adaptive scaffold fading | Support can become redundant as expertise develops | Remove a particular sentence stem after demonstrated competence; restore it for a harder genre if needed. Small HE studies support the principle, not a universal schedule. [Nückles et al., 2010](https://www.jsums.edu/english/files/2014/03/nuckles.pdf) |
| Retrieval practice | Retrieving studied material can improve delayed retention | Reconstruct a principle and apply it later to new prose. Memory findings do not by themselves establish transfer to whole-text writing. [Roediger and Karpicke, 2006](https://doi.org/10.1111/j.1467-9280.2006.01693.x) |
| Self-Determination Theory | Autonomy, competence and relatedness help explain motivation | Offer meaningful choices, criterion-based progress and optional peer contribution. The theory does not prescribe a particular points system. [Ryan and Deci, 2000](https://selfdeterminationtheory.org/SDT/documents/2000_RyanDeci_SDT.pdf) |
| Theory of Gamified Learning | Game mechanics should affect behaviour that contributes to learning | Specify the behaviour and learning mechanism behind each reward. Strong instructional content comes first. [Landers, 2014](https://doi.org/10.1177/1046878114563660) |
| UDL 3.0 | Anticipates variation in engagement, representation and expression | Build flexible routes from the outset and retain intellectual challenge. UDL is a design framework, not certification that an app is accessible. [CAST, 2024](https://udlguidelines.cast.org/) |

Gamification has encouraging but heterogeneous evidence. Sailer and Homner report pooled effects of g = 0.49 for cognitive outcomes, 0.36 for motivational outcomes and 0.25 for behavioural outcomes; the latter two were less stable in higher-rigour analyses. These are standardised effects, not percentage improvements or forecasts for Writing Lab. Their underlying search dates to 2017. Use the synthesis to justify testing learning-directed mechanics, not to promise a particular effect. [Sailer and Homner, 2020](https://link.springer.com/article/10.1007/s10648-019-09498-w)

AI evidence also resists a simple harm narrative. A high-school mathematics trial found that unrestricted AI improved supported performance but could impair subsequent unaided performance; tutor safeguards mitigated the problem. A July 2026 undergraduate working paper reports positive unaided knowledge outcomes and some delayed essay benefits after AI access. The latter is provisional and does not randomly assign the different ways students chose to use AI. Neither study establishes what this writing application will achieve. [Bastani et al., 2025](https://doi.org/10.1073/pnas.2422633122); [Contractor and Reyes, 2026, preprint](https://arxiv.org/abs/2607.08849)

Feedback quality must be evaluated through uptake. A 2026 study involving 70 university students found that more elaborate AI feedback did not produce significantly larger revision gains between conditions. Its title should not be read as proof that AI universally reduces revision. For ESOL support, a meta-analysis of 21 studies found that written corrective feedback can improve grammatical accuracy, with contextual moderators; this does not demonstrate improvement in every aspect of writing. [Farrokhnia et al., 2026](https://link.springer.com/article/10.1186/s41239-026-00579-9); [Kang and Han, 2015](https://doi.org/10.1111/modl.12189)

## Gamified Writing Grammar: the reusable activity system

Here, “grammar” means the rules for constructing useful learning experiences. It includes language grammar but extends to rhetoric, evidence, revision and judgement. The following specification is an original design synthesis to test, not an established named methodology.

**A mission has a purpose, a writing move, source material, an action, an assistance condition, a resulting artefact, feedback and a return task.** Its default rhythm is: establish purpose; inspect or retrieve; decide and compose; receive a challenge; revise; explain a consequential choice; return later on new material. These are composable stages, not seven compulsory screens.

### The skill structure

| Layer | Examples | What successful performance means |
|---|---|---|
| Sentence control | Finite clauses, reference, agreement, punctuation, qualification and sentence combining | Express the intended proposition accurately and readably |
| Rhetorical moves | Claim, definition, contrast, mechanism, evidence, limitation and implication | Make the sentence or paragraph do a recognisable job for the reader |
| Relationships and argument | Warrants, causal limits, synthesis, counterarguments and paragraph sequence | Connect ideas defensibly rather than merely place them together |
| Genre and audience | Academic introduction, analytical recommendation, workplace explanation and later literary scene | Adapt structure and register while preserving relevant meaning |
| Self-regulation and AI judgement | Planning, feedback uptake, source verification, tool choice and revision evaluation | Decide what needs improving and whether assistance actually helps |

The first four layers describe writing capability. The fifth describes how the learner manages writing and AI. Keep its evidence distinct: good prompting does not compensate for an unsupported argument. Link skills to programme outcomes, but do not claim that a narrow drill certifies a broad professional competence.

### Rhetorical move cards

Retain the workbook's purpose-first approach. Each card has a plain-language question, an optional fragment, a short example, a common failure and a criterion. Several moves may coexist in a sentence; learners may change the order or reject a proposed move.

| Move family | Learner's question | Constraint that creates a useful challenge |
|---|---|---|
| Context / chronology | What does the reader need to know, and what changed? | Select only background needed for this argument; distinguish sequence from cause |
| Definition / claim | What exactly do I mean or assert? | Define the scope and make the proposition open to scrutiny |
| Contrast / trade-off | Along which dimension do these options differ? | Compare like with like; name what is gained and given up |
| Cause / mechanism | Why might this happen, and through what process? | Separate a proposed explanation from demonstrated causality |
| Evidence / warrant | What supports this, and why does it support it? | Link a source passage to the claim; expose the inferential bridge |
| Problem / consequence / stake | What is wrong, by which standard, and for whom? | State the affected outcome and avoid unsupported alarm |
| Tension / counterargument | Which goals or interpretations compete? | Present the strongest relevant alternative fairly |
| Condition / limitation | When does this claim hold or fail? | Preserve a qualification that changes the conclusion |
| Gap / question | What remains uncertain? | Distinguish an absence of evidence from evidence of absence |
| Implication / recommendation | What follows, and what should someone do? | Make the proposed action proportionate to the evidence |

### Reusable activity contract

Authors need a content schema, not a collection of loosely worded prompts. Each activity definition should contain the following fields.

| Field group | Required content |
|---|---|
| Identity and purpose | Activity ID/version; target skill; learning outcome; genre; audience; prerequisite knowledge |
| Material and validity | Source pack/version; permitted claims; counterexamples; acceptable answer range; common misconceptions |
| Learner work | Starting artefact; exact action; output type; meaning constraints; completion criterion |
| Assistance | Available scaffold levels; reveal conditions; access supports; co-creation permissions; model-example policy |
| Feedback and progression | Rule checks; interpretive rubric; one priority intervention; retry branch; independent variant; return rule |
| Evidence and quality | Captured decisions; submission version; assessment conditions; reviewer status; known limits; accessibility equivalent |

For a causal-language activity, for example: target = calibrating claims; material = an authored observational case; action = revise one overstatement; invariant = preserve reported quantities; acceptable range = association or explicitly tentative explanation; feedback = ask what the design can establish; return task = a different case after a delay. This contract is precise enough for humans to author and AI to generate bounded variants.

### The activity catalogue

| Activity | What the learner actually does | Artefact and feedback |
|---|---|---|
| Identify the move | Labels a sentence's role, then explains one ambiguous choice | Annotated passage; accepts defensible multiple roles |
| Build a complete thought | Supplies a missing subject, finite verb or complement while preserving the idea | Learner-written sentence; explains the grammatical relationship |
| Combine and qualify | Combines short propositions while retaining an exception or condition | Combined sentence; flags lost meaning, not just length |
| Choose the precise verb | Selects or supplies “suggests”, “shows” or another verb against actual evidence | Calibrated claim; explains strength of inference |
| Repair the reference | Resolves an ambiguous “this”, pronoun or noun phrase | Clearer passage; checks what the reference points to |
| Make the comparison fair | Selects a common dimension and rewrites an uneven comparison | Comparison pair; identifies mismatched populations or outcomes |
| Fill the warrant | Explains why a supplied finding supports a claim | Inferential bridge; identifies missing assumptions |
| Audit a source link | Matches a claim to a passage, then narrows or withdraws it if needed | Claim-source pair; accepts “not supported” as success |
| Map the mechanism | Orders possible causal steps and distinguishes evidence from conjecture | Mechanism map plus prose explanation; challenges one link |
| Build the paragraph | Chooses rhetorical moves, orders them and writes the connective reasoning | Move map and paragraph; feedback on coherence and purpose |
| Synthesise disagreement | Combines two sources with different results or scopes | Synthesis paragraph; prevents a list of disconnected summaries |
| Challenge the AI editor | Accepts, adapts or rejects a fluent but flawed suggestion | Revision comparison and short reason; tests meaning and evidence |
| Change the audience | Explains the same finding to a specialist and a non-specialist | Two versions; checks stable facts and justified register changes |
| Defend a recommendation | Responds to counterevidence or an alternative proposal | Revised judgement; rewards warranted concession |
| Repair my own pattern | Applies a previously practised skill to an authorised excerpt of their draft | Personal revision; no claim of independent mastery from assisted work |
| Return and transfer | Produces or critiques new material without instructional hints | Fresh response; support conditions and delay recorded |

Sorts, choices and fill-in tasks are stepping stones. Progress must reach generation and application. A learner who recognises the right transition has not yet demonstrated that they can connect two ideas in their own paragraph.

## Turning the supplied spreadsheet into the experience

The workbook contains one sheet, “Introduction Scaffold”, with **22 sentence rows across six paragraph blocks**. Its eight columns are paragraph/artefact, fragment, finite verb, noun roles, modifiers, transition, sentence goal and the learner's sentence. It explicitly allows learners to change fragments, goals and sequence. Preserve that flexibility.

The most useful transformation is from eight simultaneous columns into progressive disclosure. Start with **“What should this sentence do?”**, the relevant source or note, and a writing space. “Help me start” reveals a fragment. “Help me construct it” reveals possible verb relationships and vocabulary. A more advanced learner can stay in an ordinary document view and open the same support only when needed.

| Workbook feature | Proposed product artefact | Important refinement |
|---|---|---|
| Paragraph / artefact | Editable paragraph-purpose map | Suggest a sequence; never require one universal introduction structure |
| Goal of sentence | Purpose card linked to a passage | Ask whether that goal still fits the argument |
| Fragment | Optional starter card | Leave the consequential content for the learner; allow complete rejection |
| Verb / noun / modifier choices | Construction aid with meaning labels | Distinguish subjects, objects and complements accurately; show certainty changes |
| Transition | Relationship selector | Choose the relationship before the connector; allow no explicit connector |
| Your sentence | Learner-owned draft and revision history | Keep the draft visible while feedback is applied |
| Missing from workbook | Source card and claim check | Prevent fluent completion of unsupported premises |
| Missing from workbook | Return task and evidence record | Check whether the skill survives removal of the scaffold |

The sheet should not become a factual answer key. Phrases such as “across every discipline”, “universally available” or “inevitably” need evidence. “Requires nothing more than a browser” also needs a defined scope. Some noun labels simplify grammatical relationships: an object of a preposition is not necessarily the direct object of the sentence's verb. Curriculum authors should review these labels before they become teaching content.

### Worked mission: from a claim to a defensible paragraph

**Mission:** write a short recommendation about a fictional workplace training pilot. This is an illustrative authored case, not evidence about BPP or a real intervention. Source card A states that 24 volunteers' average score rose from 52 to 67 after training, with no comparison group. Source card B states that the same assessment was repeated and six participants also received coaching.

**First decision:** the learner chooses the paragraph purpose: report a result, claim an effect or recommend a next step. If they write “The programme caused a 15-point improvement”, the coach asks, “What else could explain the change in this design?” It does not immediately supply the corrected paragraph.

**Construction support:** the learner can reveal “Scores increased following …, although …”. Another support card explains the difference between a temporal description and a causal claim. A source card highlights the absence of a comparison group without dictating the conclusion.

**Learner revision:** the learner rewrites the claim, links the design limitation to its implication, and proposes a proportionate next step. Multiple formulations are valid. The system checks preservation of the 15-point difference, awareness of alternative explanations and whether the recommendation follows.

**AI challenge:** a simulated editor offers an overconfident rewrite. The learner can reject it, adapt it or defend acceptance by identifying evidence. One brief reason is requested because this is the mission's target decision. Extensive reflection is not required on every edit.

**Return:** on a later visit, a new case changes the subject matter and evidence pattern. The learner must calibrate the new claim without the starter. A supervised programme checkpoint may subsequently sample the same skill under institutionally approved conditions. The record distinguishes all three performances.

### A first-session UX storyboard

| Moment | Learner experience | What the system does |
|---|---|---|
| Entry | “Practise a skill”, “Work on my writing” or “View my progress” | Shows course context and what support is available; avoids a diagnostic wall |
| Orientation | Chooses a relevant mission and optional access preferences | Offers a short baseline task or a skip route; does not diagnose the learner |
| First attempt | Reads or listens to the case and makes one writing decision | Saves the exact draft; postpones nonessential corrections |
| Coaching | Sees one anchored question next to their text | Prioritises the target skill; provides a support ladder |
| Revision | Edits with the original and feedback still available | Shows what changed and preserves undo; handles stale feedback anchors |
| Closure | Sees what they accomplished and one next step | Records supported success; offers a later fresh challenge |
| Return | Opens a new task related to an earlier difficulty | Explains why it was suggested and lets the learner choose another |

A short mission can take five to fifteen minutes, but this is a design range to test, not a countdown or learning guarantee. Permit pause and return. Avoid demanding a full rhetorical map when the learner only needs to repair one sentence.

## Assistance, co-creation and accessibility

Use separate settings for **instructional assistance**, **access support**, **assessment conditions** and **visible gamification**. These are not one Casual/Full switch. Hiding XP must not disable navigation history or useful learning records, while private free writing should offer a clearly explained non-portfolio route.

In Practise, the default assistance ladder is: task clarification; diagnostic question; cue; partial scaffold; annotated worked example. Novices may need modelling before their first attempt. After an example, use a different task for independent evidence. Assistance can be restored when the genre or subject becomes harder.

In Co-create, learners can request broader AI assistance where the task permits it. They identify intended meaning and source material, inspect alternatives, check claims and make consequential editorial decisions. A learner can use a plain-language request or a “Challenge this claim” control; sophisticated prompt syntax should not be an entry requirement. Show and allow editing of the generated request. Record both the visible user request and the assistance returned, with system configuration retained separately for audit.

| Access need | Product response | Assessment interpretation |
|---|---|---|
| Reading or visual access | Read-aloud, adjustable display, meaningful headings, reflow and screen-reader-compatible feedback | Reading aloud generally need not reduce evidence of composition; task-specific rules still apply |
| Motor or transcription access | Dictation, full keyboard operation, save/recovery and alternatives to drag-and-drop | Dictation may preserve composition evidence while changing what is inferred about independent spelling |
| Attention and cognitive load | One priority at a time, stable layout, concise instructions and optional focus view | Avoid grading speed, click counts or ability to manage visual clutter |
| Multilingual development | Optional first-language planning, bilingual explanations, glossaries and audience-aware English feedback | Distinguish reasoning from target-language production; record translation assistance where relevant |
| Hearing or speech access | Text alternatives for audio, editable transcripts, no mandatory spoken defence without an equivalent approved route | Assess the intended outcome; oral reasoning does not automatically demonstrate written communication |
| Limited connectivity or devices | Resilient local drafts, lightweight activities and retryable synchronisation | Connection failure is not failure of effort or competence |

Use WCAG 2.2 AA as an engineering target and test essential journeys with users of assistive technologies. Include keyboard access, visible/unobscured focus, contrast, zoom/reflow, understandable errors and accessible authentication. Every drag interaction needs an alternative; feedback must be available as text rather than colour alone. Do not make a conformance claim before auditing the actual application. [W3C, WCAG 2.2](https://www.w3.org/TR/WCAG22/); [W3C, dragging movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)

ESOL learners should not receive indiscriminate correction or a single “native-like” target. Offer distinct priorities: meaning, organisation, evidence and selected language patterns. A technically strong argument can coexist with developing English. Allow learners to contest a correction, retain an intentional voice and inspect the reason a change was suggested.

## Gamification that supports the work

The engaging element should be the act of solving a writing problem: defending a recommendation, resolving conflicting sources, repairing an ambiguous sentence or making a claim survive scrutiny. A light professional mission context can make the result matter without turning adult learning into a compulsory fantasy game.

| Mechanic | Intended behaviour and learning mechanism | Safeguard / measure |
|---|---|---|
| Choice of mission | Autonomy and personal relevance encourage purposeful practice | Observe actual return and task completion; allow a plain practice list |
| Visible skill routes | Learners see a manageable next challenge and growing competence | Show examples and evidence counts, not fictitious starting percentages |
| Revision milestone | Learners complete a meaningful attempt-feedback-revision cycle | Award once per meaningful cycle; no reward for repeated identical grading |
| Return challenge | Learners revisit a skill on fresh material | Recognise delayed participation and separately evaluate transfer |
| Consequence-based scenario | Language choices affect a simulated reader's interpretation | Label the reader response as simulation; judge with a rubric, not theatrical reactions |
| Optional peer editorial task | Learners explain criteria and respond to another perspective | Provide private or tutor alternatives; do not force public sharing |
| Personal progress collection | Learners retain useful before/after examples and strategies | Evidence belongs to the learner; no compulsory social ranking |

Keep XP optional and low stakes. Do not award it for word count, prompt length, accepting AI, reporting certainty or producing polished text quickly. Avoid lives, punitive daily streak resets and mandatory leaderboards. These exclusions are product judgements, not claims that competitive mechanics are universally ineffective. A weekly self-chosen practice goal may be more appropriate for apprentices and learners with fluctuating capacity.

Replace “55% mastered” with intelligible evidence states: **not yet sampled; practised with support; demonstrated in independent practice; demonstrated again after a delay; verified under stated assessment conditions**. Display the number and variety of observations, date and remaining uncertainty. “Verified” requires authorised assessment evidence; an unsupervised app exercise cannot confer it.

An initial scheduling rule could invite a fresh task a few days after success, extend the interval after further success and shorten it after difficulty. Exact intervals require evaluation. Start with transparent rules rather than an opaque adaptive model. Assisted retries are useful practice but should not count as multiple independent mastery observations. Access supports remain available as appropriate.

## Two lanes and the evidence of co-creation

Sydney's framework distinguishes secure assessment of learning from open assessment for/as learning. Secure assessment can permit examiner-controlled AI; it is not synonymous with “no AI”. Open assessment scaffolds available tools and, in Sydney's model, cannot ban or control AI. Its secure arrangements rely on in-person supervision. These are Sydney's institutional arrangements, not automatically BPP's policy. [Sydney Assessment Framework, 2025, updated 2026](https://educational-innovation.sydney.edu.au/teaching@sydney/the-sydney-assessment-framework/)

Sydney's April 2026 marker guidance explicitly separates developmental judgement in open work from the assurance provided by secure assessment. It cautions against inferring authorship or learning from polish. Writing Lab should make that boundary visible. A learner's prompt trail is useful process evidence, but is not a certificate of authorship or retained competence. [Sydney guidance for markers, 2026](https://educational-innovation.sydney.edu.au/teaching@sydney/guide-for-markers-of-open-assessments/)

| Experience | Purpose | Evidence status |
|---|---|---|
| Practise | Build skills through selected assistance and new tasks | Formative evidence; “no in-app hints” does not prove no external assistance |
| Co-create | Produce authentic work and develop evaluative judgement with AI | Observed process and artefact quality under stated conditions |
| Demonstrate | Sample capability under BPP-approved conditions and accommodations | Assessor-verified evidence only when the assessment arrangement warrants it |

These are product experiences, not a third institutional assessment lane. Voluntarily reducing in-app hints during practice is compatible with learning; do not present it as a prohibition on external AI in an open assessment following Sydney's model. Where BPP qualification rules differ, the task contract must state those rules explicitly.

For apprenticeships, the applicable assessment plan and assessment organisation remain decisive. Ofqual's April 2026 explanation describes new arrangements taking effect as plans are revised, including assessment-organisation oversight of provider responsibilities. Do not use a general AI co-creation policy to replace required methods or evidence. [Ofqual, 2026](https://ofqual.blog.gov.uk/2026/04/01/what-next-for-our-framework-for-apprenticeship-assessment/)

### The evidence packet

The useful unit is a **decision linked to a change and a learning outcome**, not an indiscriminate transcript. The default assessor view should contain the following.

| Element | Contents |
|---|---|
| Task contract | Outcome, task/rubric/source versions, permitted assistance, access arrangements and assessment conditions |
| Starting contribution | Initial claim, outline or draft; labelled platform-captured, imported or self-reported |
| Selected decision trail | Consequential prompt or control action, AI response, accepted/adapted/rejected decision and brief explanation |
| Artefact development | Exact submitted revision and a few meaningful before/after comparisons with source links |
| Learning evidence | Feedback uptake and a new-task result, including delay and support conditions |
| Human judgement | Tutor comment or authorised assessment judgement, including disagreement with the AI |

Capture meaningful events with stable IDs, revision references, server receipt times and configuration versions. A replay displays the stored artefacts and AI responses; it must not regenerate a supposedly identical conversation. External assistant histories may be imported, but must be labelled self-reported. A signed log can establish integrity after recording; it cannot establish who thought of the words or whether another device supplied them.

Do not request hidden AI chain-of-thought, infer a “human authorship percentage” or use keystroke surveillance as a proxy for cognition. The learner's short explanation is an educational artefact, not proof of an internal mental process. Sample explanations at consequential moments to avoid creating a second, burdensome essay about every essay.

Private notes, learning analytics and submitted assessment records need distinct access and retention rules. Let learners preview what is shared. Keep raw interactions available only to authorised users where needed; export a concise account first. BPP's data-protection team should determine lawful processing, retention, supplier arrangements and any required impact assessment. ICO's AI minimisation guidance supports limiting collection and retention to the purpose; it is currently marked as under review following legislative changes. [ICO, current guidance](https://ico.org.uk/for-organisations/advice-and-services/audits/data-protection-audit-framework/toolkits/artificial-intelligence/data-minimisation/)

## AI engineering and quality assurance

The durable asset is the authored learning system: skills, activities, source packs, rubrics and evidence interpretation. AI should generate variants within it. Separate coaching, exercise generation, contextual evaluation and co-creation permissions, even if they initially use the same underlying model.

The grader should distinguish mechanical checks from interpretation. Word count and missing fields are deterministic. Claim support, coherence and audience appropriateness require contextual judgement. Return evidence-linked feedback, plausible alternative readings and uncertainty where relevant. Do not silently substitute a keyword score for an unavailable contextual assessment; offer authored practice or clearly defer that judgement.

Before releasing a generated exercise, validate its schema, source grounding, answerability, target skill and acceptable answer range. Reject ambiguous selection questions without a defensible key. Teacher-reviewed templates can be reused with bounded variation; generation need not occur on every click. Keep source IDs through retrieval and grading and treat learner text and imported documents as untrusted data, not instructions to the evaluator.

Build a benchmark from educator-rated examples, including multilingual prose, intentional stylistic variation, dictation artefacts and fluent but unsupported answers. Measure false corrections, semantic distortion, missed unsupported claims, disagreement with human ratings and subgroup patterns. Provide “This feedback seems wrong” and human review routes. Version the model and rubric so updates do not invisibly redefine progress.

A suitable service boundary is: local editor and draft recovery; application API and identity; Python learning engine; AI gateway; persistent artefact and evidence store; institutional integration. LTI 1.3 and associated services can support LMS launch, roles, deep links and authorised grade return. XP should not be returned as an academic grade. [1EdTech, LTI](https://www.1edtech.org/standards/lti)

## Reflex or Next.js?

**For the ambitious production experience, favour a direct React/TypeScript editor with Next.js as the likely frontend, while retaining the Python core. For the immediate pilot, do not make rewriting the prerequisite.** The genuine advantage would be easier direct control of complex editor behaviour, not an automatic improvement in pedagogy, speed or accessibility.

Reflex supports local React/TypeScript components and explicitly identifies high-frequency input and browser APIs as cases for client-side handling. Next.js Client Components directly support browser state and events. Both can therefore implement the proposed experience. The difference to test is engineering effort, reliability and maintainability at the editor boundary. Current documentation does not establish compatibility with the prototype's pinned older Reflex version. [Reflex local components](https://reflex.dev/docs/wrapping-react/local-packages/); [Next.js Server and Client Components, August 2026](https://nextjs.org/docs/app/getting-started/server-and-client-components)

| Criterion | Retain Reflex | Next.js frontend with Python services |
|---|---|---|
| Short drills and small pilot | Fits the existing Python workflow | A rewrite may delay learning validation |
| Rich revision workspace | Feasible through a carefully wrapped editor | More direct ownership of editor state, anchors and interaction logic |
| Typing and recovery | Keep frequent input local inside the editor | Keep frequent input local in Client Components |
| Accessibility | Depends on the actual editor, controls and testing | Same; Next.js is not an accessibility guarantee |
| Team capacity | Preserves Python-centric development | Requires sustained TypeScript/frontend ownership and API maintenance |
| Migration risk | Lower immediate change; wrapper complexity may grow | Higher initial work; retain content, Python logic and evidence schemas |

Run one identical slice in both: draft a paragraph, receive an anchored question, revise, inspect a comparison, disconnect, reconnect and submit the exact latest revision. Test lower-end institutional devices, multilingual input composition, dictation, keyboard and screen-reader use. Acceptance requires no lost text or duplicated submissions in the test scenarios; correct or explicitly stale feedback anchors; and an intelligible evidence record. Agree measurable responsiveness targets before testing rather than inventing a speed claim now.

Migrate if Reflex requires disproportionate wrapper and synchronisation work or fails the agreed experience checks after a bounded fix attempt. Retain it if it passes at comparable effort. A prose editor such as a ProseMirror/Tiptap-based implementation is a candidate for investigation, not a mandatory purchase; neither a code editor nor a rich-text editor should be selected without task-level access testing. Start with versioned snapshots and a pending-save queue; add collaborative infrastructure only when concurrent editing justifies it.

## What to change in the current app

| Preserve | Change first | Defer or remove |
|---|---|---|
| Framework-independent Python core | Add persistent artefacts and separate support/evidence settings | Whole-framework rewrite before validating the learning journey |
| Short drills and optional topic focus | Introduce the purpose/claim/source activity contract | Unconstrained “generate anything” exercise creation |
| Free writing as a low-pressure space | Keep learner text visible during feedback and revision | Global diet labels as judgements of writing quality |
| Progressive hints | Delay automatic model rewrites in practice; retain modelling when needed | Penalising help-seeking through blanket XP deductions |
| Distinction between XP and mastery | Remove sample mastery; repair completion and repetition logic | Claiming streaks or spaced practice without their underlying records |
| Academic/literary ambition | Prioritise academic and workplace evidence-based writing | Simultaneous full literary curriculum and public social features |

The reviewed prototype has specific foundations to repair: Casual mode prevents completion history; focused repetition can repeatedly select the same completed item; bank progress mixes modes and generated IDs; failed attempts are treated as completion; and free-writing analysis can repeatedly award XP for unchanged text. These are source-level findings from the supplied files, not a new runtime audit. They matter because the redesigned progression must be trustworthy before adding more game mechanics.

## Delivery sequence and validation

Organise delivery around learning-risk reduction. The sequence below is a planning proposal, not a costed delivery commitment.

| Stage | Bounded deliverable | Decision gate |
|---|---|---|
| Discover and co-design | Observe 12–18 varied learners and several tutors using scaffold-based tasks; include access specialists | Can learners understand and use purpose-first support? Which steps add burden? |
| Build the learning slice | Three skill families: claim calibration, evidence/warrant links and paragraph coherence; authored variants; accessible editor; draft/decision record | Can users complete the core journey without lost work, inaccessible controls or misleading feedback? |
| Pilot in two contexts | One HE module and one apprenticeship context; formative use, real tasks, delayed checks and tutor summaries | Is there useful uptake, manageable tutor effort and credible independent improvement? |
| Comparative evaluation | Pre-registered, adequately powered comparison against existing study-assistant support | Is additional learning value large enough to justify cost and complexity? |
| Expand | More genres, calibrated adaptivity and approved programme integrations | Are content quality, access and evaluation maintained as scope grows? |

BPP needs named ownership for product decisions, writing curriculum, UX/accessibility, frontend engineering, Python/AI engineering, assessment and evaluation. Roles may be combined in a small team, but each responsibility must be explicit. Programme leaders must allocate space in teaching for the activity and subsequent discussion; an optional app link alone is a weak adoption strategy.

### Evaluation that can answer the investment question

The primary endpoint should be **blind-rated performance on an unseen writing task after practice, with a delayed follow-up**. Measure claim quality, evidence use, coherence and audience appropriateness separately from language accuracy. Include a subject-understanding measure where the intervention aims to improve disciplinary learning. Preserve approved access arrangements in every study arm.

The main comparison should use equal time, relevant materials and a credible alternative: Writing Lab versus BPP's available study assistant configured for writing support. Add usual provision if resources allow. Randomisation should account for baseline skill and teaching context; if classes are randomised, account for clustering. Calculate sample size from a pre-specified meaningful difference, expected variance, attrition and design effect. A small feasibility pilot cannot settle efficacy.

Use different prompts and source packs at baseline and follow-up, matched for difficulty. Keep assessment raters unaware of allocation, double-mark a sample and adjudicate disagreement. Report effect estimates and uncertainty, attrition, contamination and adverse experiences. Do not interpret within-arm improvement alone as an app effect. Check whether the intervention benefits those who need support and whether it creates new access barriers; small subgroups may only support descriptive findings.

Secondary measures should include feedback acted upon correctly, unsupported claims detected, transfer after scaffold removal, voluntary return, confidence calibration, learner burden, tutor review time and cost per active learner. Treat XP, prompt count, time on platform and polished AI-assisted output as process measures, not evidence of learning.

A later matched-content comparison with and without game mechanics can test gamification specifically. Otherwise any improvement belongs to the combined package of content, coaching, interface and practice. Likewise, compare scaffold policies directly before claiming that adaptive fading caused the gain.

### Investment and stop criteria

Track total cost: content authoring and review; frontend and service maintenance; model calls and storage; accessibility testing; staff training; and tutor review time. Compare the incremental cost against existing institutional assistant provision. The relevant efficiency measure is cost per additional learner reaching a pre-agreed capability standard, with uncertainty, rather than cost per generated exercise.

Continue if learners can use the experience, educators trust the feedback and evidence boundaries, and comparative evaluation supports worthwhile benefit at sustainable cost. Revise or stop if users mainly seek model answers, tutor packets create more burden than insight, unsupported grading persists, access barriers remain unresolved or a simpler assistant-based route performs as well. Keep the authored content and evaluation learning useful even if a stand-alone app is not justified.

## Additional core pattern: Interview my thinking

**Make a multi-step Q&A thinking assistant a first-class route into Co-create.** The learner can arrive with incomplete ideas, explain them in their own words, and work with AI to produce coherent text. The value is an inspectable connection between the conversation, the developing argument and the resulting prose. This is a proposed interaction pattern, not an independently validated intervention.

The assistant asks one focused question at a time, adapts to the answer, and maintains a visible, editable idea map. It should help a learner discover what they mean without quietly substituting its own argument. The learner can answer in prose, fragments or an editable dictated transcript; skip a question; correct the assistant; pause; or return to an earlier answer. No fixed number of turns is required.

### The interview and composition sequence

| Stage | Interaction | Resulting artefact |
|---|---|---|
| Establish intent | “Who will read this, and what should they understand or decide?” | Audience, purpose, genre and assistance conditions |
| Elicit the idea | “What is the main thing you want to say, in your own words?” | Original answer retained, alongside any later correction |
| Clarify and challenge | Ask about a missing mechanism, example, assumption, source or counterargument, selected from the actual answer | Linked answers and unresolved questions |
| Reflect back | “I understand your argument as these three points. What have I misunderstood?” | Learner-confirmed idea map; AI-inferred additions visibly separate |
| Build the structure | Offer a paragraph-purpose sequence and explain the proposed order | Editable outline with answer and source references |
| Choose composition support | Offer sentence stems, joint drafting of one paragraph, or an AI draft from the confirmed outline where permitted | Explicit assistance choice and corresponding draft |
| Review meaning | Ask whether the wording preserves the intended claim; surface qualifications, added claims and unsupported statements | Accepted, adapted or rejected suggestions linked to revisions |
| Consolidate and transfer | Offer one small writing task using the same move on a different topic | Separate practice evidence; never required merely to access one's draft |

Learner confirmation is required before the assistant treats an inferred idea as the learner's stated position. Approval of an AI-written sentence does not make its wording learner-authored. A new AI suggestion remains identified as such even when useful and accepted. The assistant should not invent references or turn uncertainty into certainty. When evidence is missing, it asks for a source, narrows the claim or leaves a visible evidence-needed marker.

### Example: a recommendation about AI-enabled assessment

The assistant asks: “What do you want BPP to change?” The learner replies: “Let students use AI but make sure they can explain the decisions.” The next question is tied to that answer: “Which decisions would show understanding in the task you have in mind?” The learner identifies the claim, the chosen evidence and a rejected alternative. The assistant then asks what would demonstrate those capabilities on a new problem. This exposes an assessment question before producing polished wording.

After reflection and confirmation, the workspace offers a three-part outline: the educational problem; the proposed co-creation process; the separate demonstration of capability. A sentence scaffold might begin, “The assessment should require learners to ___ because ___.” Alternatively, in permitted Co-create use, the learner can ask the assistant to draft a paragraph from the confirmed points. Both routes are useful; their records support different conclusions about composition.

### Contribution record and accessible interaction

Store the visible question, the learner's answer and its version, the assistant's proposed interpretation, the learner's confirmation or correction, the outline node, the generated suggestion and the accepted document revision. Each draft block links to the relevant answer, idea and source IDs. Mark links as system-proposed until checked; a semantic relationship is not a forensic authorship guarantee. When edits invalidate a link, mark it stale and request review. Do not display a human-contribution percentage.

For spoken answers, retain an editable transcript with correction history; do not retain raw audio by default. For multilingual planning, preserve the original answer and the translated interpretation separately and allow correction. Avoid forcing speech, dense parallel panels or repeated confirmation of trivial changes. A linear, keyboard-accessible view must expose the same questions, outline and provenance as the desktop workspace. Provide progress by meaningful stages, not a countdown of obligatory answers.

The implementation requires an explicit interview state machine and structured idea records rather than a chat transcript alone. Editing an earlier answer invalidates dependent confirmation and draft provenance until rechecked. A failed or cancelled model response must not advance the session. The server enforces assistance permissions; client controls alone are insufficient. Default to a short reflection checkpoint after several substantive answers, with an option to continue exploring.

Measure whether the assistant preserves intended meaning, asks relevant rather than repetitive questions, exposes unsupported claims, reduces composition barriers and helps learners later perform the targeted move. Include multilingual learners and people who prefer dictation or low-distraction interaction. Track inaccurate paraphrases and unnoticed additions as quality failures. Reward useful clarification and revision sparingly; never reward the number or length of interview answers. Prompt trails establish what occurred inside the tool, while independent performance and human judgement remain separate evidence of capability.

## Research limits and source notes

This was targeted decision research across three parallel lanes, followed by verification of consequential institutional, product and research claims. It was not a systematic review or an exhaustive market audit. Search families covered writing-to-learn, gamification theory and meta-analysis, scaffold fading, AI-assisted versus independent learning, ESOL feedback, accessibility, Sydney assessment and frontend capabilities. Discovery stopped when major decisions had primary support or an explicit uncertainty; further broad searching was unlikely to change the proposed pilot.

Personas have not been validated with BPP learners. The grammar, reward rules, scheduling, mission duration and success criteria are design hypotheses. No source establishes the efficacy of Writing Lab itself. Adult, ESOL and disability-related outcomes require direct testing, and neither policy alignment nor software accessibility can be certified from this proposal.

The supplied materials were ARCHITECTURE.md; README(1).md; documentation(1).md; layout.py; theme.py; writing_lab.py; lab_state.py; dashboard.py; free_write.py; practice.py; editor.py; feedback_panel.py; mastery.py; mode_toggle.py; and Introduction_Sentence_Scaffold.xlsx. The missing domain, AI-service and custom-editor implementations limit conclusions about the present system's educational quality and runtime behaviour.

### Academic references

- Graham, S., Kiuhara, S. A. and MacKay, M. (2020). The Effects of Writing on Learning in Science, Social Studies, and Mathematics: A Meta-Analysis. Review of Educational Research, 90(2), 179–226. Publisher and author-institution abstract reviewed; school-based evidence. [Article](https://doi.org/10.3102/0034654320914744)
- Nückles, M., Roelle, J., Glogger-Frey, I., Waldeyer, J. and Renkl, A. (2020). The Self-Regulation-View in Writing-to-Learn: Using Journal Writing to Optimize Cognitive Load in Self-Regulated Learning. Educational Psychology Review. Open research synthesis. [Article](https://link.springer.com/article/10.1007/s10648-020-09541-1)
- Nückles, M., Hübner, S., Dümer, S. and Renkl, A. (2010). Expertise reversal effects in writing-to-learn. Instructional Science, 38, 237–258. Original paper reviewed; small HE experiments. [Paper](https://www.jsums.edu/english/files/2014/03/nuckles.pdf)
- Harris, K. R. and Graham, S. (2016). Self-Regulated Strategy Development in Writing: Policy Implications of an Evidence-Based Practice. Policy Insights from the Behavioral and Brain Sciences. Evidence-based practice synthesis; adult extrapolation flagged. [Article](https://doi.org/10.1177/2372732215624216)
- Chi, M. T. H. and Wylie, R. (2014). The ICAP Framework: Linking Cognitive Engagement to Active Learning Outcomes. Educational Psychologist, 49(4), 219–243. Author-institution paper. [Paper](https://education.asu.edu/sites/g/files/litvpz656/files/lcl/chiwylie2014icap_2.pdf)
- Roediger, H. L. and Karpicke, J. D. (2006). Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention. Psychological Science, 17(3), 249–255. Original experiments; memory outcome distinguished from composition. [Article](https://doi.org/10.1111/j.1467-9280.2006.01693.x)
- Ryan, R. M. and Deci, E. L. (2000). Self-Determination Theory and the Facilitation of Intrinsic Motivation, Social Development, and Well-Being. American Psychologist, 55(1), 68–78. Author-hosted theory paper. [Paper](https://selfdeterminationtheory.org/SDT/documents/2000_RyanDeci_SDT.pdf)
- Landers, R. N. (2014). Developing a Theory of Gamified Learning: Linking Serious Games and Gamification of Learning. Simulation & Gaming, 45(6), 752–768. Theoretical model. [Article](https://doi.org/10.1177/1046878114563660)
- Sailer, M. and Homner, L. (2020; online 2019). The Gamification of Learning: a Meta-analysis. Educational Psychology Review, 32, 77–112. Open article; heterogeneous interventions and 2017 search. [Article](https://link.springer.com/article/10.1007/s10648-019-09498-w)
- Bastani, H. et al. (2025). Generative AI without guardrails can harm learning: Evidence from high school mathematics. PNAS, 122, e2422633122. Bounded finding reviewed through the research lane. A published correction exists; its full text was not accessible during verification and its contents are not assumed here. [Article](https://doi.org/10.1073/pnas.2422633122); [Correction](https://doi.org/10.1073/pnas.2518204122)
- Contractor, Z. and Reyes, G. (2026). Experimental Evidence on the Learning Impact of Generative AI. arXiv working paper, submitted 9 July. Not peer reviewed; randomised access differs from self-selected use strategy. [Preprint](https://arxiv.org/abs/2607.08849)
- Farrokhnia, M. et al. (2026). Generative AI offers more, but students revise less: comparing the effects of teacher and AI feedback on student essay revisions. International Journal of Educational Technology in Higher Education, published 10 February. Article inconsistently describes study level; reported here as university students. [Article](https://link.springer.com/article/10.1186/s41239-026-00579-9)
- Kang, E. and Han, Z. (2015). The Efficacy of Written Corrective Feedback in Improving L2 Written Accuracy: A Meta-Analysis. The Modern Language Journal, 99, 1–18. Publisher abstract reviewed; grammatical accuracy outcome. [Article](https://doi.org/10.1111/modl.12189)

### Institutional, accessibility and product sources

- Attewell, S. / Jisc (22 May 2025). Student perceptions of AI 2025. Discussion groups and survey synthesis; student experience, not causal efficacy. [Report](https://www.jisc.ac.uk/reports/student-perceptions-of-ai-2025)
- CAST (2024). Universal Design for Learning Guidelines 3.0. Design framework and language/action-expression guidance. [Guidelines](https://udlguidelines.cast.org/)
- W3C (2024 recommendation version). Web Content Accessibility Guidelines 2.2. Normative technical standard; consulted with the informative dragging-movements explanation. [Standard](https://www.w3.org/TR/WCAG22/); [Explanation](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)
- Bridgeman, A. and Liu, D. / University of Sydney (18 March 2025; page updated July 2026). The Sydney Assessment Framework. Official institutional guidance. [Framework](https://educational-innovation.sydney.edu.au/teaching@sydney/the-sydney-assessment-framework/)
- Bridgeman, A., Liu, D. and Kalman, E. / University of Sydney (29 April 2026). Guide for markers of open assessments. Official guidance on judgement and assurance boundaries. [Guide](https://educational-innovation.sydney.edu.au/teaching@sydney/guide-for-markers-of-open-assessments/)
- Ofqual (1 April 2026). What next for our framework for apprenticeship assessment. Official explanation; applicability depends on assessment-plan transition. [Article](https://ofqual.blog.gov.uk/2026/04/01/what-next-for-our-framework-for-apprenticeship-assessment/)
- ICO (current, undated). Data minimisation, Artificial Intelligence audit toolkit. Guidance marked under review following the Data (Use and Access) Act. [Guidance](https://ico.org.uk/for-organisations/advice-and-services/audits/data-protection-audit-framework/toolkits/artificial-intelligence/data-minimisation/)
- OpenAI (29 July 2025). ChatGPT study mode. First-party capability announcement, not independent evaluation. [Announcement](https://openai.com/index/chatgpt-study-mode/)
- Anthropic (2 April 2025). Introducing Claude for Education. First-party description of Learning mode and templates. [Announcement](https://www.anthropic.com/news/introducing-claude-for-education)
- Microsoft Education (13 May 2026). Study and Learn: AI built for your student. First-party description and availability statement. [Announcement](https://www.microsoft.com/en-us/education/blog/2026/05/study-and-learn-ai-built-for-your-student/)
- Reflex (current documentation, undated). Local Packages / Local Components. Capability evidence; not a benchmark of the pinned prototype version. [Documentation](https://reflex.dev/docs/wrapping-react/local-packages/)
- Next.js (25 August 2026). Server and Client Components. Current framework documentation; no comparative performance finding. [Documentation](https://nextjs.org/docs/app/getting-started/server-and-client-components)
- 1EdTech (current documentation, undated). Learning Tools Interoperability. LTI 1.3 and associated service overview. [Standard overview](https://www.1edtech.org/standards/lti)

All web sources were accessed on 6 September 2026. Product capabilities and institutional guidance may change; deployment decisions should use the versions then in force.
