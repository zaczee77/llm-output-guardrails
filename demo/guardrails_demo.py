"""Reference demo: an LLM output guardrail for model outputs.

Plain Python, standard library only. No network calls. Every sample
output is invented data written only to exercise the pattern.

The pattern: a model output never leaves the pipeline on its own. Five
checks run on every output, in the same order: required fields present,
blocked wording absent, personal identifiers absent, confidence high
enough, and numbers inside a plausible range. Each output leaves with
exactly one outcome: pass, pass with redaction, escalate, or block.
A redaction is recorded. A block stops the output from being used.
"""

import re

CONFIDENCE_THRESHOLD = 0.6
AMOUNT_MIN = 0
AMOUNT_MAX = 100000

REQUIRED_FIELDS = ("summary", "amount", "confidence")
BLOCKED_PHRASES = ("guaranteed approval", "definitely covered")

PHONE_PATTERN = re.compile(r"\d{3}-\d{3}-\d{4}")
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SSN_PATTERN = re.compile(r"\d{3}-\d{2}-\d{4}")


class GuardrailResult:
    """One output and the single outcome the guardrail gave it."""

    def __init__(self, output_id, title):
        self.output_id = output_id
        self.title = title
        self.outcome = None
        self.reason = None
        self.redactions = []
        self.summary = None


def redact(text):
    """Replace personal identifiers with markers, and report each one."""
    redactions = []
    if PHONE_PATTERN.search(text):
        redactions.append("phone number")
        text = PHONE_PATTERN.sub("[phone redacted]", text)
    if EMAIL_PATTERN.search(text):
        redactions.append("email address")
        text = EMAIL_PATTERN.sub("[email redacted]", text)
    if SSN_PATTERN.search(text):
        redactions.append("social security number")
        text = SSN_PATTERN.sub("[identifier redacted]", text)
    return text, redactions


def guardrail(output):
    """Run the five checks in order and return one outcome."""
    result = GuardrailResult(output["id"], output["title"])

    missing = [field for field in REQUIRED_FIELDS
               if field not in output]
    if missing:
        result.outcome = "blocked"
        result.reason = "missing required field: " + ", ".join(missing)
        return result

    summary = output["summary"]
    for phrase in BLOCKED_PHRASES:
        if phrase in summary.lower():
            result.outcome = "blocked"
            result.reason = "blocked wording present: " + phrase
            return result

    clean_summary, redactions = redact(summary)
    result.summary = clean_summary
    result.redactions = redactions

    if output["confidence"] < CONFIDENCE_THRESHOLD:
        result.outcome = "escalated"
        result.reason = ("confidence " + str(output["confidence"])
                         + " below threshold " + str(CONFIDENCE_THRESHOLD))
        return result

    amount = output["amount"]
    if amount < AMOUNT_MIN or amount > AMOUNT_MAX:
        result.outcome = "escalated"
        result.reason = ("amount " + str(amount)
                         + " outside plausible range "
                         + str(AMOUNT_MIN) + " to " + str(AMOUNT_MAX))
        return result

    if redactions:
        result.outcome = "passed with redaction"
        result.reason = "redacted " + " and ".join(redactions)
    else:
        result.outcome = "passed"
        result.reason = "all five checks satisfied"
    return result


def build_outputs():
    return [
        {"id": 1,
         "title": "Claim summary, routine imaging",
         "summary": "Claim summary ready for review.",
         "amount": 450.00,
         "confidence": 0.92},
        {"id": 2,
         "title": "Claim note, patient called in",
         "summary": "Patient at 555-123-4567 called about the claim.",
         "amount": 120.00,
         "confidence": 0.88},
        {"id": 3,
         "title": "Coverage summary, specialty drug request",
         "summary": "This claim is guaranteed approval.",
         "amount": 300.00,
         "confidence": 0.95},
        {"id": 4,
         "title": "Eligibility summary, new patient",
         "summary": "Eligibility looks likely, details to confirm.",
         "amount": 200.00,
         "confidence": 0.42},
        {"id": 5,
         "title": "Billing note, amount missing",
         "summary": "Billing note ready for review.",
         "confidence": 0.81},
        {"id": 6,
         "title": "Claim summary, high value case",
         "summary": "Large claim summary ready for review.",
         "amount": 250000.00,
         "confidence": 0.90},
    ]


def main():
    results = [guardrail(output) for output in build_outputs()]
    for result in results:
        print("Output " + str(result.output_id) + ": " + result.title)
        print("  outcome: " + result.outcome)
        print("  reason: " + result.reason)
        if result.summary is not None:
            print("  summary after guardrail: " + result.summary)
    passed = sum(1 for r in results if r.outcome == "passed")
    redacted = sum(1 for r in results
                   if r.outcome == "passed with redaction")
    blocked = sum(1 for r in results if r.outcome == "blocked")
    escalated = sum(1 for r in results if r.outcome == "escalated")
    total_redactions = sum(len(r.redactions) for r in results)
    print("")
    print("Summary: " + str(len(results)) + " outputs checked, "
          + str(passed) + " passed, "
          + str(redacted) + " passed with redaction, "
          + str(blocked) + " blocked, "
          + str(escalated) + " escalated, "
          + str(total_redactions) + " redaction made.")
    assert all(r.outcome is not None for r in results), \
        "every output needs exactly one outcome"
    assert passed + redacted + blocked + escalated == len(results), \
        "every output ends in exactly one outcome"
    for result in results:
        if result.outcome in ("passed", "passed with redaction"):
            assert not PHONE_PATTERN.search(result.summary), \
                "no phone number may leave the pipeline"
            assert not EMAIL_PATTERN.search(result.summary), \
                "no email address may leave the pipeline"
            assert not SSN_PATTERN.search(result.summary), \
                "no identifier may leave the pipeline"
    print("Checks passed: every output has one outcome, blocked outputs "
          "were stopped, and no personal identifier left the pipeline.")


if __name__ == "__main__":
    main()
