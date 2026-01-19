from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd
from scipy.stats import linregress, pearsonr


def _to_python_number(x: Any) -> Any:
    """Convierte tipos numpy/pandas a tipos Python para poder guardar en JSON."""
    if pd.isna(x):
        return None
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    return x


def _trend_label(slope: float) -> str:
    """Clasifica tendencia según umbral del enunciado."""
    if slope > 0.01:
        return "creciente"
    if slope < -0.01:
        return "decreciente"
    return "estable"


def analyze_dataset(merged_df: pd.DataFrame, output_json_path: str) -> Dict[str, Any]:
    """Realiza análisis estadístico y lo guarda en un JSON.

    Args:
        merged_df: dataset fusionado del ejercicio 2.
        output_json_path: ruta donde guardar el JSON.

    Returns:
        Diccionario con el análisis (también se guarda en disco).
    """
    # --- 4.1 metadata ---
    periodo = sorted(merged_df["Curs Acadèmic"].dropna().unique().tolist())

    analysis: Dict[str, Any] = {
        "metadata": {
            "fecha_analisis": datetime.now().strftime("%Y-%m-%d"),
            "num_registros": int(len(merged_df)),
            "periodo_temporal": periodo,
        }
    }

    # --- 4.2 global ---
    abandono = merged_df["% Abandonament a primer curs"].astype(float)
    rendimiento = merged_df["Taxa rendiment"].astype(float)

    abandono_medio = float(abandono.mean())
    rendimiento_medio = float(rendimiento.mean())

    # correlación Pearson (aseguramos pares sin NaN)
    valid = merged_df[["% Abandonament a primer curs", "Taxa rendiment"]].dropna()
    if len(valid) >= 2:
        corr, p_value = pearsonr(
            valid["% Abandonament a primer curs"].astype(float),
            valid["Taxa rendiment"].astype(float),
        )
        corr_val = float(corr)
        p_val = float(p_value)
    else:
        corr_val = None
        p_val = None

    analysis["estadisticas_globales"] = {
        "abandono_medio": abandono_medio,
        "rendimiento_medio": rendimiento_medio,
        "correlacion_abandono_rendimiento": {
            "pearson_corr": corr_val,
            "p_value": p_val,
        },
    }

    # --- 4.3 por rama ---
    ramas = sorted(merged_df["Branca"].dropna().unique().tolist())
    por_rama: Dict[str, Any] = {}

    for rama in ramas:
        df_r = merged_df[merged_df["Branca"] == rama].copy()

        # descriptivas
        ab_mean = float(df_r["% Abandonament a primer curs"].mean())
        ab_std = float(df_r["% Abandonament a primer curs"].std())
        re_mean = float(df_r["Taxa rendiment"].mean())
        re_std = float(df_r["Taxa rendiment"].std())

        # tendencia temporal del abandono (media por año)
        by_year = (
            df_r.groupby("Curs Acadèmic")["% Abandonament a primer curs"]
            .mean()
            .reset_index()
        )

        years = by_year["Curs Acadèmic"].tolist()
        values = by_year["% Abandonament a primer curs"].astype(float).tolist()

        # usamos posiciones 0..n-1 
        if len(values) >= 2:
            slope, intercept, r_value, p_value_lr, std_err = linregress(
                range(len(years)),
                values,
            )
            slope_f = float(slope)
            trend = _trend_label(slope_f)
            r_val = float(r_value)
            p_lr = float(p_value_lr)
            se = float(std_err)
        else:
            slope_f = None
            trend = "estable"
            r_val = None
            p_lr = None
            se = None

        por_rama[rama] = {
            "estadisticas": {
                "abandono_media": ab_mean,
                "abandono_std": ab_std,
                "rendimiento_media": re_mean,
                "rendimiento_std": re_std,
            },
            "tendencia_abandono": {
                "pendiente": slope_f,
                "clasificacion": trend,
                "r_value": r_val,
                "p_value": p_lr,
                "std_err": se,
                "periodo": years,
            },
        }

    analysis["analisis_por_rama"] = por_rama

    # --- 4.4 rankings ---
    # calculamos medias por rama para ranking
    resumen_ramas = (
        merged_df.groupby("Branca")[["Taxa rendiment", "% Abandonament a primer curs"]]
        .mean()
        .reset_index()
    )

    # mejor/peor rendimiento
    best_r = resumen_ramas.sort_values("Taxa rendiment", ascending=False).iloc[0]
    worst_r = resumen_ramas.sort_values("Taxa rendiment", ascending=True).iloc[0]

    # mayor/menor abandono
    worst_a = resumen_ramas.sort_values("% Abandonament a primer curs", ascending=False).iloc[0]
    best_a = resumen_ramas.sort_values("% Abandonament a primer curs", ascending=True).iloc[0]

    analysis["rankings"] = {
        "rama_mejor_rendimiento": {
            "branca": best_r["Branca"],
            "taxa_rendiment": float(best_r["Taxa rendiment"]),
        },
        "rama_peor_rendimiento": {
            "branca": worst_r["Branca"],
            "taxa_rendiment": float(worst_r["Taxa rendiment"]),
        },
        "rama_mayor_abandono": {
            "branca": worst_a["Branca"],
            "abandono": float(worst_a["% Abandonament a primer curs"]),
        },
        "rama_menor_abandono": {
            "branca": best_a["Branca"],
            "abandono": float(best_a["% Abandonament a primer curs"]),
        },
    }

    # --- guardar JSON ---
    out_path = Path(output_json_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # limpieza final por si queda algún tipo raro
    def sanitize(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: sanitize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [sanitize(v) for v in obj]
        return _to_python_number(obj)

    analysis_clean = sanitize(analysis)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(analysis_clean, f, ensure_ascii=False, indent=2)

    return analysis_clean
