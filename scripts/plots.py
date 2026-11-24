import glob
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

C = ["#2a78d6", "#eb6834", "#1baf7a"]
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281"]
MARKERS = ["o", "s", "^", "D", "v"]
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
    "axes.spines.right": False, "lines.linewidth": 2, "lines.markersize": 7,
    "legend.frameon": False, "font.size": 10, "axes.titlesize": 11,
})
SEQ = LinearSegmentedColormap.from_list("seq", ["#f0f5fc", "#86b6ef", "#2a78d6", "#0d366b"])
HEAT = LinearSegmentedColormap.from_list("heat", ["#fbf1ea", "#f2a27e", "#eb6834", "#8a3412"])
DIV = LinearSegmentedColormap.from_list("div", ["#104281", "#2a78d6", "#f0efec", "#e34948", "#8c1f1f"])
MAXIT = 30


def load(path):
    with open(path) as f:
        cols = f.readline().lstrip("#").split()
    d = np.atleast_2d(np.loadtxt(path))
    return {c: d[:, i] for i, c in enumerate(cols)}


def ref_slope(ax, h, e, order):
    ax.loglog(h, 0.3 * e[-1] * (h / h[-1]) ** order, "--", color=MUTED, lw=1.2,
              label=rf"$O(h^{order})$")


def h_ticks(ax, h):
    ax.set_xticks(h, [f"1/{round(1 / v)}" for v in h])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())


def save(fig, name):
    os.makedirs("figures", exist_ok=True)
    fig.savefig(f"figures/{name}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"figures/{name}.png")


def q2():
    runs = [(k, f"results/q2/conv_P{k}.txt") for k in (2, 3)]
    runs = [(k, p) for k, p in runs if os.path.exists(p)]
    if not runs:
        return
    fig, axes = plt.subplots(1, len(runs), figsize=(5.2 * len(runs), 4.3), squeeze=False)
    for ax, (k, path) in zip(axes[0], runs):
        d = load(path)
        for (key, rkey, lab), col, m in zip(
                [("eu", "r_u", r"$\|u-u_h\|_1$"), ("ep", "r_p", r"$\|p-p_h\|_0$"),
                 ("eT", "r_T", r"$\|\theta-\theta_h\|_1$")], C, MARKERS):
            ax.loglog(d["h"], d[key], marker=m, color=col,
                      label=f"{lab}  (r = {d[rkey][-1]:.2f})")
        ref_slope(ax, d["h"], np.min([d["eu"], d["ep"], d["eT"]], axis=0), k)
        h_ticks(ax, d["h"])
        ax.set_title(f"P{k}-P{k-1}-P{k}")
        ax.set_xlabel("h")
        ax.legend(loc="upper left")
    axes[0][0].set_ylabel("erreur")
    save(fig, "q2_convergence")


def q3():
    if not os.path.exists("results/q3/visc_P2.txt"):
        return
    d = load("results/q3/visc_P2.txt")
    nus = sorted(set(d["nu"]), reverse=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.3))
    for ax, key, lab in zip(axes, ["eu", "ep", "eT"],
                            [r"$\|u-u_h\|_1$", r"$\|p-p_h\|_0$", r"$\|\theta-\theta_h\|_1$"]):
        for nu, col, m in zip(nus, RAMP, MARKERS):
            s = (d["nu"] == nu) & (d["niter"] < MAXIT)
            ax.loglog(d["h"][s], d[key][s], marker=m, color=col, label=rf"$\nu$ = {nu:g}")
        s = d["nu"] == nus[0]
        ref_slope(ax, d["h"][s], d[key][s], 2)
        h_ticks(ax, d["h"][s])
        ax.set_title(lab)
        ax.set_xlabel("h")
    axes[0].legend(loc="lower right")
    if np.any(d["niter"] >= MAXIT):
        fig.text(0.5, -0.02, "Points où Newton n'a pas convergé omis.", ha="center", color=INK2)
    save(fig, "q3_viscosity")


def q4():
    for path in sorted(glob.glob("results/q4/cavity_nu*.txt")):
        d = np.loadtxt(path)
        N = int(round(np.sqrt(d.shape[0])))
        x, y, u1, u2, p, T, psi = (d[:, i].reshape(N, N) for i in range(7))
        tag = os.path.basename(path)[len("cavity_"):-len(".txt")]
        fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), layout="constrained")
        for ax in axes:
            ax.set_aspect("equal")
            ax.grid(False)
            ax.set_xlabel("x")
        axes[0].set_ylabel("y")

        c = axes[0].contourf(x, y, np.hypot(u1, u2), 30, cmap=SEQ)
        axes[0].contour(x, y, psi, np.linspace(0, psi.max(), 14)[1:], colors=INK, linewidths=0.8)
        fig.colorbar(c, ax=axes[0], shrink=0.8)
        axes[0].set_title(r"$|u_h|$ et lignes de courant ($\psi$)")

        c = axes[1].contourf(x, y, T, 30, cmap=HEAT)
        axes[1].contour(x, y, T, 12, colors=INK, linewidths=0.8)
        fig.colorbar(c, ax=axes[1], shrink=0.8)
        axes[1].set_title(r"Température $\theta_h$ (isothermes)")

        c = axes[2].contourf(x, y, p, 30, cmap=DIV, norm=TwoSlopeNorm(0., p.min(), p.max()))
        fig.colorbar(c, ax=axes[2], shrink=0.8)
        axes[2].set_title(r"Pression $p_h$")

        fig.suptitle(rf"Cavité, $\nu$ = {tag[2:]}, $\kappa$ = 1")
        save(fig, f"q4_cavity_{tag}")


if __name__ == "__main__":
    targets = sys.argv[1:] or ["q2", "q3", "q4"]
    for t in targets:
        {"q2": q2, "q3": q3, "q4": q4}[t]()
