from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1 booth multiplication
def booth_steps(m, q):
    steps = []
    n = len(m)

    M = int(m, 2)
    Q = int(q, 2)
    A = 0
    Q_1 = 0

    for i in range(n):
        step = {}

        step["cycle"] = i + 1
        step["A"] = format(A & ((1 << n) - 1), f"0{n}b")
        step["Q"] = format(Q & ((1 << n) - 1), f"0{n}b")
        step["Q_1"] = Q_1

        Q0 = Q & 1

        if Q0 == 0 and Q_1 == 1:
            A = A + M
            step["operation"] = "A = A + M"
        elif Q0 == 1 and Q_1 == 0:
            A = A - M
            step["operation"] = "A = A - M"
        else:
            step["operation"] = "No operation"

        step["before_shift_A"] = format(A & ((1 << n) - 1), f"0{n}b")

        combined = (A << (n + 1)) | (Q << 1) | Q_1
        combined >>= 1

        Q_1 = combined & 1
        Q = (combined >> 1) & ((1 << n) - 1)
        A = (combined >> (n + 1)) & ((1 << n) - 1)
        step["after_shift_A"] = format(A, f"0{n}b")
        step["after_shift_Q"] = format(Q, f"0{n}b")
        step["after_shift_Q_1"] = Q_1

        steps.append(step)

    product = (A << n) | Q
    return {
        "steps": steps,
        "result": format(product, f"0{2*n}b")
    }

# 2 modified booth
def modified_booth_steps(m, q):
    steps = []
    q = "0" + q   
    pairs = []

    for i in range(0, len(q) - 1, 2):
        block = q[i:i+3]
        pairs.append(block)

    for i, block in enumerate(pairs):
        if block in ["000", "111"]:
            op = "0 × M"
        elif block in ["001", "010"]:
            op = "+M"
        elif block == "011":
            op = "+2M"
        elif block == "100":
            op = "-2M"
        elif block in ["101", "110"]:
            op = "-M"

        steps.append({
            "pair": i + 1,
            "bits": block,
            "operation": op,
            "shift_amount": 2 * i
        })

    return {
        "steps": steps,
        "result": "Partial products shown above"
    }

# 3 restoring
def restoring_division_steps(dividend, divisor):
    A = 0
    Q = int(dividend, 2)
    M = int(divisor, 2)
    n = len(dividend)

    steps = []

    for i in range(n):
        step = {"cycle": i + 1}

        A = (A << 1) | ((Q >> (n - 1)) & 1)
        Q = (Q << 1) & ((1 << n) - 1)

        A2 = A - M

        if A2 < 0:
            step["operation"] = "A - M is negative → restore, Q0 = 0"
            Q |= 0
        else:
            step["operation"] = "A - M is positive → keep, Q0 = 1"
            A = A2
            Q |= 1

        step["A"] = format(A & ((1 << n) - 1), f"0{n}b")
        step["Q"] = format(Q, f"0{n}b")
        steps.append(step)

    return {
        "steps": steps,
        "quotient": format(Q, f"0{n}b"),
        "remainder": format(A, f"0{n}b")
    }

# 4 non restoring
def non_restoring_division_steps(dividend, divisor):
    A = 0
    Q = int(dividend, 2)
    M = int(divisor, 2)
    n = len(dividend)

    steps = []

    for i in range(n):
        step = {"cycle": i + 1}

        A = (A << 1) | ((Q >> (n - 1)) & 1)
        Q = (Q << 1) & ((1 << n) - 1)

        if A >= 0:
            A = A - M
            step["operation"] = "A>=0 → A=A-M, Q0=1"
            Q |= 1
        else:
            A = A + M
            step["operation"] = "A<0 → A=A+M, Q0=0"
            Q |= 0

        step["A"] = format(A & ((1 << n) - 1), f"0{n}b")
        step["Q"] = format(Q, f"0{n}b")
        steps.append(step)

    if A < 0:
        A = A + M

    return {
        "steps": steps,
        "quotient": format(Q, f"0{n}b"),
        "remainder": format(A & ((1 << n) - 1), f"0{n}b")
    }


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    op = data["operation"]

    if op == "booth":
        return jsonify(booth_steps(data["m"], data["q"]))

    elif op == "modified_booth":
        return jsonify(modified_booth_steps(data["m"], data["q"]))

    elif op == "restoring":
        return jsonify(restoring_division_steps(data["dividend"], data["divisor"]))

    elif op == "non_restoring":
        return jsonify(non_restoring_division_steps(data["dividend"], data["divisor"]))

    return jsonify({"error": "Invalid operation"})

