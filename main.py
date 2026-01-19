import argparse

from src.modules import load_eda
from src.modules import clean_merge
from src.modules import visualization
from src.modules import analysis_report


def parse_args() -> argparse.Namespace:
    """Parsea argumentos de linea de comandos."""
    parser = argparse.ArgumentParser(
        description="PEC4 - Analisis de rendimiento y abandono universitario (UOC)"
    )
    parser.add_argument(
        "-ex",
        "--exercise",
        type=int,
        default=4,
        help="Ejecuta del ejercicio 1 al N (1..4). Por defecto ejecuta todos.",
    )
    return parser.parse_args()


def run(exercise: int) -> None:
    """Ejecuta la PEC de forma progresiva: 1 -> N."""
    if exercise < 1 or exercise > 4:
        raise ValueError("El valor de -ex debe estar entre 1 y 4.")

    print(f"Ejecutando ejercicios 1..{exercise}")

    if exercise >= 1:
        print("[EJ1] Carga y EDA del dataset")

        if exercise == 1:
            df = load_eda.load_dataset(path=None)  
        else:
            df = load_eda.load_dataset("data/rendiment_estudiants.xlsx")  

        load_eda.show_basic_eda(df)


    if exercise >= 2:
        print("[EJ2] Limpieza + agregación + merge")


        df_rend = load_eda.load_dataset("data/rendiment_estudiants.xlsx")
        df_aband = load_eda.load_dataset("data/taxa_abandonament.xlsx")

        merged_df = clean_merge.build_merged_dataset(df_rend, df_aband)
        print("Merged shape:", merged_df.shape)
        print("Merged columns:", list(merged_df.columns))
        print(merged_df.head(5))

    if exercise >= 3:
        print("[EJ3] Graficos de tendencias y guardado en src/img/")
        visualization.plot_time_trends(
            merged_df,
            output_path="src/img/evolucion_nombre_alumno.png"
        )
        print("Figura guardada en: src/img/evolucion_nombre_alumno.png")

    if exercise >= 4:
        print("[EJ4] Analisis estadistico y guardado JSON")
        analysis_report.analyze_dataset(
            merged_df,
            output_json_path="src/report/analisi_estadistic.json",
        )
        print("JSON guardado en: src/report/analisi_estadistic.json")


def main() -> None:
    args = parse_args()
    run(args.exercise)


if __name__ == "__main__":
    main()
