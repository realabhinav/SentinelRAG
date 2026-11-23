"""Run a small labeled retrieval evaluation with python evaluate.py."""
from copilot import load_corpus, retrieve

CASES = [
    ("How can I verify recovered records?", "backup"),
    ("Review assigned privileges", "identity"),
    ("Where are proxy access events recorded?", "logging"),
    ("Which assets lack an owner?", "inventory"),
    ("Restrict outbound destinations", "egress"),
    ("Rotate a TLS certificate", None),
    ("Calculate payroll deductions", None),
]


def evaluate():
    corpus = load_corpus()
    correct = rejected = total = unknown = 0
    for question, expected in CASES:
        ranked = retrieve(question, corpus)
        first = next(iter(ranked), None)
        print(f"{question} | expected={expected} | retrieved={first}")
        if expected is None:
            rejected += first is None
            unknown += 1
        else:
            correct += first == expected
            total += 1
    print(f"Top-1 hits: {correct}/{total}. Correct abstentions: {rejected}/{unknown}.")


if __name__ == "__main__":
    evaluate()
