---
week: W01
title: Learning linear algebra, finally. The textbook said n³; my laptop said n^2.1.
format: image
status: draft
posted:
url:
---

Learning linear algebra, finally!

The textbook says multiplying two matrices scales with n³. My laptop measured n^2.1. Both were right, and figuring out why was the best part of my week.

Week 1 of working through a 23-week AI/ML program in public. The rule: build everything by hand before a library is allowed anywhere near it. Plain Python loops. Dot product, matrix-vector product, rotation, shear, matrix multiply, determinant, inverse. Seven functions, each graded against NumPy, which is a humbling way to spend a weekend.

Then I raced my matrix multiply against NumPy's. NumPy won by 500 to 740×. I'd love to say it was close. It was not.

The surprise was the slope. n×n matrices need n³ multiplications, so doubling n should cost 8×. Mine grew like n^2.1. Had I accidentally invented a faster algorithm? Reader, I had not.

My matrix-vector function scaled whole columns at once, which quietly handed each column to NumPy. Only two of my three loops actually ran in Python. Big-O counts multiplications. The clock measures where the time goes, and most of mine went to Python overhead.

The blooper reel:

→ My first benchmark timed each size once. The NumPy line zigzagged like a seismograph. I was measuring noise. Best of 7 fixed it.
→ I pasted a code template with its ___ blanks still in it. Turns out ___ is a perfectly legal Python variable name. Nothing crashed. Nothing worked either.
→ I never wrote down a guess before running the benchmark, so I'll never know how wrong I was. Probably very.

What finally clicked: a matrix is just a list of where the basis vectors land. The minus sign in the rotation matrix made sense once I drew where "up" goes after a quarter turn. Left. It goes left.

When did a benchmark last tell you something the Big-O didn't?

#MachineLearning #Python #LearningInPublic #SoftwareEngineering #AI

---
**First comment:** Week 1 notebooks, including the from-scratch functions, the benchmark, and my written answers: https://github.com/roberjo/aiml-study/tree/main/weeks/w01-setup
**Visual:** `posts/assets/w01-loops-vs-numpy.png` (log-log timing chart: my loops vs NumPy). Alternative: `posts/assets/w01-order-matters.png` (rotate-then-shear vs shear-then-rotate panels).
