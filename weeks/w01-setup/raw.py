import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="W1 · Linear algebra by hand")

with app.setup:
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # W1 · Linear algebra by hand

    Raw pass for 3Blue1Brown's *Essence of Linear Algebra*, chapters 1–7. The big idea:
    **a matrix is a transformation of space, and its columns say where the basis vectors land.**

    **How this works**

    1. Each function below is a stub. Replace `raise NotImplementedError` with your code.
    2. Use plain Python loops and indexing. No `@`, `np.dot`, `np.matmul`, or `np.linalg` inside
       your functions (`np.array`, `np.zeros`, `np.cos`, and `np.sin` are fine).
    3. The **checks** table updates as you go: ⏳ not started · ❌ wrong · ✅ correct.
    4. The **plots** come alive as functions start working. Use them to answer the questions at the bottom.

    Run with `uv run marimo edit weeks/w01-setup/raw.py`.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1 · Vectors and transformations (ch. 1–3)
    """)
    return


@app.function
def dot(u, v):
    """Dot product: the sum of u[i] * v[i].

    Hint: one loop, one running total. (Geometry of this is ch. 9; not needed yet.)
    """
    total = 0
    for i in range(len(u)):
        total += u[i] * v[i]
    return total


@app.function
def matvec(A, x):
    """Apply matrix A (m x n) to vector x (length n). Returns a length-m vector.

    Hint (ch. 3): A @ x is x[0] * (column 0 of A) + x[1] * (column 1 of A) + ...
    Build it that way: a linear combination of A's columns. Then, as a bonus, write a
    second version using dot() on A's rows, and convince yourself why both agree.
    """
    m, n = A.shape
    total = np.zeros(m)
    for j in range(n):
        total = total + x[j] * A[:, j]
    return total


@app.function
def rotation(theta):
    """2x2 matrix that rotates the plane counterclockwise by theta radians.

    Hint (ch. 3): where does i-hat = (1, 0) land after rotating by theta? And j-hat = (0, 1)?
    Those two landing spots are the matrix's columns.
    """
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])


@app.function
def shear(k):
    """2x2 shear: i-hat stays put, j-hat moves to (k, 1)."""
    return np.array([[1, k],
                     [0, 1]])


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2 · Composition (ch. 4)
    """)
    return


@app.function
def matmul(A, B):
    """Matrix product A @ B for A (m x n) and B (n x p). Returns an m x p array.

    Hint (ch. 4): column j of A @ B is A applied to column j of B. You already wrote that.
    Make sure it works for non-square shapes.
    """
    m, n = A.shape
    n2, p = B.shape
    result = np.zeros((m, p))
    for j in range(p):
        result[:, j] = matvec(A, B[:, j])
    return result


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3 · Determinant and inverse (ch. 6–7)
    """)
    return


@app.function
def det2(A):
    """Determinant of a 2x2 matrix: the factor by which A scales area.

    Negative means orientation flipped (i-hat and j-hat swapped sides). Watch the gold
    square in the plots before you look up the formula, then derive it if you can.
    """
    a, b = A[0][0], A[0][1]
    c, d = A[1][0], A[1][1]
    return a * d - b * c


@app.function
def inverse2(A):
    """Inverse of a 2x2 matrix: the transformation that undoes A.

    Return None when det2(A) == 0: space got squished onto a line, so there's no way back (ch. 7).
    """
    det = det2(A)
    if det == 0:
        return None
    a, b = A[0][0], A[0][1]
    c, d = A[1][0], A[1][1]
    return np.array([[d, -b],
                     [-c, a]]) / det


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Checks
    """)
    return


