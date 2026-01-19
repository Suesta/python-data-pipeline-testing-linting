import unittest
import pandas as pd

from src.modules.clean_merge import (
    aggregate_by_branch,
    merge_datasets,
    GROUP_COLS,
)


class TestCleanMerge(unittest.TestCase):
    def test_aggregate_by_branch_mean(self) -> None:
        df = pd.DataFrame(
            {
                "Curs Acadèmic": ["19-20", "19-20"],
                "Tipus universitat": ["PÚBLICA", "PÚBLICA"],
                "Sigles": ["UB", "UB"],
                "Tipus Estudi": ["grau", "grau"],
                "Branca": ["Ciències", "Ciències"],
                "Sexe": ["DONA", "DONA"],
                "Integrat S/N": ["Integrat", "Integrat"],
                "Taxa rendiment": [0.8, 1.0],
                "Estudi": ["X", "Y"],  
            }
        )

        out = aggregate_by_branch(df, value_col="Taxa rendiment")
        self.assertEqual(len(out), 1)
        self.assertAlmostEqual(out.loc[0, "Taxa rendiment"], 0.9, places=7)

        # verifica que están las columnas clave
        self.assertEqual(list(out.columns), GROUP_COLS + ["Taxa rendiment"])

    def test_merge_inner(self) -> None:
        df_r = pd.DataFrame(
            {
                "Curs Acadèmic": ["19-20", "19-20"],
                "Tipus universitat": ["PÚBLICA", "PÚBLICA"],
                "Sigles": ["UB", "UB"],
                "Tipus Estudi": ["grau", "grau"],
                "Branca": ["Ciències", "Arts i humanitats"],
                "Sexe": ["DONA", "DONA"],
                "Integrat S/N": ["Integrat", "Integrat"],
                "Taxa rendiment": [0.9, 0.8],
            }
        )

        df_a = pd.DataFrame(
            {
                "Curs Acadèmic": ["19-20"],
                "Tipus universitat": ["PÚBLICA"],
                "Sigles": ["UB"],
                "Tipus Estudi": ["grau"],
                "Branca": ["Ciències"], 
                "Sexe": ["DONA"],
                "Integrat S/N": ["Integrat"],
                "% Abandonament a primer curs": [0.1],
            }
        )

        merged = merge_datasets(df_r, df_a)
        self.assertEqual(len(merged), 1)
        self.assertIn("Taxa rendiment", merged.columns)
        self.assertIn("% Abandonament a primer curs", merged.columns)


if __name__ == "__main__":
    unittest.main()
