from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _sort_curs_academic(values: list[str]) -> list[str]:
    """Ordena strings tipo '18-19', '19-20', ... por el primer año (18, 19, ...)."""
    def key_fun(x: str) -> int:
        x = str(x)
        try:
            return int(x.split("-")[0])
        except Exception:
            return 999  

    return sorted(values, key=key_fun)


def plot_time_trends(merged_df: pd.DataFrame, output_path: str) -> None:
    """Genera y guarda dos series temporales (abandono y rendimiento) por Branca."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    cursos = _sort_curs_academic(list(merged_df["Curs Acadèmic"].dropna().unique()))
    branches = sorted(list(merged_df["Branca"].dropna().unique()))

    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    ax1 = axes[0]
    ax2 = axes[1]

    cmap = plt.cm.tab10

    for i, branch in enumerate(branches):
        df_b = merged_df[merged_df["Branca"] == branch].copy()

        # media por curso
        serie = (
            df_b.groupby("Curs Acadèmic")["% Abandonament a primer curs"]
            .mean()
            .reindex(cursos)
        )
        ax1.plot(cursos, serie.values, label=branch, color=cmap(i % 10))

        serie2 = (
            df_b.groupby("Curs Acadèmic")["Taxa rendiment"]
            .mean()
            .reindex(cursos)
        )
        ax2.plot(cursos, serie2.values, label=branch, color=cmap(i % 10))

    ax1.set_title("Evolució del % d'abandonament per curs acadèmic")
    ax1.set_ylabel("% Abandonament a primer curs")
    ax1.grid(True)
    ax1.legend(loc="best", fontsize=9)

    ax2.set_title("Evolució de la taxa de rendiment per curs acadèmic")
    ax2.set_xlabel("Curs Acadèmic")
    ax2.set_ylabel("Taxa rendiment")
    ax2.grid(True)
    ax2.legend(loc="best", fontsize=9)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out, dpi=300)
    plt.close(fig)