@app.cell(hide_code=True)
def _():
    rng = np.random.default_rng(1)
    _A, _B, _x = rng.normal(size=(2, 3)), rng.normal(size=(3, 4)), rng.normal(size=3)
    _M, _u, _v = rng.normal(size=(2, 2)), rng.normal(size=5), rng.normal(size=5)
    _t, _c, _s = 0.7, np.cos(0.7), np.sin(0.7)
    _singular = np.array([[1.0, 2.0], [2.0, 4.0]])

    _checks = {
        "dot": lambda: np.isclose(dot(_u, _v), _u @ _v),
        "matvec": lambda: np.allclose(matvec(_A, _x), _A @ _x),
        "rotation": lambda: np.allclose(rotation(_t), [[_c, -_s], [_s, _c]]),
        "shear": lambda: np.allclose(shear(1.5), [[1, 1.5], [0, 1]]),
        "matmul": lambda: np.allclose(matmul(_A, _B), _A @ _B),
        "det2": lambda: np.isclose(det2(_M), np.linalg.det(_M)),
        "inverse2": lambda: (
            np.allclose(inverse2(_M), np.linalg.inv(_M)) and inverse2(_singular) is None
        ),
    }

    def _status(check):
        try:
            return "✅" if check() else "❌ wrong answer"
        except NotImplementedError:
            return "⏳ not started"
        except Exception as e:  # shape bugs, typos, etc.
            return f"❌ {type(e).__name__}: {e}"

    _rows = "\n".join(f"| `{name}` | {_status(c)} |" for name, c in _checks.items())
    mo.md(f"| Function | Status |\n|---|---|\n{_rows}")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Play: rotation, shear, and the order of operations
    """)
    return


@app.function
def draw_transform(ax, M, title):
    """Plot how M moves the grid, the unit square (gold), i-hat (green), and j-hat (red)."""
    ax.set_title(title, fontsize=10)
    ax.set(xlim=(-3, 3), ylim=(-3, 3), aspect="equal", xticks=[], yticks=[])
    ax.axhline(0, color="0.85", lw=0.8)
    ax.axvline(0, color="0.85", lw=0.8)
    if M is None:
        ax.text(0, 0, "not implemented yet", ha="center", va="center", color="0.5")
        return
    M = np.asarray(M, dtype=float)
    for c in range(-4, 5):
        for line in (np.array([[c, c], [-4, 4]]), np.array([[-4, 4], [c, c]])):
            pts = M @ line
            ax.plot(pts[0], pts[1], color="steelblue", lw=0.6, alpha=0.5)
    square = M @ np.array([[0, 1, 1, 0], [0, 0, 1, 1]])
    ax.fill(square[0], square[1], color="gold", alpha=0.45)
    for col, color in ((0, "green"), (1, "crimson")):
        ax.quiver(
            0,
            0,
            M[0, col],
            M[1, col],
            angles="xy",
            scale_units="xy",
            scale=1,
            color=color,
            width=0.012,
        )
    try:
        ax.set_xlabel(f"det = {det2(M):.2f}", fontsize=9)
    except NotImplementedError:
        pass


@app.function
def attempt(f, *args):
    """Call f, returning None if it isn't implemented yet or got None inputs."""
    if any(a is None for a in args):
        return None
    try:
        return f(*args)
    except NotImplementedError:
        return None


@app.cell
def _():
    theta = mo.ui.slider(-180, 180, value=30, step=5, label="rotation θ (degrees)")
    k = mo.ui.slider(-2, 2, value=1, step=0.25, label="shear k")
    mo.hstack([theta, k], justify="start", gap=2)
    return k, theta


@app.cell
def _(k, theta):
    _R = attempt(rotation, np.radians(theta.value))
    _S = attempt(shear, k.value)
    _panels = [
        ("R: rotation", _R),
        ("S: shear", _S),
        ("R·S: shear first, then rotate", attempt(matmul, _R, _S)),
        ("S·R: rotate first, then shear", attempt(matmul, _S, _R)),
    ]
    _fig, _axes = plt.subplots(1, 4, figsize=(14, 3.9))
    for _ax, (_title, _M) in zip(_axes, _panels, strict=True):
        draw_transform(_ax, _M, _title)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Your matrix

    Edit `my_matrix` and watch what it does. Try to find: a reflection, a matrix with det = 0,
    and one with det = −2. The right panel applies your inverse, so it should snap back to the
    original square.
    """)
    return


@app.cell
def _():
    my_matrix = np.array([[1.0, 2.0], [0.5, 1.5]])
    return (my_matrix,)


@app.cell
def _(my_matrix):
    _inv = attempt(inverse2, my_matrix)
    _fig, (_a, _b) = plt.subplots(1, 2, figsize=(7, 3.6))
    draw_transform(_a, my_matrix, "my_matrix")
    draw_transform(_b, attempt(matmul, _inv, my_matrix), "inverse2(my_matrix) · my_matrix")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Questions (answer in the week's README, not here)

    Predict first, then use the sliders to check.

    1. Is R·S the same as S·R? For which values of θ or k are they equal, and why?
    2. What is the determinant of any rotation? Of any shear? Explain it geometrically before algebraically.
    3. What happens to the gold square when det = 0? Why does that make `inverse2` impossible?
    4. Your `matvec` builds the answer from **columns**. Why is that the same as taking dot products with **rows**?
    5. Which chapter's idea surprised you most, and what were you picturing wrong before?
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
