import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="W1 · Your loops vs NumPy")

with app.setup:
    import time

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from raw import matmul


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # W1 · Framework pass: your loops vs NumPy

    Do this after every check in `raw.py` is ✅. Same math, two implementations: your Python
    loops and NumPy's `@`, which hands the work to compiled BLAS code. Every ML library you'll
    use from W4 onward rests on this gap.

    **Before you run it, write down a guess:** for two 150 × 150 matrices, how many times faster is `@`?
    """)
    return


@app.cell
def _():
    sizes = [10, 25, 50, 100, 150]
    rows = []
    for n in sizes:
        rng = np.random.default_rng(n)
        A, B = rng.normal(size=(n, n)), rng.normal(size=(n, n))
        t0 = time.perf_counter()
        mine = matmul(A, B)
        t_mine = time.perf_counter() - t0
        t0 = time.perf_counter()
        theirs = A @ B
        t_numpy = time.perf_counter() - t0
        assert np.allclose(mine, theirs)
        rows.append(
            {
                "n": n,
                "your loops (s)": t_mine,
                "numpy @ (s)": t_numpy,
                "speedup": t_mine / max(t_numpy, 1e-9),
            }
        )
    mo.ui.table(rows, selection=None)
    return (rows,)


@app.cell
def _(rows):
    _fig, _ax = plt.subplots(figsize=(6, 3.6))
    _n = [r["n"] for r in rows]
    _ax.loglog(_n, [r["your loops (s)"] for r in rows], "o-", label="your loops")
    _ax.loglog(_n, [r["numpy @ (s)"] for r in rows], "o-", label="numpy @")
    _ax.set(xlabel="matrix size n", ylabel="seconds (log scale)", title="Matrix multiply time")
    _ax.legend()
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Questions (answer in the README)

    1. How far off was your guess? On a log-log plot, the slope of your line is the exponent of
       n in the running time. What slope do you get, and why should it be about 3?
    2. NumPy does the same number of multiplications. Where does the speedup come from?
    3. `np.linalg` has `det`, `inv`, and `solve`. Why do numerical people say "never compute `inv(A) @ b`,
       use `solve(A, b)`"? (One paragraph; look it up.)
    """)
    return


if __name__ == "__main__":
    app.run()
