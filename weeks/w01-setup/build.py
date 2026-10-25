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

    **Before you run it, write down a guess:** for two 200 × 200 matrices, how many times faster is `@`?
    """)
    return


@app.function
def best_time(f, *args, repeats=7):
    """Fastest of several runs: one run is mostly noise at microsecond scale."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        f(*args)
        times.append(time.perf_counter() - t0)
    return min(times)


@app.cell
def _():
    sizes = [10, 25, 50, 100, 200, 400]
    rows = []
    for n in sizes:
        rng = np.random.default_rng(n)
        A, B = rng.normal(size=(n, n)), rng.normal(size=(n, n))
        assert np.allclose(matmul(A, B), A @ B)
        t_mine = best_time(matmul, A, B)
        t_numpy = best_time(np.matmul, A, B)
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

    1. How far off was your guess? On a log-log plot, the slope of a line is the exponent of n
       in the running time. Multiplying two n × n matrices takes n³ multiplications, so you'd
       expect a slope of 3. Measure your blue line's slope (pick two points: log of the time ratio
       ÷ log of the size ratio). If it isn't 3, look at what your `matvec` hands to NumPy on each
       loop iteration, and count how many loops actually run in Python.
    2. NumPy does the same number of multiplications. Where does the speedup come from?
    3. `np.linalg` has `det`, `inv`, and `solve`. Why do numerical people say "never compute `inv(A) @ b`,
       use `solve(A, b)`"? (One paragraph; look it up.)
    """)
    return


if __name__ == "__main__":
    app.run()
