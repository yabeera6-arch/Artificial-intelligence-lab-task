"""Lab 1 demo: compare scholarship rules with a sample probability cutoff."""
CUTOFF = 0.70


def check_rules(score, documents_complete, income_ok, full_time):
    """Flag an application for review only when it meets every rule."""
    return "Review" if score >= 70 and all((documents_complete, income_ok, full_time)) else "Hold"


def check_probability(probability):
    """Compare the example probability with the chosen cutoff."""
    if not 0 <= probability <= 1:
        raise ValueError("Please enter a probability between 0 and 1.")
    return "Review" if probability >= CUTOFF else "Hold"


# Each example shows the applicant details, expected answers, and a short explanation.
cases = [
    ("Application passes", 82, True, True, True, .81, ("Review", "Review"), "All the rules pass, and the probability is above 0.70."),
    ("Income requirement missed", 82, True, False, True, .88, ("Hold", "Review"), "The income rule fails, but the probability is above the cutoff."),
    ("Not enrolled full-time", 91, True, True, False, .88, ("Hold", "Review"), "The enrollment rule fails, but the probability is above the cutoff."),
    ("Right on the cutoff", 70, True, True, True, .70, ("Review", "Review"), "A score of 70 and probability of 0.70 meet the cutoffs."),
]

print("Lab 1: Scholarship Screening Demo")
print("‘Review’ means a person should check the application; it is not an award.")
for name, score, documents, income_ok, full_time, probability, expected, reason in cases:
    actual = (check_rules(score, documents, income_ok, full_time), check_probability(probability))
    print(f"\n{name}\n  Input: score={score}, documents complete={documents}, income okay={income_ok}, full-time={full_time}, probability={probability:.2f}\n  Expected: rules={expected[0]}, probability={expected[1]}\n  Actual:   rules={actual[0]}, probability={actual[1]}\n  Reason: {reason}")
    assert actual == expected, f"Please check the expected result for: {name}"

# The original score and document requirements should still be enforced.
assert check_rules(69, True, True, True) == check_rules(82, False, True, True) == "Hold"
print("\nAll four examples and the original rule checks passed.")
