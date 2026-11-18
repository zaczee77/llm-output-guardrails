# LLM output guardrails

A reference pattern and a small runnable demo for the guardrail step that sits between a language model output and anything a person or a system acts on. The pattern comes from work Nirmeet Rao has shipped in healthcare AI: Paxei, a prior authorization assistant built as an LLM agent with guardrails and human in the loop review of every output, and PharmFlows, where workflow output is checked before it moves forward.

## The problem

A language model can produce text that looks finished while carrying a flaw that makes it unsafe to use. A summary can promise an outcome nobody approved. A draft can repeat a phone number or an identifier that should never leave the system. A structured answer can arrive missing the one field the next step needs. A confident sounding number can sit far outside any plausible range. Each of these is easy to miss when the text reads smoothly, and that is exactly why the check has to run before the output is used, not after someone notices the damage.

A guardrail is not a second model. It is a small set of deterministic checks that run on every output, in the same order, with the same rules. Deterministic matters here. A check that sometimes runs is a suggestion. A check that always runs is a gate.

## What the pattern does

1. Every model output passes through the guardrail before it reaches a person, a file, or another system.
2. Every output is checked the same way. The demo checks five things: are the required fields present, is the confidence high enough to act on, does the text carry blocked wording, does the text carry personal identifiers, and are the numbers inside a plausible range.
3. A failed check decides the outcome, not a judgement call. Missing fields and blocked wording stop the output. Low confidence and out of range numbers send it to a person. Personal identifiers are removed before the output can continue.
4. Nothing leaves the pipeline without exactly one outcome. Pass, pass with redaction, escalate, or block. There is no fifth path and no silent exit.
5. A blocked output is a normal outcome, not an error. A pipeline that never blocks is not guarding. It is passing everything through.

## The demo in this repository

The demo folder contains a small reference demo in plain Python with no external packages. It runs six invented model outputs through the guardrail: one clean output passes, one output with a phone number passes after the number is redacted, one output carrying a promise of approval is blocked, one low confidence output is escalated, one output missing its amount field is blocked, and one output with an amount far outside the plausible range is escalated.

The docs folder describes the pattern in full: the five checks, the four outcomes, and the rule that a redaction is recorded, not hidden.

## What this is not

This demo is not the Paxei product and not the PharmFlows product. It models the guardrail pattern those products use, at miniature scale, with invented sample data. No real patient records, claims, or model outputs appear here, and no accuracy, speed, or outcome number is claimed. A real guardrail would run its checks against real records and real model outputs, and would add checks this demo does not model, such as grounding a claim against a source document. Neither the model nor the records are modeled here.

## Links

1. Portfolio: https://nirmeetrao.com
2. GitHub: https://github.com/Zaczee77
3. LinkedIn: https://www.linkedin.com/in/nirmeet-rao
