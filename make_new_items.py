import json

# Data extraction
# Let's craft the principles and exercises manually in code.

new_principles = [
    {
        "rule_id": "ACA-FUNC-COMP-001",
        "title": "Comparing and contrasting",
        "track": "academic",
        "skills": ["transitions", "cohesion", "comparison", "contrast"],
        "principle": "Use comparing and contrasting phrases to highlight similarities and differences between subjects. This analysis can precede evaluation.",
        "weak_examples": ["X is different to Y. They are similar in some ways."],
        "strong_examples": [
            "X is different from Y in a number of respects.",
            "There are a number of important differences between X and Y.",
            "X differs from Y in a number of important ways.",
            "Women and men differ not only in physical attributes but also in the way in which they...",
            "The mode of processing used by the right brain is comparable in complexity to that used by the left..."
        ],
        "exceptions": ["Do not force a contrast where none exists."],
        "source": {"document": "Comparing and contrasting.docx", "section": "Comparing and Contrasting"}
    },
    {
        "rule_id": "ACA-FUNC-CRIT-001",
        "title": "Being critical",
        "track": "academic",
        "skills": ["transitions", "cohesion", "criticality"],
        "principle": "Being critical means questioning sources, identifying problems with arguments or methods, and not accepting claims merely because they are published.",
        "weak_examples": ["The author says this is true, so it must be."],
        "strong_examples": [
            "One major drawback of this approach is...",
            "However, this argument fails to take into account...",
            "The authors' claim that X causes Y is not supported by their data."
        ],
        "exceptions": ["Do not be critical merely for the sake of it; criticism should be constructive."],
        "source": {"document": "Being critical.docx", "section": "Being Critical"}
    },
    {
        "rule_id": "ACA-FUNC-CAUSE-001",
        "title": "Describing cause and effect",
        "track": "academic",
        "skills": ["transitions", "cohesion", "causation"],
        "principle": "Academic work often involves analyzing problems by thoroughly understanding their causes and effects.",
        "weak_examples": ["X happened and then Y happened."],
        "strong_examples": [
            "X causes Y.",
            "Y is a consequence of X.",
            "The increase in X can be attributed to Y.",
            "This resulted in a significant change in Z."
        ],
        "exceptions": ["Avoid assuming correlation implies causation."],
        "source": {"document": "Describing causes and effects.docx", "section": "Describing Causes and Effects"}
    },
    {
        "rule_id": "ACA-FUNC-EXAM-001",
        "title": "Giving examples",
        "track": "academic",
        "skills": ["transitions", "cohesion", "exemplification"],
        "principle": "Specific examples serve as evidence to support general claims and help clarify complex or unfamiliar concepts.",
        "weak_examples": ["There are many issues, like this one."],
        "strong_examples": [
            "For example, the recent study by Smith (2020) illustrates...",
            "This concept is exemplified in the work of Jones...",
            "A notable example of this phenomenon is..."
        ],
        "exceptions": ["Examples must be relevant and representative of the general claim."],
        "source": {"document": "Giving examples.docx", "section": "Giving Examples"}
    },
    {
        "rule_id": "ACA-FUNC-DEF-001",
        "title": "Defining terms",
        "track": "academic",
        "skills": ["transitions", "cohesion", "defining"],
        "principle": "Define key terms clearly to prevent misinterpretation and demonstrate understanding of complex concepts.",
        "weak_examples": ["A catalyst is something that helps a reaction."],
        "strong_examples": [
            "In this study, X is defined as...",
            "The term Y refers to...",
            "X can be loosely described as..."
        ],
        "exceptions": ["Avoid overly complex definitions that obscure rather than clarify."],
        "source": {"document": "Defining terms.docx", "section": "Writing Definitions"}
    },
    {
        "rule_id": "ACA-FUNC-TREND-001",
        "title": "Describing trends",
        "track": "academic",
        "skills": ["transitions", "cohesion", "describing-trends"],
        "principle": "Use precise language to describe changes over time (trends) and predict future changes (projections).",
        "weak_examples": ["The numbers went up and down."],
        "strong_examples": [
            "The number of live births outside marriage reached a peak during the second world war.",
            "The peak age for committing a crime is 18.",
            "There was a sharp decline in the rate of inflation."
        ],
        "exceptions": ["Ensure descriptions match the data precisely without exaggeration."],
        "source": {"document": "Describing trends.docx", "section": "Describing Trends and Projections"}
    },
    {
        "rule_id": "ACA-FUNC-REP-001",
        "title": "Reporting results",
        "track": "academic",
        "skills": ["transitions", "cohesion", "reporting-results"],
        "principle": "Present results clearly, often by identifying the relevant figure/table and highlighting the most significant data without elaborate discussion in the results section.",
        "weak_examples": ["The table shows our results."],
        "strong_examples": [
            "Table 1 shows the results obtained from...",
            "As can be seen from Figure 2, there is a clear trend...",
            "The data demonstrate that..."
        ],
        "exceptions": ["Do not interpret the results extensively in the reporting section; save that for the discussion."],
        "source": {"document": "Reporting results.docx", "section": "Reporting Results"}
    },
    {
        "rule_id": "ACA-FUNC-LIT-001",
        "title": "Referring to the literature",
        "track": "academic",
        "skills": ["transitions", "cohesion", "literature-review"],
        "principle": "Acknowledge sources clearly within or alongside the text, using appropriate reporting verbs to integrate the literature into your argument.",
        "weak_examples": ["A book said this idea."],
        "strong_examples": [
            "Smith (2003) argues that...",
            "Previous studies have shown that...",
            "According to Jones (2010),..."
        ],
        "exceptions": ["Ensure citations accurately reflect the original author's intent."],
        "source": {"document": "Referring to Literature.docx", "section": "Referring to Literature"}
    },
    {
        "rule_id": "ACA-FUNC-HEDGE-001",
        "title": "Hedging a claim",
        "track": "academic",
        "skills": ["transitions", "cohesion", "hedging", "discussing-findings"],
        "principle": "Use hedging language when discussing findings to acknowledge limitations, indicate probability rather than certainty, and leave room for alternative explanations.",
        "weak_examples": ["This proves that our theory is completely correct."],
        "strong_examples": [
            "These findings suggest that...",
            "It appears that X may influence Y...",
            "This could indicate a potential relationship between..."
        ],
        "exceptions": ["Do not hedge when stating established facts or definitive results."],
        "source": {"document": "Discussing findings.docx", "section": "Discussions"}
    },
    {
        "rule_id": "ACA-TRANS-ADD-001",
        "title": "Signalling addition",
        "track": "academic",
        "skills": ["transitions", "cohesion", "addition"],
        "principle": "Use addition transitions to add information, reinforce ideas, and express agreement with preceding material.",
        "weak_examples": ["The study was good. And it was cheap."],
        "strong_examples": [
            "In addition, the results show...",
            "Furthermore, this approach provides...",
            "Moreover, the data indicates...",
            "Similarly, the second group..."
        ],
        "exceptions": ["Avoid starting too many sentences with 'And' or 'Also' in formal prose."],
        "source": {"document": "Linking words1.docx", "section": "Agreement / Addition / Similarity"}
    },
    {
        "rule_id": "ACA-TRANS-CONT-001",
        "title": "Signalling contrast",
        "track": "academic",
        "skills": ["transitions", "cohesion", "contrast"],
        "principle": "Use contrast transitions to introduce opposing ideas, point out alternatives, or establish differences.",
        "weak_examples": ["The hypothesis was plausible. But it failed."],
        "strong_examples": [
            "However, the evidence suggests otherwise.",
            "In contrast, the second model demonstrated...",
            "Conversely, the control group exhibited...",
            "On the other hand, earlier studies found..."
        ],
        "exceptions": ["Ensure the contrast is logical and clear to the reader."],
        "source": {"document": "Linking words1.docx", "section": "Opposition / Limitation / Contradiction"}
    },
    {
        "rule_id": "ACA-TRANS-CAUSE-001",
        "title": "Signalling cause and result",
        "track": "academic",
        "skills": ["transitions", "cohesion", "cause-and-result"],
        "principle": "Use cause and result transitions to link conditions to their consequences and show logical progression.",
        "weak_examples": ["It rained. So we stopped."],
        "strong_examples": [
            "Consequently, the project was delayed.",
            "As a result, the temperature increased.",
            "Therefore, we conclude that...",
            "Thus, the hypothesis is supported."
        ],
        "exceptions": ["Avoid overusing 'so' in formal academic writing."],
        "source": {"document": "Linking words1.docx", "section": "Cause / Condition / Purpose"}
    },
    {
        "rule_id": "ACA-TRANS-CONC-001",
        "title": "Signalling concession",
        "track": "academic",
        "skills": ["transitions", "cohesion", "concession"],
        "principle": "Use concession transitions to acknowledge a point that might oppose your argument before asserting your own point.",
        "weak_examples": ["Even though it was hard we did it."],
        "strong_examples": [
            "Although the sample size was small, the results were statistically significant.",
            "Despite these limitations, the findings suggest...",
            "Nevertheless, the overall trend remains clear."
        ],
        "exceptions": ["Ensure the concession does not completely undermine your main argument."],
        "source": {"document": "Linking words1.docx", "section": "Opposition / Limitation / Contradiction"}
    },
    {
        "rule_id": "ACA-TRANS-SEQ-001",
        "title": "Signalling sequence and time",
        "track": "academic",
        "skills": ["transitions", "cohesion", "sequence-and-time"],
        "principle": "Use sequence and time transitions to organize points chronologically or establish an order of events.",
        "weak_examples": ["First we did X. Next we did Y. Then Z happened."],
        "strong_examples": [
            "Initially, the sample was prepared.",
            "Subsequently, the solution was heated.",
            "Finally, the results were recorded.",
            "In the meantime, the control group..."
        ],
        "exceptions": ["Do not overuse simple sequencers (first, second, third) if logical connections are more appropriate."],
        "source": {"document": "Linking words1.docx", "section": "Time / Chronology / Sequence"}
    },
    {
        "rule_id": "ACA-TRANS-SUMM-001",
        "title": "Signalling summary and conclusion",
        "track": "academic",
        "skills": ["transitions", "cohesion", "summary-and-conclusion"],
        "principle": "Use summary transitions to draw points together, restate key ideas briefly, and signal the end of an argument.",
        "weak_examples": ["To finish up, the paper is about X."],
        "strong_examples": [
            "In summary, the evidence points to...",
            "To conclude, this study demonstrates...",
            "Overall, the findings indicate...",
            "In brief, the proposed model..."
        ],
        "exceptions": ["Avoid cliché conclusions like 'In conclusion' if the ending is already obvious from the structure."],
        "source": {"document": "Linking words1.docx", "section": "Conclusion / Summary / Restatement"}
    }
]

