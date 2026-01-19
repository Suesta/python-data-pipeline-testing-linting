from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


def get_default_dataset_path(option: str) -> Path:
    """Devuelve la ruta por defecto segun opcion ('rendiment' o 'abandonament').

    Args:
        option: opcion del usuario. Se aceptan variantes tipo '1', '2', 'r', 'a'.

    Returns:
        Path relativo al fichero excel dentro de data/.
    """
    option_clean = option.strip().lower()

    if option_clean in {"1", "rendiment", "rendimiento", "r"}:
        return Path("data") / "rendiment_estudiants.xlsx"

    if option_clean in {"2", "abandonament", "abandono", "a"}:
        return Path("data") / "taxa_abandonament.xlsx"

    raise ValueError("Opcion no valida. Usa 1/2 o rendiment/abandonament.")


def load_dataset(path: Optional[str] = None) -> pd.DataFrame:
    """Carga uno de los dos datasets.

    Si 'path' es None, pregunta al usuario por consola qué dataset cargar.

    Args:
        path: ruta relativa al fichero .xlsx.

    Returns:
        DataFrame con el contenido del excel.
    """
    if path is None:
        print("Que dataset quieres cargar?")
        print("  1) rendiment_estudiants.xlsx (tasa rendimiento)")
        print("  2) taxa_abandonament.xlsx (tasa abandono)")
        user_opt = input("Elige 1 o 2: ")
        file_path = get_default_dataset_path(user_opt)
    else:
        file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"No existe el fichero: {file_path}")

    # leo el excel
    df = pd.read_excel(file_path)

    return df


def show_basic_eda(df: pd.DataFrame) -> None:
    """Muestra una exploracion basica del dataframe: head, columnas e info."""
    print("\n--- HEAD (5 primeras filas) ---")
    print(df.head(5))

    print("\n--- COLUMNAS ---")
    print(list(df.columns))

    print("\n--- INFO ---")
    df.info()
