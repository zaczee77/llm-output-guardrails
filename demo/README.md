# Demo: LLM output guardrails

A small reference demo of the guardrail pattern behind Paxei and PharmFlows: a model output passes through five deterministic checks before it can be used, and leaves with exactly one outcome: pass, pass with redaction, escalate, or block.

## How to run it

From the repository root, or from this folder:

```
python3 demo/guardrails_demo.py
```

Plain Python, no external packages, no network calls.

## What it does

1. Check output 1. A claim summary for routine imaging. All fields present, no blocked wording, no identifiers, confidence 0.92, amount 450. Passed.
2. Check output 2. A claim note that repeats a patient phone number. The number is replaced with a marker, and the output passes with redaction.
3. Check output 3. A coverage summary that promises guaranteed approval. Blocked wording present. Blocked, and the output is not used.
4. Check output 4. An eligibility summary with confidence 0.42, below the 0.6 threshold. Escalated to a person.
5. Check output 5. A billing note missing its amount field. Blocked, because the next step cannot use an output with a missing required field.
6. Check output 6. A claim summary with an amount of 250000, outside the plausible range of 0 to 100000. Escalated to a person.

## What it printed when it was tested

6 outputs checked, 1 passed, 1 passed with redaction, 2 blocked, 2 escalated, 1 redaction made. The built in checks passed: every output has one outcome, blocked outputs were stopped, and no personal identifier left the pipeline.

## What the sample data is

Every output title, summary, amount, and confidence value in `guardrails_demo.py` is invented sample data written only to exercise the pattern. Nothing here is a real model output, a real claim, a real patient record, or a real identifier. A real guardrail would run its checks against real outputs and real records. None of those are modeled here.

## Files

1. `guardrails_demo.py`: the demo. The five checks, the four outcomes, the redaction step, and the built in assertions.
2. `README.md`: this file.
