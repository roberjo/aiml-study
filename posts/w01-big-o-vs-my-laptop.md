---
week: W01
title: Learning linear algebra, finally. The textbook said n³; my laptop said n^2.1.
format: image
status: draft
posted:
url:
---

Learning linear algebra, finally!

The textbook says multiplying two matrices scales with n³. My laptop measured n^2.1. Both were right, and the gap taught me more than the math did.

Week 1 of rebuilding a 23-week AI/ML program in public, and the rule was simple: build it all by hand before touching a library. Plain Python loops, no NumPy shortcuts. Dot product, matrix-vector product, rotation, shear, matrix multiply, determinant, inverse. Seven functions, each checked against NumPy.

Then I raced my matrix multiply against NumPy's. NumPy won by 500 to 740×. No surprise.

The surprise was the slope. n×n matrices take n³ multiplications, so doubling n should cost 8×. Mine grew like n^2.1.

The answer was in my own code. My matrix-vector function scaled whole columns at once, handing each column to NumPy in one call. Only two of the three nested loops ran in Python. Big-O counts multiplications. The clock measures where the time goes, and most of mine was Python's per-loop overhead.

Three mistakes:

→ My first benchmark timed each size once. The NumPy line zigzagged because I was measuring noise. Best of 7 fixed it.
→ I pasted a code template with its ___ blanks still in it. ___ is a legal Python name, so nothing crashed. The check just quietly failed.
→ I never wrote down a guess before running the benchmark. No prediction, no gap to learn from.

The concept that finally clicked: a matrix is a list of where the basis vectors land. The minus sign in the rotation matrix made sense once I tabulated where "up" goes after a quarter turn. Left.

When did a benchmark last tell you something the Big-O didn't?

#MachineLearning #Python #LearningInPublic #SoftwareEngineering #AI

---
**First comment:** Week 1 notebooks, including the from-scratch functions, the benchmark, and my written answers: https://github.com/roberjo/aiml-study/tree/main/weeks/w01-setup
**Visual:** `posts/assets/w01-loops-vs-numpy.png` (log-log timing chart: my loops vs NumPy). Alternative: `posts/assets/w01-order-matters.png` (rotate-then-shear vs shear-then-rotate panels).
