# Projects

This repository contains two independent projects.

## Parkinsons ABC Feature Selection

The Python project compares Logistic Regression, Random Forest, and SVM classifiers with and without Artificial Bee Colony (ABC) feature selection on the Parkinsons dataset.

Install its dependencies with:

```powershell
python -m pip install -r requirements.txt
```

Run the Python experiments from the repository root with `python lrwithabc.py`, `python rfwithabc.py`, or `python svmwithabc.py`.

## Quiz Management System

A console-based C++ quiz management system with separate student and admin workflows.

## Features

- Student registration and login
- Admin login
- Add, view, and delete quiz questions
- Start a quiz and record scores
- View previous results
- Input validation for menu choices

## Build and Run

Compile with a C++17 compiler from this directory:

```powershell
g++ -std=c++17 main.cpp -o main.exe
.\main.exe
```

The program reads and writes these local data files:

- `admin.txt` - admin credentials
- `users.txt` - registered users
- `questions.txt` - quiz questions and answers
- `results.txt` - quiz scores

Credential and result files are intentionally not included in the public repository because they contain private data. Create them locally before running the program.

## Data File Formats

`admin.txt` and `users.txt` use one username/password pair per line. `results.txt` stores one result per line. `questions.txt` stores each question followed by four options and the numeric answer position.
