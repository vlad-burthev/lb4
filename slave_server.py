from flask import Flask, request, jsonify
import numpy as np
from numpy.linalg import eigvals

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_l2():
    matrix = request.json.get("matrix")
    if matrix is None:
        return jsonify({"error": "Matrix is missing"}), 400

    np_matrix = np.array(matrix)
    eigenvalues = eigvals(np_matrix)
    max_eigenvalue = max(eigenvalues.real)
    return jsonify({"L2": max_eigenvalue})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
