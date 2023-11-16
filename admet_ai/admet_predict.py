"""Make predictions on a dataset using Chemprop-RDKit models trained on TDC ADMET data."""
from pathlib import Path

import pandas as pd
from tap import tapify

from admet_ai import ADMETModel
from admet_ai.utils import load_and_preprocess_data


def admet_predict(
    data_path: Path,
    model_dir: Path,  # TODO: set default model dir
    save_path: Path | None = None,
    drugbank_path: Path | None = None,  # TODO: set default DrugBank path
    atc_code: str | None = None,
    smiles_column: str = "smiles",
    num_workers: int = 0,
    cache_molecules: bool = True,
) -> None:
    """Make predictions on a dataset using Chemprop-RDKit models trained on TDC ADMET data.

    :param data_path: Path to a CSV file containing a dataset of molecules.
    :param model_dir: Path to a directory containing Chemprop or Chemprop-RDKit models.
    :param save_path: Path to a CSV file where predictions will be saved. If None, defaults to data_path.
    :param drugbank_path: Path to a CSV file containing DrugBank approved molecules
                          with ADMET predictions and ATC codes.
    :param atc_code: The ATC code to filter the DrugBank reference set by.
                     If None, the entire DrugBank reference set will be used.
    :param smiles_column: Name of the column containing SMILES strings.
    :param num_workers: Number of workers for the data loader. Zero workers (i.e., sequential data loading)
                        may be faster if not using a GPU.
    :param cache_molecules: Whether to cache molecules. Caching improves prediction speed but requires more memory.

    """
    # Load and preprocess data
    data = load_and_preprocess_data(data_path=data_path, smiles_column=smiles_column)

    # Build ADMETModel
    model = ADMETModel(
        model_dirs=sorted(path for path in model_dir.iterdir() if path.is_dir()),
        drugbank_path=drugbank_path,
        atc_code=atc_code,
        num_workers=num_workers,
        cache_molecules=cache_molecules,
    )

    # Make predictions
    preds = model.predict(smiles=list(data.index))

    # Merge data and preds
    data_with_preds = pd.concat((data, preds), axis=1)

    # Save predictions
    if save_path is None:
        save_path = data_path

    save_path.parent.mkdir(parents=True, exist_ok=True)
    data_with_preds.to_csv(save_path, index_label=smiles_column)


def admet_predict_command_line() -> None:
    """Run admet_predict from the command line."""
    tapify(admet_predict)
