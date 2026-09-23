# Writing Lab proposal: addendum

Companion to WritingLab_Proposal.md. Prepared 8 September 2026.

These are additive sections. The existing proposal is not superseded. Each section below names where it should be inserted.

The gaps addressed here are delivery risks rather than design flaws. The proposal reasons carefully about what Writing Lab should be and what evidence would justify it. What it does not yet do is protect the project from the four ways initiatives of this shape usually fail: no named decision-maker, an unsequenced governance dependency, an underweighted content-authoring load, and an unclear relationship to the rest of the estate.

---

## A. Governance and data protection as a delivery gate

**Insert after "Delivery sequence and validation", before "Evaluation that can answer the investment question".**

The proposal correctly states that BPP's data-protection team should determine lawful processing, retention, supplier arrangements and any required impact assessment. It does not place that determination in the delivery sequence, which means the current plan permits building the full learning slice and then discovering it cannot be piloted with real learners.

This is the single most likely way the project stalls, and it is entirely avoidable.

| Gate | Must be resolved before | Owner |
|---|---|---|
| Lawful basis for processing learner writing, and whether a DPIA is required | Any pilot involving real learner submissions | BPP data protection |
| Supplier arrangements for the AI provider, including whether learner text may leave the BPP estate | Any AI call on real learner text | BPP data protection and procurement |
| Retention and deletion policy for artefacts, snapshots, interview turns and evidence events | Schema is finalised in Stage 1 | Product owner, with data protection sign-off |
| Hosting location and whether non-BPP infrastructure is permitted for a pilot | Any deployment reachable by learners | BPP IT |
| Accessibility conformance position, including what may and may not be claimed | Any communication describing the product to learners | Product owner and accessibility specialist |

Two of these bind earlier than they appear. The retention policy shapes the EvidenceEvent and InterviewTurn schemas, so it is a Stage 1 dependency rather than a pre-pilot one. And the hosting question binds before any deployment, including an internal demonstration on free-tier infrastructure.

**Recommended action:** open the data protection conversation at the start of Stage 0, in parallel with the repository audit, not after the learning slice exists. The conversation is slow and the engineering is not blocked by it, so starting it early costs nothing and starting it late costs a delivery cycle.

---

## B. Content authoring: the load the plan underweights

**Insert as a subsection within "Delivery sequence and validation".**

The proposal names content authoring as a role requiring an owner. It does not estimate the load, and that load is the most commonly underestimated cost in projects of this shape.

Stage 2 requires three skill families, each with a supported activity and a genuinely different transfer activity, each with an authored source pack, permitted claims, acceptable answer range, common misconceptions, a rubric and a scaffold ladder, all educator-reviewed. Working from the activity contract in the proposal, that is at minimum six complete activity definitions with reviewed source material before a single learner sees anything useful.

The failure mode is not that this is impossible. It is that engineering delivers a working activity engine into which nobody has had time to author activities, and the pilot slips while the platform sits idle. This has a specific tell: a demo that works beautifully on the one authored example.

Three consequences for the plan:

- **Authoring starts in Stage 0**, not Stage 2. The activity contract is already specified well enough to author against, and authored content is the only part of this project that survives a decision not to build the app.
- **Name the author, not the role.** If the answer is "Mo, in evenings", the plan should say that, because it changes the realistic timeline and it is a single point of failure worth surfacing.
- **Separate authoring from review.** The proposal requires educator-reviewed content. Whoever authors cannot also be the reviewer, and reviewer time needs to be requested before it is needed.

**Recommended addition to the delivery table:** a Stage 0 deliverable of one complete, reviewed activity definition, used to establish how long authoring actually takes before committing to a Stage 2 date.

---

## C. Position in the AI-enabled education estate

**Insert after "Value proposition and position in an AI-enabled education experience".**

The proposal positions Writing Lab against generic AI assistants. It does not position it against, or with, BPP's two other in-house tools. For an internal audience this is a material omission, because the obvious challenge to the proposal is "why is this separate from FeedbackHub?"

Writing Lab occupies a distinct position in the Practise, Prove, Progress model, and it is the only one of the three tools that does.

| Tool | Stage | What it produces |
|---|---|---|
| ConCraftr | Enabler layer feeding Practise | Learning artefacts, assessment tasks and source material at programme scale |
| FeedbackHub | Practise, reaching into Prove | Episodic feedback on a submitted artefact, and Lane 2 critical-evaluation evidence |
| Writing Lab | Practise, and the only tool structurally shaped for Progress | A longitudinal capability record: repeated observations of the same skill under stated conditions, over time |

