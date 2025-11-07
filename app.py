from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Simulación de base de datos (en memoria)
db = {
    'empleados': [],
    'vacantes': [],
    'contratos': [],
    'afiliaciones': [],
    'liquidaciones': [],
    'capacitaciones': [],
    'evaluaciones': []
}

# Rutas principales
@app.route('/')
def home():
    return render_template('index.html')

# Rutas para los diferentes módulos
@app.route('/modulo/seleccion')
def seleccion():
    return render_template('modulos/seleccion.html')

@app.route('/modulo/contratacion')
def contratacion():
    return render_template('modulos/contratacion.html')

@app.route('/modulo/seguridad-social')
def seguridad_social():
    return render_template('modulos/seguridad_social.html')

@app.route('/modulo/liquidaciones')
def liquidaciones():
    return render_template('modulos/liquidaciones.html')

@app.route('/modulo/capacitacion')
def capacitacion():
    return render_template('modulos/capacitacion.html')

@app.route('/modulo/evaluacion')
def evaluacion():
    return render_template('modulos/evaluacion.html')

# API Endpoints - Selección
@app.route('/api/vacancies', methods=['GET', 'POST'])
def handle_vacancies():
    if request.method == 'POST':
        vacancy = request.json
        vacancy['id'] = len(db['vacantes']) + 1
        vacancy['fecha_creacion'] = datetime.now().isoformat()
        db['vacantes'].append(vacancy)
        return jsonify({"success": True, "data": vacancy})
    return jsonify({"success": True, "data": db['vacantes']})

@app.route('/api/candidates', methods=['GET', 'POST'])
def handle_candidates():
    if request.method == 'POST':
        candidate = request.json
        candidate['id'] = len(db['empleados']) + 1
        db['empleados'].append(candidate)
        return jsonify({"success": True, "data": candidate})
    return jsonify({"success": True, "data": db['empleados']})

# API Endpoints - Contratación
@app.route('/api/contracts', methods=['GET', 'POST'])
def handle_contracts():
    if request.method == 'POST':
        contract = request.json
        contract['id'] = len(db['contratos']) + 1
        contract['fecha_creacion'] = datetime.now().isoformat()
        db['contratos'].append(contract)
        return jsonify({"success": True, "data": contract})
    return jsonify({"success": True, "data": db['contratos']})

# API Endpoints - Seguridad Social
@app.route('/api/affiliations', methods=['GET', 'POST'])
def handle_affiliations():
    if request.method == 'POST':
        affiliation = request.json
        affiliation['id'] = len(db['afiliaciones']) + 1
        affiliation['fecha_creacion'] = datetime.now().isoformat()
        db['afiliaciones'].append(affiliation)
        return jsonify({"success": True, "data": affiliation})
    return jsonify({"success": True, "data": db['afiliaciones']})

# API Endpoints - Liquidaciones
@app.route('/api/liquidations', methods=['GET', 'POST'])
def handle_liquidations():
    if request.method == 'POST':
        liquidation = request.json
        liquidation['id'] = len(db['liquidaciones']) + 1
        liquidation['fecha_calculo'] = datetime.now().isoformat()
        db['liquidaciones'].append(liquidation)
        return jsonify({"success": True, "data": liquidation})
    return jsonify({"success": True, "data": db['liquidaciones']})

# API Endpoints - Capacitación
@app.route('/api/training', methods=['GET', 'POST'])
def handle_training():
    if request.method == 'POST':
        training = request.json
        training['id'] = len(db['capacitaciones']) + 1
        training['fecha_creacion'] = datetime.now().isoformat()
        db['capacitaciones'].append(training)
        return jsonify({"success": True, "data": training})
    return jsonify({"success": True, "data": db['capacitaciones']})

# API Endpoints - Evaluación
@app.route('/api/evaluations', methods=['GET', 'POST'])
def handle_evaluations():
    if request.method == 'POST':
        evaluation = request.json
        evaluation['id'] = len(db['evaluaciones']) + 1
        evaluation['fecha_creacion'] = datetime.now().isoformat()
        db['evaluaciones'].append(evaluation)
        return jsonify({"success": True, "data": evaluation})
    return jsonify({"success": True, "data": db['evaluaciones']})

# Rutas de utilidad
@app.route('/api/employees', methods=['GET'])
def get_employees():
    return jsonify({"success": True, "data": db['empleados']})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    stats = {
        'total_empleados': len(db['empleados']),
        'vacantes_activas': len(db['vacantes']),
        'contratos_activos': len(db['contratos']),
        'capacitaciones_en_curso': len(db['capacitaciones']),
        'evaluaciones_pendientes': len(db['evaluaciones'])
    }
    return jsonify({"success": True, "data": stats})

if __name__ == '__main__':
    app.run(debug=True)