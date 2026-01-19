from __future__ import annotations

from typing import Tuple

import pandas as pd


GROUP_COLS = [
    "Curs Acadèmic",
    "Tipus universitat",
    "Sigles",
    "Tipus Estudi",
    "Branca",
    "Sexe",
    "Integrat S/N",
]


def rename_abandonment_cols(df_aband: pd.DataFrame) -> pd.DataFrame:
    """Renombra columnas del dataset de abandono para homogeneizar con rendimiento."""
    df = df_aband.copy()

    rename_map = {
        # equivalencias observadas en EDA
        "Naturalesa universitat responsable": "Tipus universitat",
        "Universitat Responsable": "Universitat",
        "Sexe Alumne": "Sexe",
        "Tipus de centre": "Integrat S/N",
    }

    df = df.rename(columns=rename_map)

    return df


def drop_unused_cols(
    df_rend: pd.DataFrame, df_aband: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Elimina columnas no necesarias según enunciado."""
    df_r = df_rend.copy()
    df_a = df_aband.copy()

    # eliminar Universitat y Unitat en ambos
    for col in ["Universitat", "Unitat"]:
        if col in df_r.columns:
            df_r = df_r.drop(columns=[col])
        if col in df_a.columns:
            df_a = df_a.drop(columns=[col])

    # en rendimiento, además eliminar créditos
    for col in ["Crèdits ordinaris superats", "Crèdits ordinaris matriculats"]:
        if col in df_r.columns:
            df_r = df_r.drop(columns=[col])

    return df_r, df_a


def aggregate_by_branch(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Agrupa por GROUP_COLS y calcula la media de value_col."""
    if value_col not in df.columns:
        raise ValueError(f"No existe la columna de valor '{value_col}' en el dataframe.")

    # nos quedamos con columnas clave + valor 
    cols_to_use = [c for c in GROUP_COLS if c in df.columns] + [value_col]
    df2 = df[cols_to_use].copy()

    # groupby + mean
    df_agg = (
        df2.groupby(GROUP_COLS, dropna=False)[value_col]
        .mean()
        .reset_index()
    )

    return df_agg


def merge_datasets(df_rend_agg: pd.DataFrame, df_aband_agg: pd.DataFrame) -> pd.DataFrame:
    """Fusiona ambos datasets agregados usando un inner merge."""
    merged_df = pd.merge(df_rend_agg, df_aband_agg, on=GROUP_COLS, how="inner")
    return merged_df


def build_merged_dataset(df_rend: pd.DataFrame, df_aband: pd.DataFrame) -> pd.DataFrame:
    """Pipeline completo del ejercicio 2: renombrar, eliminar, agrupar y fusionar."""
    df_aband2 = rename_abandonment_cols(df_aband)
    df_rend2, df_aband3 = drop_unused_cols(df_rend, df_aband2)

    df_rend_agg = aggregate_by_branch(df_rend2, value_col="Taxa rendiment")
    df_aband_agg = aggregate_by_branch(df_aband3, value_col="% Abandonament a primer curs")

    merged_df = merge_datasets(df_rend_agg, df_aband_agg)
    return merged_df
