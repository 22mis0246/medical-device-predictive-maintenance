# Python Import Resolution & Running Guide

If you see red squiggles or "Import could not be resolved" errors in VS Code, follow these steps:

## 1. Select the Correct Python Interpreter (Fixes Red Squiggles)
VS Code needs to use the virtual environment (`venv`) where your dependencies are installed, not the global Anaconda environment.

1.  Press `Ctrl + Shift + P` in VS Code.
2.  Type **"Python: Select Interpreter"** and select it.
3.  Choose the path: `.\venv\Scripts\python.exe`.
4.  **Important:** Restart VS Code if the errors don't disappear immediately.

## 2. Updated Project Settings
I've updated the following files to help the IDE find your code:
- `.vscode/settings.json`: Points to `.\venv` and the project root.
- `pyrightconfig.json`: Explicitly guides the static analyzer through your project folders.

## 3. Difference Between "Linter Errors" and "Actual Errors"

> [!NOTE]
> **Static Analysis (Linter) Errors:** These are the red squiggles you see in the editor. They are *guesses* by VS Code. Sometimes they are wrong, especially with libraries like `python-jose` that don't provide "Type Stubs" (special files that tell editors what the code looks like).
>
> **Runtime Errors:** These are the errors you see in the terminal when you run the app. If the app runs in the terminal, your code is working!

## 4. How to Run the App

### Option A: The "One-Click" Launcher (Recommended)
Double-click or run from the terminal:
```powershell
.\setup_and_run.bat
```

### Option B: Running Individually in VS Code Terminal
Open a terminal in VS Code and run:

1.  **Backend API:**
    ```powershell
    uvicorn backend.main:app --reload
    ```
2.  **Dashboard:**
    ```powershell
    streamlit run dashboard/app.py
    ```
3.  **Device Simulator (to see live data):**
    ```powershell
    python simulator/device_simulator.py
    ```