new_exercises = [
    {
        "exercise_id": "aca-trans-diag-1",
        "kind": "diagnostic_selection",
        "mode": "academic",
        "skill": "contrast",
        "prompt": "Choose the connective that correctly signals the logical relationship between the sentences.",
        "options": [
            "Furthermore,",
            "However,",
            "Therefore,",
            "Similarly,"
        ],
        "answer_index": 1,
        "seed_text": "The initial hypothesis was highly plausible. ______, the experimental evidence suggests otherwise.",
        "target": "A contrast connective indicating contradiction.",
        "hints": [
            "The second sentence contradicts the expectation set by the first.",
            "You need a word that signals opposition or limitation."
        ],
        "rule_ids": ["ACA-TRANS-CONT-001"],
        "max_xp": 50,
        "difficulty": 1
    },
    {
        "exercise_id": "aca-trans-diag-2",
        "kind": "transitions",
        "mode": "academic",
        "skill": "cause-and-result",
        "prompt": "Choose the connective that correctly signals the logical relationship between the sentences.",
        "options": [
            "Consequently,",
            "Nevertheless,",
            "In addition,",
            "For example,"
        ],
        "answer_index": 0,
        "seed_text": "The temperature of the solution was unexpectedly increased. ______, the reaction proceeded at an accelerated rate.",
        "target": "A cause-and-result connective.",
        "hints": [
            "The increased temperature caused the accelerated reaction.",
            "Look for a word that means 'as a result'."
        ],
        "rule_ids": ["ACA-TRANS-CAUSE-001"],
        "max_xp": 50,
        "difficulty": 2
    },
    {
        "exercise_id": "aca-trans-comp-1",
        "kind": "sentence_completion",
        "mode": "academic",
        "skill": "literature-review",
        "prompt": "Complete the stem using a phrase that refers to the literature appropriately.",
        "seed_text": "According to Smith (2003), ______",
        "target": "A clause summarising a finding from the literature.",
        "hints": [
            "Follow the introductory phrase with a statement of fact or argument.",
            "Example: 'According to Smith (2003), distinct differences exist between the two groups.'"
        ],
        "rule_ids": ["ACA-FUNC-LIT-001"],
        "max_xp": 80,
        "difficulty": 1
    },
    {
        "exercise_id": "aca-trans-comp-2",
        "kind": "sentence_completion",
        "mode": "academic",
        "skill": "hedging",
        "prompt": "Complete the stem using hedging language to discuss the finding.",
        "seed_text": "These findings suggest that ______",
        "target": "A cautious conclusion based on the findings.",
        "hints": [
            "Avoid words like 'proves' or 'definitely'.",
            "Example: 'These findings suggest that X may influence Y under certain conditions.'"
        ],
        "rule_ids": ["ACA-FUNC-HEDGE-001"],
        "max_xp": 80,
        "difficulty": 2
    },
    {
        "exercise_id": "aca-trans-const-1",
        "kind": "constrained_composition",
        "mode": "academic",
        "skill": "exemplification",
        "prompt": "Write one or two sentences performing the function of giving an example. Use the phrase 'For example, the recent study by'.",
        "seed_text": "",
        "target": "A sentence correctly using the specified phrase to give an example.",
        "hints": [
            "Start by making a general claim.",
            "Then use the phrase to introduce a specific study that supports the claim."
        ],
        "rule_ids": ["ACA-FUNC-EXAM-001"],
        "max_xp": 100,
        "difficulty": 3
    },
    {
        "exercise_id": "aca-trans-const-2",
        "kind": "constrained_composition",
        "mode": "academic",
        "skill": "concession",
        "prompt": "Write one or two sentences using a concession transition. Use the word 'Although' at the beginning of the first sentence.",
        "seed_text": "",
        "target": "A sentence that acknowledges a limitation before asserting a main point.",
        "hints": [
            "Start with 'Although' followed by a limitation or opposing point.",
            "Follow the comma with your main, stronger point."
        ],
        "rule_ids": ["ACA-TRANS-CONC-001"],
        "max_xp": 100,
        "difficulty": 3
    }
]

# Write to file
with open('new_items.json', 'w') as f:
    json.dump({'principles': new_principles, 'exercises': new_exercises}, f, indent=2)

print("Created new items.")
