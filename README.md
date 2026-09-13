# Parkinsons ABC Feature Selection

This project compares Logistic Regression, Random Forest, and SVM classifiers with and without Artificial Bee Colony (ABC) feature selection on the Parkinsons dataset.

## Files

- `lrwithabc.py` - Logistic Regression with ABC feature selection
- `rfwithabc.py` - Random Forest with ABC feature selection
- `svmwithabc.py` - SVM with ABC feature selection
- `rfclaud.py` and `svmclaud.py` - parallelized experiment variants
- `parkinsons.data` - dataset used by the scripts
- `parkinsons.names` - dataset description

The duplicate `lrwithabc (1).py` file is retained as provided.

## Setup

Use Python 3.10 or newer, then install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run

Run a script from this directory so it can find `parkinsons.data`:

```powershell
python lrwithabc.py
python rfwithabc.py
python svmwithabc.py
```

Each script prints accuracy results and displays a comparison plot. The experiments can take time because ABC evaluates many candidate feature subsets.
