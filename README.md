# 🚀 Computer Arithmetic Calculator

A learning toolkit showing how key CPU arithmetic algorithms work in practice:

- Booth Multiplication
- Modified Booth Multiplication
- Restoring Division
- Non-Restoring Division

## ✨ Features

- **Booth's Multiplication**: Standard algorithm for signed binary multiplication
- **Modified Booth's Multiplication**: Optimized version using bit-pair recoding
- **Restoring Division**: Classic division algorithm with remainder restoration
- **Non-Restoring Division**: Efficient division without restoration steps

## Installation

1. Clone or download the repository
2. Install Python 3.11 or later
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Navigate to the project directory
2. Run the Flask server:
   ```bash
   python backend/app.py
   ```
3. Open your browser and go to `http://localhost:5000`

## Usage

1. Select an arithmetic operation from the main page
2. Enter binary numbers in the input fields
3. Click "Calculate" to see the step-by-step algorithm execution
4. View the intermediate steps and final result

## How it works

- The front-end captures two binary inputs and the user-selected operation.
- A JSON POST request is sent to `/calculate` on the Flask backend.
- The backend runs the selected algorithm and generates a list of cycle states (A, Q, carry bits, operations, etc.)
- The response includes `result` or `quotient`/`remainder` plus the trace steps.
- The front-end renders the output as visually structured step cards for easy learning.

## Development notes

- ✅ Ensure binary inputs have only `0` and `1` characters.
- ✅ Use same bit widths for Booth and Modified Booth inputs for correct behavior.
- ✅ If you see unexpected results, refresh the page and re-enter values.

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Modern dark theme with responsive design

## Educational Purpose

This application is designed for educational purposes to help students understand the inner workings of computer arithmetic algorithms used in digital systems and processors.