# W1 · Nov 2 — AI landscape + math refresher

## Learn
- [ ] [Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra), chapters 1–7
- [ ] Google ML Crash Course intro:
  - [ ] [Intro to Machine Learning](https://developers.google.com/machine-learning/intro-to-ml)
  - [ ] [Prerequisites and prework](https://developers.google.com/machine-learning/crash-course/prereqs-and-prework)

## Build
- [x] Repo scaffold and uv environment
- [x] Free Gemini + Groq keys in `.env`
- [ ] `uv run marimo tutorial intro` (10 minutes, if marimo is new to you)
- [x] **Raw pass:** `uv run marimo edit weeks/w01-setup/raw.py`. Implement the seven stubs
      (dot, matvec, rotation, shear, matmul, det2, inverse2) until every check is ✅
- [x] **Framework pass:** `uv run marimo edit weeks/w01-setup/build.py`. Your loops vs NumPy `@`
- [x] Answer the notebook questions below
- [ ] Accounts: Kaggle, Hugging Face (needed by W3 and W10)
- [ ] Install Quarto (`brew install --cask quarto`; needed by the first write-up)

Suggested pacing: videos 1–4 + `rotation`/`shear`/`matvec` on weeknight 1; videos 5–7 +
`matmul`/`det2`/`inverse2` on weeknight 2; Saturday for `build.py`, the questions, and the
ML Crash Course.

## Answers

**raw.py**

1. **R·S vs S·R:** Not the same in general. At θ = 30°, k = 1 the two panels are visibly
   different parallelograms: shearing then rotating isn't rotating then shearing. They're equal
   only when k = 0 (the shear is the identity), θ = 0° (the rotation is the identity), or
   θ = ±180°. That last case is the non-obvious one: a half turn sends every vector to −1 times
   itself, and scaling everything by the same number commutes with any linear map. On paper,
   with S = I + kN, they commute exactly when R·N = N·R, which forces sin θ = 0.
2. **Determinants of rotations and shears:** Both are always 1. A rotation is rigid: it turns
   the square without stretching it (cos²θ + sin²θ = 1). A shear slides the top edge sideways
   but keeps the base (1) and height (1), so the area is unchanged (1·1 − k·0 = 1). That's why
   every panel reads det = 1.00, even R·S and S·R, which differ in shape but not in area.
3. **det = 0 and why there's no inverse:** The gold square flattens onto a line. The two columns
   point the same way (for [[1, 2], [2, 4]], the second column is twice the first), so the whole
   plane collapses onto one line. Many different inputs land on the same output, so there's no
   way to tell which one you started from. The inverse formula divides by det, which fails at 0.
4. **Columns vs rows in matvec:** Output entry i is the sum over j of A[i, j]·x[j]. The column
   view groups that double sum by j (x[j] times column j, added up); the row view groups it by
   i (row i dotted with x). Same m·n products, added in a different order.
5. **Biggest surprise:** The minus sign in the rotation matrix. I couldn't see where j-hat
   lands until I tabulated i-hat and j-hat at 0°, 90°, 180°, 270° next to cos and sin. j-hat's
   y matched cos θ, and its x matched −sin θ: rotating "up" counterclockwise pushes it left.

**build.py**

1. **Guess vs actual, and the slope:** I didn't write a guess down before running it. Actual:
   NumPy was 583× faster at 200 × 200, and 500–750× faster from n = 50 to 400. My line's slope
   from n = 50 to 400 was log(184.3 / 2.2) / log(8) ≈ **2.1, not the 3** you'd expect from n³
   multiplications. My `matvec` does `x[j] * A[:, j]`, which hands a whole column to NumPy in one
   call, so only two of the three loops run in Python. That's n² Python iterations, each doing
   n multiplications in compiled code that are cheap next to Python's per-iteration overhead.
   At large enough n, the compiled part should start to dominate and the slope should rise toward 3.
2. **Where NumPy's speed comes from:** `@` calls a BLAS library (here, Apple's Accelerate). No
   interpreter overhead per element (Python checks types and creates a number object for every
   operation), contiguous memory laid out for the CPU cache, SIMD instructions doing several
   multiply-adds at once, and multiple cores. Same arithmetic, far less overhead per operation.
3. **Why `solve` beats `inv`:** `solve(A, b)` factors A (LU decomposition) and back-substitutes
   to get x directly. `inv(A) @ b` computes the entire inverse first, which is more work, and
   then multiplies, adding more rounding error. For ill-conditioned matrices the difference in
   accuracy can be large. If you have many right-hand sides, factor once and reuse it.

## Findings

| n | My `matmul` | NumPy `@` | Speedup |
|---|---|---|---|
| 10 | 0.09 ms | 0.0007 ms | 124× |
| 50 | 2.2 ms | 0.003 ms | 702× |
| 200 | 41 ms | 0.07 ms | 583× |
| 400 | 184 ms | 0.36 ms | 514× |

- My loops scale as roughly n^2.1, not n³, because the innermost loop is vectorized.
- NumPy's own slope was only about 2.3: for small matrices its time is fixed overhead
  (the call, allocating the result) more than arithmetic, so its line is flat on the left.
- Every rotation and shear, and every product of them, has det = 1.

## Thoughts

- Building each matrix from "where do i-hat and j-hat land?" turned formulas into pictures.
- The interactive panels made the order-of-operations question something to see, not just compute.

## Trade-offs

- **Loops vs vectorized code:** writing the loops showed me what matrix multiplication *is*;
  NumPy is 500× faster. Understanding first, then the library.
- **Single timing vs repeated timing:** one run is quick to write but mostly noise at
  microsecond scale; best-of-7 costs a few lines and gives a clean plot.

## Mistakes

- Pasted a code template with its `___` blanks into `shear`. `___` is a legal Python name, so
  there was no syntax error: marimo treated it as an undefined variable and quietly turned my
  function into a regular cell, so the check failed instead of running.
- The first benchmark timed each size once. The NumPy line zigzagged randomly; it was measuring
  noise. Fixed with best-of-7.
- Expected a slope of 3 from the textbook O(n³). Measured 2.1. The textbook counts
  multiplications; my laptop measured where the time actually goes.
- Didn't write down a speedup guess before running the benchmark, so I lost the chance to see
  how wrong my intuition was.

## Lessons learned

- A matrix is just a list of where the basis vectors land. Rotation, shear, and inverse all fall
  out of that.
- Big-O counts operations; real runtime depends on which operations run in Python and which in
  compiled code.
- Benchmark properly: repeat, take the minimum, and use sizes big enough to measure.
- Make the prediction *before* running the experiment, or you can't learn from the gap.
