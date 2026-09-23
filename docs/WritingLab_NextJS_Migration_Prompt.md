# WritingLab: Next.js frontend prompt (Stage 4)

Companion to WritingLab_Cursor_Architecture_Prompt.md. Prepared 8 September 2026.

## Why this is structured as a comparison

The proposal sets a decision gate: build a bounded Next.js candidate, run an identical slice in both frameworks, and favour Next.js only when the comparison supports the change.

This prompt builds the Next.js frontend now, in a form that satisfies that gate. If the comparison goes the way we expect, this codebase becomes the production frontend and nothing is thrown away. If it does not, we have an answer worth having and a working Reflex app still standing.

The practical difference between this and a straight rewrite is small: build the same thing, keep the Reflex app alive alongside it, and record the comparison as you go. The difference in what you can defend afterwards is large.

**Do not delete or disable the Reflex application at any point in this task.**

---

## Prompt

```
You are building a Next.js/TypeScript frontend candidate for WritingLab in this
repository, as Stage 4 of the plan in docs/WritingLab_Cursor_Architecture_Prompt.md.

Read that document and docs/WritingLab_Proposal.md completely before starting. Its
section 3, Execution contract, governs this task in full: plan before code, never
commit, isolated branch, additive and fail-closed, British English, pinned
dependencies, no secrets in the repo, no deployment.

## What you are building

A Next.js App Router frontend that consumes the existing Python API and reproduces one
bounded slice of the learner experience. Not the whole product. The slice is defined in
"The comparison slice" below.

The Python learning engine, domain logic, activity content and evidence schemas stay
where they are. You are replacing the interface layer only.

## Hard boundary: no business logic in TypeScript

This is the requirement most likely to be violated and the most expensive to unwind.

Learning rules, reward eligibility, assistance permissions, evidence conditions,
completion logic and assessment policy live in Python, server-side, and are reached
over the API. The frontend renders state and sends intents. It does not decide them.

Specifically:
- The frontend never decides whether an attempt counts as complete.
- The frontend never decides whether a reward is due.
- The frontend never decides what assistance is permitted. It renders the
  permitted_actions the server returned.
- Client-side controls are a convenience, never an enforcement point. Assume the client
  is hostile.

If you find yourself writing a rule in TypeScript that also exists in Python, stop and
report it. Duplicated business rules across two languages is the failure mode that makes
this migration a permanent tax rather than a one-off cost.

## Phase A: contract first

Before building any UI:

1. Read the existing Python API surface and document every endpoint the slice needs:
   method, path, request shape, response shape, error shapes, auth.
2. Where the API does not yet expose something the slice needs, list it. Do not invent
   endpoints and do not add them to the Python side without approval.
3. Generate shared types from the Python schemas rather than hand-writing TypeScript
   interfaces. Report the mechanism you propose (OpenAPI generation, or equivalent) and
   why. Hand-written types drift silently and will be wrong within a month.
4. Confirm how authentication works today and how the Next.js frontend will participate
   in it without holding credentials client-side.

STOP. Report the contract and wait for approval.

## Phase B: the comparison slice

Build exactly this journey, no more:

1. Open an authored claim-calibration activity.
2. Read the source material and write a paragraph in the editor.
3. Request feedback on a specified revision.
4. See one anchored question against the text.
5. Revise, with the original and the feedback both still visible.
6. View a before/after comparison.
7. Disconnect the network, keep typing, reconnect.
8. Submit the exact latest revision.

Plus, from the interview pattern:
9. Answer one interview question.
10. Edit an earlier answer and observe dependent confirmations invalidate.

Suggested structure, adapted to repository conventions:
- apps/web for the Next.js candidate
- the existing Python package for API and domain logic
- schemas for generated shared contracts
- content for versioned activities
- tests for domain, API and user journeys

Editor requirements:
- Keystrokes and selection stay local. No round trip to type.
- Versioned snapshots synchronised through a recoverable queue.
- Saved, pending and conflicted states shown in plain language.
- On conflict, preserve both versions and offer resolution. Never silently discard.
- Feedback anchors go stale visibly when their referenced text changes. Never
  silently reattach old feedback to different text.
- Preserve cursor position through updates. Support composition input methods
  (this matters for multilingual learners and is easy to break).

Accessibility is a build requirement, not a later pass:
- Full keyboard operation, visible and unobscured focus.
- Meaningful headings and labels; screen-reader announcement on completed responses,
  not on every token.
- Zoom and reflow; text alternatives to colour; keyboard alternatives to any drag.
- No motion or timer as a completion requirement.
- A linear accessible view exposing the same questions, outline and provenance as the
  wide layout.

STOP. Report before moving to comparison.

## Phase C: run the comparison

Perform the same ten steps above against the existing Reflex application and record
results side by side in docs/frontend-comparison.md.

Record for each framework:
- Did each step complete without lost text or duplicated submission?
- Were feedback anchors correct, or explicitly stale?
- Was the evidence record intelligible afterwards?
- Keyboard-only completion: yes or no, with any blocking issue named.
- Screen-reader behaviour where tools permit, stated as developer verification, not
  as user testing.
- Multilingual composition input: does it survive a re-render?
- Behaviour on disconnect and reconnect.
- Implementation effort in each, honestly, including wrapper complexity in Reflex and
  API surface added for Next.js.
- Ongoing maintenance burden as you observed it, not as you expect it.

Test on a representative lower-end device if one is available. If not, say so rather
than estimating.

Acceptance for either framework: no lost text, no duplicated submissions, correct or
explicitly stale anchors, an intelligible evidence record, and keyboard completion of
the whole slice.

## Phase D: recommend

Write the recommendation into docs/architecture-decision.md as a decision record:
context, options, evidence observed, decision, consequences, and what would reverse it.

Recommend Next.js only if the comparison supports it. If Reflex passes at comparable
effort, say so plainly. A recommendation that simply confirms the preference we started
with, without evidence in the comparison table to support it, is worse than no
recommendation, because it will not survive being questioned.

If the recommendation is Next.js, include:
- What remains to be ported beyond the slice, as a bounded list.
- The migration and rollback path.
- What must stay in Python permanently.

## Constraints

- Do not delete, disable or break the Reflex application. It must remain runnable
  throughout and at the end.
- Do not port the whole product in this task. The slice is the deliverable.
- Do not add Python endpoints without approval.
- Do not write business rules in TypeScript.
- Do not hand-write types that could be generated.
- Do not introduce a state management library, component library or editor dependency
  without naming it in a plan and justifying it. Every dependency here is a long-term
  commitment.
- Do not deploy anything.
- No commits. Isolated branch. Stage nothing.

## On the editor library

A ProseMirror or Tiptap-based implementation is a candidate for investigation, not a
decision already made. Before adopting any rich-text editor, check it against the
accessibility requirements above, specifically keyboard operation, screen-reader
behaviour and composition input. Report what you find. Neither a code editor nor a
rich-text editor should be selected without task-level access testing.

If you can build the slice with a plain contenteditable or textarea and defer the
editor decision, do that and say so. It is much easier to add a rich editor later than
to remove one.

## Reporting

At each STOP, report: what you built, file by file; commands run with real output;
tests written and their results; what you did not implement and why; untested risks;
and rollback instructions.

Do not claim the slice demonstrates educational effectiveness, accessibility
conformance or production readiness. It demonstrates that the framework can carry the
interaction, which is the only question Stage 4 asks.
```

---

## Notes for Mo

**Phase A is the one to be strict about.** Generated types from the Python schemas rather than hand-written interfaces is the difference between one migration and a permanent synchronisation problem. If Cursor proposes hand-writing them because it is faster, that is the moment to push back.

**The "no business logic in TypeScript" rule will be tested repeatedly.** It is faster in the moment to compute completion client-side, and every time that happens the evidence integrity argument weakens, because a rule the client can compute is a rule the client can be made to lie about.

**Expect Phase C to be uncomfortable.** If Reflex passes the comparison, the honest outcome is to keep it, and the prompt is deliberately written to make that outcome sayable. The value of the gate is entirely in whether you would accept the answer you did not want.
