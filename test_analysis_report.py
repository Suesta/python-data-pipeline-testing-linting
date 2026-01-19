import json
import unittest
from pathlib import Path

import pandas as pd

from src.modules.analysis_report import analyze_dataset


class TestAnalysisReport(unittest.TestCase):
    def test_analyze_dataset_creates_json_and_structure(self) -> None:
        df = pd.DataFrame(
            {
                "Curs Acadèmic": ["19-20", "20-21"],
                "Tipus universitat": ["PÚBLICA", "PÚBLICA"],
                "Sigles": ["UB", "UB"],
                "Tipus Estudi": ["grau", "grau"],
                "Branca": ["Ciències", "Ciències"],
                "Sexe": ["DONA", "DONA"],
                "Integrat S/N": ["Integrat", "Integrat"],
                "Taxa rendiment": [0.9, 0.8],
                "% Abandonament a primer curs": [0.1, 0.2],
            }
        )

        out_path = Path("src/report/test_analisi_estadistic.json")
        if out_path.exists():
            out_path.unlink()

        result = analyze_dataset(df, output_json_path=str(out_path))

        self.assertTrue(out_path.exists())
        self.assertIn("metadata", result)
        self.assertIn("estadisticas_globales", result)
        self.assertIn("analisis_por_rama", result)
        self.assertIn("rankings", result)

        # también comprobamos que el JSON se puede leer
        with out_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("metadata", data)

        # limpieza
        out_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