The distinction that matters: FeedbackHub evaluates a submission. Writing Lab models a learner. A Skills Passport is a longitudinal claim, so Writing Lab's evidence states are the only outputs in the estate already shaped like passport entries.

Three connections should be stated as intent, not built in the first release:

- **ConCraftr as content supply.** The activity contract in this proposal and ConCraftr's SOW schema describe the same object at different levels of detail. ConCraftr already has Skills England KSB retrieval. Authored activities should carry the same capability tags so that a Writing Lab evidence record can resolve to a programme outcome.
- **FeedbackHub evidence landing in the Writing Lab ledger.** The Critical Evaluator persona produces structured Lane 2 scores. Those belong in a capability record, not in FeedbackHub's session history.
- **One evidence schema, three producers.** The CapabilityEvidence model specified in the architecture prompt should be designed as a shared contract from the start, even while only Writing Lab writes to it. Retrofitting a shared schema across three applications is substantially harder than designing one that anticipates them.

This does not require building the shared store now. It requires not designing something that makes it impossible later.

---

## D. Risk register

**Insert before "Investment and stop criteria".**

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Data protection determination arrives after the build, blocking the pilot | High | High | Open the conversation in Stage 0; design retention into the schema | Product owner |
| Authored content is not ready when the engine is | High | High | Author one complete activity in Stage 0 to calibrate; separate author from reviewer | Curriculum owner |
| Frontend decision is made on preference and cannot be defended | Medium | Medium | Run the Stage 4 comparison as specified; record evidence before deciding | Engineering owner |
| Single-person dependency across product, curriculum and engineering | High | High | Name each responsibility explicitly, including where they are the same person | Sponsor |
| AI feedback is confidently wrong in a way educators notice first | Medium | High | Educator-rated benchmark before pilot; visible challenge route; version rubric and model | Curriculum owner |
| Accessibility conformance claimed before it is audited | Medium | High | No conformance claim until an audit exists; state WCAG 2.2 AA as a target, not an achievement | Accessibility specialist |
| Evidence records are interpreted as assurance of authorship | Medium | High | Evidence states carry explicit conditions; never display an authorship percentage | Product owner |
| Pilot shows learners mainly seek model answers | Medium | Medium | Already a stated stop criterion; instrument it from the first release | Evaluation owner |
| Scope expands to literary writing or social features before validation | Medium | Medium | Already excluded in the proposal; hold the line at each stage gate | Sponsor |

The two High/High risks at the top are the ones to act on this month. Both are cheap to start and expensive to start late.

---

## E. Decision requested

**Insert immediately after "Decision in brief".**

The proposal describes what should be built and how it should be validated. It does not state what is being asked of the reader, which makes it a strategy document rather than a decision paper.

State explicitly:

- **What is being asked for**: named time from a curriculum author and reviewer, engineering capacity, an accessibility specialist for testing, and a decision on hosting.
- **What is not being asked for**: a commitment to the full delivery sequence, a budget for institutional integration, or a decision on Reflex versus Next.js.
- **Who decides what**: sponsor decides investment and scope; product owner decides sequence; engineering owner decides architecture within the recorded decision gates; data protection decides what may be processed.
- **What happens if the answer is no**: the authored content and the evaluation design remain useful. This is stated in the proposal's stop criteria and should be visible at the front, because a proposal that survives its own rejection is easier to approve.

---

## F. Cost model structure

**Insert within "Investment and stop criteria".**

The proposal correctly identifies the categories to track and correctly refuses to invent figures. A reader approving investment still needs a shape to reason about, so give the model without the numbers and fill them in as they become known.

| Category | Unit | Recurring or one-off | Known? |
|---|---|---|---|
| Curriculum authoring | Days per activity definition | One-off per activity, plus revision | Establish in Stage 0 |
| Educator review | Days per activity definition | One-off per activity | Establish in Stage 0 |
| Engineering build | Days per stage | One-off per stage | Estimate after the repository audit |
| Engineering maintenance | Days per month | Recurring | Unknown until architecture is settled |
| Model calls | Cost per completed activity | Recurring, scales with learners | Measurable from the first slice |
| Storage and hosting | Cost per month | Recurring | Depends on hosting decision |
| Accessibility testing | Days per release | Recurring | Quote required |
| Tutor review time | Minutes per learner per cycle | Recurring, scales with learners | Measure in pilot |

Two of these are measurable cheaply and early: cost per completed activity in model calls, and days per authored activity. Both should be reported at the Stage 2 gate, because together they determine whether the efficiency measure the proposal specifies, cost per additional learner reaching a capability standard, is computable at all.
