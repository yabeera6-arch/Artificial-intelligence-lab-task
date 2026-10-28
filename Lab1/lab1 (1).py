
def symbolic(score, complete): return "Review" if complete and score >= 70 else "Hold"
def threshold(probability): return "Review" if probability >= 0.70 else "Hold"

print("Part 1: Symbolic vs Threshold")
for name, score, complete, prob in [("complete_high", 82, True, 0.81), ("complete_low", 68, True, 0.74), ("incomplete_high", 91, False, 0.88), ("boundary", 70, True, 0.70)]:
    a, b = symbolic(score, complete), threshold(prob)
    print(f"{name} | symbolic={a} | threshold={b} | disagreement={a != b}")

def rule(score, complete, deadline, recommendation): return "Review" if score >= 70 and complete and deadline and recommendation else "Hold"

print("\nPart 2: Modified Rule Tests")
for name, score, complete, deadline, recommendation, expected, reason in [
    ("Pass", 82, True, True, True, "Review", "All rules are true."),
    ("Fail deadline", 85, True, False, True, "Hold", "Deadline was missed."),
    ("Fail recommendation", 88, True, True, False, "Hold", "Recommendation letter is missing."),
    ("Boundary 70", 70, True, True, True, "Review", "70 is included in 70 or more.")]:
    actual = rule(score, complete, deadline, recommendation)
    print(f"{name} | Input: score={score}, documents_complete={complete}, deadline_met={deadline}, recommendation_present={recommendation} | Expected: {expected} | Actual: {actual} | Passed: {actual == expected} | Reason: {reason}")
