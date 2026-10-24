# W1 · Nov 2 — AI landscape + math refresher

## Learn
- [ ] [Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra), chapters 1–7
- [ ] [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course), intro modules

## Build
- [x] Repo scaffold and uv environment
- [x] Free Gemini + Groq keys in `.env`
- [ ] `uv run marimo tutorial intro` (10 minutes, if marimo is new to you)
- [ ] **Raw pass:** `uv run marimo edit weeks/w01-setup/raw.py`. Implement the seven stubs
      (dot, matvec, rotation, shear, matmul, det2, inverse2) until every check is ✅
- [ ] **Framework pass:** `uv run marimo edit weeks/w01-setup/build.py`. Your loops vs NumPy `@`
- [ ] Answer the notebook questions below
- [ ] Accounts: Kaggle, Hugging Face (needed by W3 and W10)
- [ ] Install Quarto (`brew install --cask quarto`; needed by the first write-up)

Suggested pacing: videos 1–4 + `rotation`/`shear`/`matvec` on weeknight 1; videos 5–7 +
`matmul`/`det2`/`inverse2` on weeknight 2; Saturday for `build.py`, the questions, and the
ML Crash Course.

## Answers

**raw.py**
1. R·S vs S·R:
2. Determinant of rotations and shears:
3. det = 0 and why there's no inverse:
4. Columns vs rows in matvec:
5. Biggest surprise:

**build.py**
1. My guess vs actual speedup, and the log-log slope:
2. Where NumPy's speed comes from:
3. Why `solve` beats `inv`:

## Findings

## Thoughts

## Trade-offs

## Mistakes

## Lessons learned
