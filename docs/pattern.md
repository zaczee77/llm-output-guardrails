# The LLM output guardrail pattern

## Where the pattern comes from

Paxei is a healthcare AI prior authorization assistant built by Nirmeet Rao and presented on his portfolio at nirmeetrao.com. Its own description says it is an LLM agent with guardrails and human in the loop review of every output. PharmFlows, his workflow product at Concordia Pharma, uses the same shape: workflow output is checked before it moves on. This pattern writes down the guardrail step those products share, so it can be reused wherever a model output meets a decision that matters.

The review queue from the companion pattern is the human gate that follows. The guardrail is the automated gate that comes first. The guardrail catches what a deterministic check can catch, and the reviewer catches what only a person can judge. Neither replaces the other.

## The pipeline

Every model output enters the guardrail. The guardrail is the only way out. An output that never enters the guardrail cannot be used, and an output that leaves it carries exactly one outcome: pass, pass with redaction, escalate, or block. That single rule is what turns a set of checks into a gate.

Each output carries its fields, the checks run on it, and, once decided, its outcome and the reason in plain words. A redaction is recorded with the field it touched, so the record shows what was removed and where. A blocked output is kept out of the pipeline entirely. It is never passed along with a warning attached.

## The five checks

Every output is checked the same way, in the same order.

1. Required fields present. Does the output carry every field the next step needs. The demo requires a summary, an amount, and a confidence value. An output missing one of these cannot be used, because the next step would be guessing at a missing value.
2. Blocked wording absent. Does the text carry wording that should never go out as written, such as a promise of approval or a definitive coverage claim. Blocked wording is a stop sign, not a style note. The demo blocks the phrases guaranteed approval and definitely covered.
3. Personal identifiers absent. Does the text carry a phone number, an email address, or an identifier shaped like a social security number. If it does, the identifier is replaced with a marker before the output can continue. The demo redacts phone numbers, email addresses, and social security number shapes.
4. Confidence high enough. Is the model confidence at or above the threshold. The demo uses 0.6. Below that, the output is not wrong, it is uncertain, and uncertainty goes to a person.
5. Numbers inside a plausible range. Is the amount inside the range the business expects. The demo uses 0 to 100000. Outside that, the number is either a model error or a case a person needs to look at. Either way, it does not pass on its own.

The checks are deliberately small. A guardrail with five checks gets run every time. A guardrail with fifty checks gets skipped when the day is busy.

## The four outcomes

The checks combine into one outcome, and only one.

1. Pass. Every check is satisfied. The output is ready to use.
2. Pass with redaction. The only problem was a personal identifier, and it has been removed. The output is ready to use, and the record says what was redacted.
3. Escalate. The output is uncertain or out of range, but it is not unsafe as written. A person looks at it next.
4. Block. A required field is missing, or the text carries blocked wording. The output is not used. A block names the reason, so the next attempt knows what to fix.

The order matters. A missing field blocks before anything else is checked, because there is nothing to check against. Blocked wording blocks before redaction, because a promise of approval should not be cleaned up and sent. It should be stopped.

## Design principles

1. The guardrail is the only way out. An output that skips the guardrail is an output nobody checked, whatever its quality.
2. The same checks every time, in the same order. Guardrail quality comes from consistency, not from a clever check on a good day.
3. A redaction is recorded, not hidden. The record says what was removed and from which field, so a later reader knows the output was changed and why.
4. A block is a normal outcome. A guardrail that never blocks is not guarding. It is passing everything through.
5. Escalation is not failure. Low confidence and out of range numbers are the guardrail doing its job: sending the uncertain cases to the people who can judge them.
6. The model never clears its own output. The guardrail is deterministic code, not the model checking itself, and the reviewer is a person, not the model again.

## What the demo shows, and what it does not show

The demo in this repository shows the pattern at miniature scale: six invented outputs, five checks, four outcomes, and one redaction. It shows the shape of the work: a gate, a consistent check, one outcome per output, and a record of what changed. It does not show real outputs, real records, real reviewers, or measured results, and it does not show the Paxei product or the PharmFlows product. Real check logic, real identifier rules, and real escalation routes are all real parts of a guardrail, and none of them are modeled in the demo. The demo is a reference implementation of the pattern, written in plain Python with no external packages.

## Links

1. Portfolio: https://nirmeetrao.com
2. GitHub: https://github.com/Zaczee77
3. LinkedIn: https://www.linkedin.com/in/nirmeet-rao
