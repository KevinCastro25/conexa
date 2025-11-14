from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

# Importar modelos y base de datos
from models import db, Empleado, Vacante, Candidato, Entrevista, Contrato, Afiliacion, Liquidacion, Capacitacion, ParticipanteCapacitacion, Evaluacion

app = Flask(__name__)
CORS(app)

# ==================== CONFIGURACIÓN DE BASE DE DATOS ====================
# Configuración de SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'conexa.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui-cambiar-en-produccion'

# Inicializar base de datos
db.init_app(app)

# ==================== INICIALIZACIÓN DE BASE DE DATOS ====================
def init_database():
    """
    Inicializa la base de datos limpiando datos anteriores y creando datos de ejemplo
    """
    with app.app_context():
        # Eliminar todas las tablas y recrearlas (limpia datos anteriores)
        db.drop_all()
        db.create_all()
        
        print("📊 Inicializando base de datos con datos de ejemplo...")
        
        from datetime import date, time, timedelta
        
        # ========== EMPLEADOS ==========
        empleados_ejemplo = [
            Empleado(
                nombre="María Fernanda Torres",
                email="maria.torres@conexa.com",
                telefono="+57 300 111 2222",
                documento="1001234567",
                cargo="Gerente de Recursos Humanos",
                departamento="recursos_humanos",
                salario=7000000,
                fecha_ingreso=date(2020, 1, 15),
                estado="activo"
            ),
            Empleado(
                nombre="Juan Carlos Méndez",
                email="juan.mendez@conexa.com",
                telefono="+57 301 222 3333",
                documento="1002345678",
                cargo="Desarrollador Full Stack Senior",
                departamento="tecnologia",
                salario=6500000,
                fecha_ingreso=date(2021, 3, 10),
                estado="activo"
            ),
            Empleado(
                nombre="Laura Sofía Ramírez",
                email="laura.ramirez@conexa.com",
                telefono="+57 302 333 4444",
                documento="1003456789",
                cargo="Especialista en Marketing Digital",
                departamento="marketing",
                salario=4500000,
                fecha_ingreso=date(2022, 6, 1),
                estado="activo"
            ),
            Empleado(
                nombre="Diego Alejandro Castro",
                email="diego.castro@conexa.com",
                telefono="+57 303 444 5555",
                documento="1004567890",
                cargo="Contador Senior",
                departamento="contabilidad",
                salario=5500000,
                fecha_ingreso=date(2021, 9, 15),
                estado="activo"
            ),
            Empleado(
                nombre="Valentina Gómez Silva",
                email="valentina.gomez@conexa.com",
                telefono="+57 304 555 6666",
                documento="1005678901",
                cargo="Diseñadora UX/UI",
                departamento="tecnologia",
                salario=5000000,
                fecha_ingreso=date(2022, 2, 20),
                estado="activo"
            ),
            Empleado(
                nombre="Andrés Felipe Moreno",
                email="andres.moreno@conexa.com",
                telefono="+57 305 666 7777",
                documento="1006789012",
                cargo="Analista de Datos",
                departamento="tecnologia",
                salario=4800000,
                fecha_ingreso=date(2023, 1, 10),
                estado="activo"
            )
        ]
        
        for emp in empleados_ejemplo:
            db.session.add(emp)
        db.session.flush()  # Para obtener los IDs
        
        # ========== VACANTES ==========
        vacantes_ejemplo = [
            Vacante(
                titulo="Desarrollador Backend Python",
                departamento="tecnologia",
                nivel="senior",
                cantidad=2,
                descripcion="Buscamos desarrollador Backend con experiencia en Python, Flask, Django y bases de datos. Experiencia mínima 4 años.",
                salario=6000000,
                estado="activa"
            ),
            Vacante(
                titulo="Especialista en Redes Sociales",
                departamento="marketing",
                nivel="middle",
                cantidad=1,
                descripcion="Experiencia en gestión de redes sociales, creación de contenido y análisis de métricas. Conocimiento en herramientas de diseño.",
                salario=3500000,
                estado="activa"
            ),
            Vacante(
                titulo="Analista Contable Junior",
                departamento="contabilidad",
                nivel="junior",
                cantidad=1,
                descripcion="Recién graduado en Contaduría Pública. Manejo de software contable y conocimientos en tributación.",
                salario=2800000,
                estado="activa"
            ),
            Vacante(
                titulo="Desarrollador Frontend React",
                departamento="tecnologia",
                nivel="middle",
                cantidad=2,
                descripcion="Desarrollador con experiencia en React, TypeScript, y diseño responsivo. Mínimo 2 años de experiencia.",
                salario=5000000,
                estado="activa"
            )
        ]
        
        for vac in vacantes_ejemplo:
            db.session.add(vac)
        db.session.flush()
        
        # ========== CANDIDATOS ==========
        candidatos_ejemplo = [
            Candidato(
                vacante_id=1,  # Desarrollador Backend Python
                nombre="Ana García López",
                email="ana.garcia@email.com",
                telefono="+57 300 123 4567",
                documento="1007890123",
                estado="en_proceso",
                notas="Excelente perfil técnico, 5 años de experiencia"
            ),
            Candidato(
                vacante_id=1,  # Desarrollador Backend Python
                nombre="Carlos Rodríguez Pérez",
                email="carlos.rodriguez@email.com",
                telefono="+57 301 234 5678",
                documento="1008901234",
                estado="entrevista",
                notas="Muy buen portafolio, experiencia en Flask"
            ),
            Candidato(
                vacante_id=2,  # Especialista en Redes Sociales
                nombre="Camila Herrera Díaz",
                email="camila.herrera@email.com",
                telefono="+57 302 345 6789",
                documento="1009012345",
                estado="nuevo",
                notas="Certificaciones en marketing digital"
            ),
            Candidato(
                vacante_id=3,  # Analista Contable Junior
                nombre="Daniel Ospina Ruiz",
                email="daniel.ospina@email.com",
                telefono="+57 303 456 7890",
                documento="1010123456",
                estado="nuevo",
                notas="Recién graduado con honores"
            ),
            Candidato(
                vacante_id=4,  # Desarrollador Frontend React
                nombre="Isabella Martínez Cruz",
                email="isabella.martinez@email.com",
                telefono="+57 304 567 8901",
                documento="1011234567",
                estado="en_proceso",
                notas="3 años de experiencia en React y Next.js"
            ),
            Candidato(
                vacante_id=4,  # Desarrollador Frontend React
                nombre="Santiago Vargas León",
                email="santiago.vargas@email.com",
                telefono="+57 305 678 9012",
                documento="1012345678",
                estado="entrevista",
                notas="Portafolio muy completo, conoce TypeScript"
            )
        ]
        
        for cand in candidatos_ejemplo:
            db.session.add(cand)
        db.session.flush()
        
        # ========== ENTREVISTAS ==========
        hoy = date.today()
        entrevistas_ejemplo = [
            Entrevista(
                candidato_id=1,  # Ana García
                fecha=hoy + timedelta(days=2),
                hora=time(10, 0),
                tipo="tecnica",
                entrevistador="Juan Carlos Méndez",
                estado="programada"
            ),
            Entrevista(
                candidato_id=2,  # Carlos Rodríguez
                fecha=hoy + timedelta(days=3),
                hora=time(14, 0),
                tipo="presencial",
                entrevistador="María Fernanda Torres",
                estado="programada"
            ),
            Entrevista(
                candidato_id=6,  # Santiago Vargas
                fecha=hoy + timedelta(days=1),
                hora=time(11, 30),
                tipo="virtual",
                entrevistador="Valentina Gómez Silva",
                estado="programada"
            )
        ]
        
        for ent in entrevistas_ejemplo:
            db.session.add(ent)
        db.session.flush()
        
        # ========== CONTRATOS ==========
        contratos_ejemplo = [
            Contrato(
                empleado_id=1,  # María Fernanda Torres
                tipo="indefinido",
                cargo="Gerente de Recursos Humanos",
                salario=7000000,
                fecha_inicio=date(2020, 1, 15),
                estado="activo"
            ),
            Contrato(
                empleado_id=2,  # Juan Carlos Méndez
                tipo="indefinido",
                cargo="Desarrollador Full Stack Senior",
                salario=6500000,
                fecha_inicio=date(2021, 3, 10),
                estado="activo"
            ),
            Contrato(
                empleado_id=3,  # Laura Sofía Ramírez
                tipo="indefinido",
                cargo="Especialista en Marketing Digital",
                salario=4500000,
                fecha_inicio=date(2022, 6, 1),
                estado="activo"
            ),
            Contrato(
                empleado_id=4,  # Diego Alejandro Castro
                tipo="indefinido",
                cargo="Contador Senior",
                salario=5500000,
                fecha_inicio=date(2021, 9, 15),
                estado="activo"
            ),
            Contrato(
                empleado_id=5,  # Valentina Gómez Silva
                tipo="indefinido",
                cargo="Diseñadora UX/UI",
                salario=5000000,
                fecha_inicio=date(2022, 2, 20),
                estado="activo"
            ),
            Contrato(
                empleado_id=6,  # Andrés Felipe Moreno
                tipo="fijo",
                cargo="Analista de Datos",
                salario=4800000,
                fecha_inicio=date(2023, 1, 10),
                fecha_fin=date(2024, 1, 10),
                estado="activo"
            )
        ]
        
        for cont in contratos_ejemplo:
            db.session.add(cont)
        db.session.flush()
        
        # ========== CAPACITACIONES ==========
        capacitaciones_ejemplo = [
            Capacitacion(
                nombre="Python Avanzado y Machine Learning",
                tipo="tecnica",
                descripcion="Curso intensivo de Python avanzado con enfoque en ciencia de datos y ML",
                fecha_inicio=date(2024, 11, 20),
                duracion_horas=40,
                instructor="Dr. Roberto Sánchez",
                costo=5000000,
                estado="programada"
            ),
            Capacitacion(
                nombre="Liderazgo y Gestión de Equipos",
                tipo="habilidades",
                descripcion="Taller de habilidades blandas para líderes de equipo",
                fecha_inicio=date(2024, 11, 15),
                duracion_horas=16,
                instructor="Psic. Ana María Gómez",
                costo=2500000,
                estado="en_curso"
            ),
            Capacitacion(
                nombre="Seguridad Informática y Ciberseguridad",
                tipo="seguridad",
                descripcion="Capacitación en mejores prácticas de seguridad informática",
                fecha_inicio=date(2024, 10, 1),
                duracion_horas=32,
                instructor="Ing. Carlos Mendoza",
                costo=4000000,
                estado="completada"
            )
        ]
        
        for cap in capacitaciones_ejemplo:
            db.session.add(cap)
        db.session.flush()
        
        # ========== PARTICIPANTES EN CAPACITACIONES ==========
        participantes_ejemplo = [
            ParticipanteCapacitacion(capacitacion_id=1, empleado_id=2, asistencia=True, calificacion=0),  # Juan - Python
            ParticipanteCapacitacion(capacitacion_id=1, empleado_id=6, asistencia=True, calificacion=0),  # Andrés - Python
            ParticipanteCapacitacion(capacitacion_id=2, empleado_id=1, asistencia=True, calificacion=0),  # María - Liderazgo
            ParticipanteCapacitacion(capacitacion_id=3, empleado_id=2, asistencia=True, calificacion=95),  # Juan - Seguridad
            ParticipanteCapacitacion(capacitacion_id=3, empleado_id=5, asistencia=True, calificacion=88)   # Valentina - Seguridad
        ]
        
        for part in participantes_ejemplo:
            db.session.add(part)
        db.session.flush()
        
        # ========== EVALUACIONES DE DESEMPEÑO ==========
        evaluaciones_ejemplo = [
            Evaluacion(
                empleado_id=2,  # Juan Carlos
                evaluador_id=1,  # María Fernanda
                tipo="anual",
                periodo="2024",
                calificacion=90,
                comentarios="Excelente desempeño técnico. Líder natural en el equipo.",
                plan_desarrollo="Continuar con capacitaciones en nuevas tecnologías",
                estado="completada",
                fecha_completada=date(2024, 10, 15)
            ),
            Evaluacion(
                empleado_id=3,  # Laura Sofía
                evaluador_id=1,  # María Fernanda
                tipo="semestral",
                periodo="2024-S2",
                calificacion=88,
                comentarios="Creatividad excepcional en campañas de marketing",
                plan_desarrollo="Profundizar en análisis de datos y métricas",
                estado="completada",
                fecha_completada=date(2024, 10, 20)
            ),
            Evaluacion(
                empleado_id=5,  # Valentina
                evaluador_id=1,  # María Fernanda
                tipo="semestral",
                periodo="2024-S2",
                calificacion=0,
                comentarios="",
                plan_desarrollo="",
                estado="pendiente"
            )
        ]
        
        for ev in evaluaciones_ejemplo:
            db.session.add(ev)
        
        # Guardar todos los cambios
        db.session.commit()
        
        print("✅ Base de datos inicializada correctamente!")
        print(f"   - {len(empleados_ejemplo)} empleados creados")
        print(f"   - {len(vacantes_ejemplo)} vacantes creadas")
        print(f"   - {len(candidatos_ejemplo)} candidatos creados")
        print(f"   - {len(entrevistas_ejemplo)} entrevistas programadas")
        print(f"   - {len(contratos_ejemplo)} contratos creados")
        print(f"   - {len(capacitaciones_ejemplo)} capacitaciones creadas")
        print(f"   - {len(evaluaciones_ejemplo)} evaluaciones creadas")

# Inicializar la base de datos al arranque
init_database()

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
        try:
            data = request.json
            nueva_vacante = Vacante(
                titulo=data.get('titulo'),
                departamento=data.get('departamento'),
                nivel=data.get('nivel'),
                cantidad=data.get('cantidad', 1),
                descripcion=data.get('descripcion'),
                salario=data.get('salario'),
                estado='activa'
            )
            db.session.add(nueva_vacante)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Vacante creada exitosamente",
                "data": nueva_vacante.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al crear vacante: {str(e)}"
            }), 400
    
    # GET - Obtener todas las vacantes
    vacantes = Vacante.query.filter_by(estado='activa').all()
    return jsonify({
        "success": True,
        "data": [v.to_dict() for v in vacantes]
    })

@app.route('/api/vacancies/<int:vacancy_id>', methods=['PUT', 'DELETE'])
def update_vacancy(vacancy_id):
    vacancy = Vacante.query.get(vacancy_id)
    
    if not vacancy:
        return jsonify({
            "success": False,
            "message": "Vacante no encontrada"
        }), 404
    
    if request.method == 'PUT':
        try:
            data = request.json
            
            # Actualizar campos
            if 'titulo' in data:
                vacancy.titulo = data['titulo']
            if 'departamento' in data:
                vacancy.departamento = data['departamento']
            if 'nivel' in data:
                vacancy.nivel = data['nivel']
            if 'cantidad' in data:
                vacancy.cantidad = data['cantidad']
            if 'descripcion' in data:
                vacancy.descripcion = data['descripcion']
            if 'salario' in data:
                vacancy.salario = data['salario']
            if 'estado' in data:
                vacancy.estado = data['estado']
            
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Vacante actualizada exitosamente",
                "data": vacancy.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al actualizar vacante: {str(e)}"
            }), 400
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(vacancy)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Vacante eliminada exitosamente"
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al eliminar vacante: {str(e)}"
            }), 400

@app.route('/api/candidates', methods=['GET', 'POST'])
def handle_candidates():
    if request.method == 'POST':
        try:
            data = request.json
            nuevo_candidato = Candidato(
                vacante_id=data.get('vacante_id'),
                nombre=data.get('nombre'),
                email=data.get('email'),
                telefono=data.get('telefono'),
                documento=data.get('documento'),
                estado='nuevo'
            )
            db.session.add(nuevo_candidato)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Candidato registrado exitosamente",
                "data": nuevo_candidato.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al registrar candidato: {str(e)}"
            }), 400
    
    # GET - Obtener todos los candidatos (excluyendo contratados)
    candidatos = Candidato.query.filter(Candidato.estado != 'contratado').all()
    return jsonify({
        "success": True,
        "data": [c.to_dict() for c in candidatos]
    })

@app.route('/api/candidates/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    candidate = Candidato.query.get(candidate_id)
    
    if not candidate:
        return jsonify({
            "success": False,
            "message": "Candidato no encontrado"
        }), 404
    
    try:
        data = request.json
        
        # Actualizar estado
        if 'estado' in data:
            candidate.estado = data['estado']
        
        # Actualizar otras propiedades si se envían
        if 'notas' in data:
            candidate.notas = data['notas']
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Candidato actualizado exitosamente",
            "data": candidate.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error al actualizar candidato: {str(e)}"
        }), 400

@app.route('/api/interviews', methods=['GET', 'POST'])
def handle_interviews():
    if request.method == 'POST':
        try:
            data = request.json
            from datetime import datetime as dt, time
            
            # Procesar la hora
            hora_str = data.get('hora')
            if hora_str:
                if ':' in hora_str:
                    h, m = hora_str.split(':')
                    hora_obj = time(int(h), int(m))
                else:
                    hora_obj = None
            else:
                hora_obj = None
            
            nueva_entrevista = Entrevista(
                candidato_id=data.get('candidato_id'),
                fecha=dt.strptime(data.get('fecha'), '%Y-%m-%d').date() if data.get('fecha') else None,
                hora=hora_obj,
                tipo=data.get('tipo'),
                entrevistador=data.get('entrevistador'),
                estado=data.get('estado', 'programada'),
                calificacion=data.get('calificacion'),
                comentarios=data.get('comentarios')
            )
            db.session.add(nueva_entrevista)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Entrevista agendada exitosamente",
                "data": nueva_entrevista.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al agendar entrevista: {str(e)}"
            }), 400
    
    # GET - Obtener todas las entrevistas
    entrevistas = Entrevista.query.all()
    return jsonify({
        "success": True,
        "data": [e.to_dict() for e in entrevistas]
    })

# API Endpoints - Contratación
@app.route('/api/contracts', methods=['GET', 'POST'])
def handle_contracts():
    if request.method == 'POST':
        try:
            data = request.json
            from datetime import datetime as dt
            
            nuevo_contrato = Contrato(
                empleado_id=data.get('empleado_id'),
                tipo=data.get('tipo'),
                cargo=data.get('cargo'),
                salario=float(data.get('salario')),
                fecha_inicio=dt.strptime(data.get('fecha_inicio'), '%Y-%m-%d').date(),
                estado=data.get('estado', 'activo')
            )
            
            if data.get('fecha_fin'):
                nuevo_contrato.fecha_fin = dt.strptime(data.get('fecha_fin'), '%Y-%m-%d').date()
            
            db.session.add(nuevo_contrato)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Contrato creado exitosamente",
                "data": nuevo_contrato.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al crear contrato: {str(e)}"
            }), 400
    
    # GET - Obtener todos los contratos
    contratos = Contrato.query.all()
    return jsonify({
        "success": True,
        "data": [c.to_dict() for c in contratos]
    })

# API Endpoints - Seguridad Social
@app.route('/api/affiliations', methods=['GET', 'POST'])
def handle_affiliations():
    if request.method == 'POST':
        try:
            data = request.json
            from datetime import datetime as dt
            
            # Convertir fecha_afiliacion si viene como string
            fecha_afiliacion = data.get('fecha_afiliacion')
            if fecha_afiliacion and isinstance(fecha_afiliacion, str):
                fecha_afiliacion = dt.strptime(fecha_afiliacion, '%Y-%m-%d').date()
            
            nueva_afiliacion = Afiliacion(
                empleado_id=data.get('empleado_id'),
                tipo=data.get('tipo'),
                entidad=data.get('entidad'),
                numero_afiliacion=data.get('numero_afiliacion'),
                fecha_afiliacion=fecha_afiliacion,
                estado=data.get('estado', 'activo')
            )
            db.session.add(nueva_afiliacion)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Afiliación creada exitosamente",
                "data": nueva_afiliacion.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al crear afiliación: {str(e)}"
            }), 400
    
    # GET - Obtener todas las afiliaciones
    afiliaciones = Afiliacion.query.all()
    return jsonify({
        "success": True,
        "data": [a.to_dict() for a in afiliaciones]
    })

# API Endpoints - Liquidaciones
@app.route('/api/liquidations', methods=['GET', 'POST'])
def handle_liquidations():
    if request.method == 'POST':
        try:
            data = request.json
            from datetime import datetime as dt
            
            # Manejar diferentes formatos de entrada
            periodo = data.get('periodo')  # Formato: "2025-11"
            if periodo and '-' in periodo:
                year, month = periodo.split('-')
                # Primer día del mes
                periodo_inicio = dt(int(year), int(month), 1).date()
                # Último día del mes
                import calendar
                last_day = calendar.monthrange(int(year), int(month))[1]
                periodo_fin = dt(int(year), int(month), last_day).date()
            else:
                periodo_inicio = dt.strptime(data.get('periodo_inicio'), '%Y-%m-%d').date() if data.get('periodo_inicio') else None
                periodo_fin = dt.strptime(data.get('periodo_fin'), '%Y-%m-%d').date() if data.get('periodo_fin') else None
            
            # Obtener salario base
            salario_base = float(data.get('salario_base', 0))
            
            # Calcular devengado (salario base + bonificaciones)
            horas_extra = int(data.get('horas_extra', 0))
            bonificaciones = float(data.get('bonificaciones', 0))
            
            # Cálculo simple de devengado
            devengado = salario_base + bonificaciones + (horas_extra * (salario_base / 240))  # 240 horas mes
            
            # Calcular deducciones (aproximado: 8% salud + 4% pensión)
            deducciones_salud = salario_base * 0.04  # 4% empleado
            deducciones_pension = salario_base * 0.04  # 4% empleado
            deducciones_otras = float(data.get('deducciones', 0))
            deducciones_total = deducciones_salud + deducciones_pension + deducciones_otras
            
            # Neto a pagar
            neto = devengado - deducciones_total
            
            nueva_liquidacion = Liquidacion(
                empleado_id=data.get('empleado_id'),
                tipo=data.get('tipo', 'nomina'),
                periodo_inicio=periodo_inicio,
                periodo_fin=periodo_fin,
                salario_base=salario_base,
                devengado=round(devengado, 2),
                deducciones=round(deducciones_total, 2),
                neto=round(neto, 2),
                estado=data.get('estado', 'pendiente'),
                fecha_pago=dt.strptime(data.get('fecha_pago'), '%Y-%m-%d').date() if data.get('fecha_pago') else None
            )
            db.session.add(nueva_liquidacion)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Liquidación calculada exitosamente",
                "data": nueva_liquidacion.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al calcular liquidación: {str(e)}"
            }), 400
    
    # GET - Obtener todas las liquidaciones
    liquidaciones = Liquidacion.query.all()
    return jsonify({
        "success": True,
        "data": [l.to_dict() for l in liquidaciones]
    })

# API Endpoints - Capacitación
@app.route('/api/training', methods=['GET', 'POST'])
def handle_training():
    if request.method == 'POST':
        try:
            data = request.json
            from datetime import datetime as dt
            
            # Aceptar tanto 'titulo' como 'nombre'
            titulo = data.get('titulo') or data.get('nombre')
            
            nueva_capacitacion = Capacitacion(
                nombre=titulo,
                tipo=data.get('tipo'),
                instructor=data.get('instructor'),
                fecha_inicio=dt.strptime(data.get('fecha_inicio'), '%Y-%m-%d').date() if data.get('fecha_inicio') else None,
                duracion_horas=data.get('duracion_horas'),
                costo=float(data.get('costo', 0)) if data.get('costo') else None,
                descripcion=data.get('descripcion'),
                estado=data.get('estado', 'programada')
            )
            db.session.add(nueva_capacitacion)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Capacitación creada exitosamente",
                "data": nueva_capacitacion.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al crear capacitación: {str(e)}"
            }), 400
    
    # GET - Obtener todas las capacitaciones
    capacitaciones = Capacitacion.query.all()
    return jsonify({
        "success": True,
        "data": [c.to_dict() for c in capacitaciones]
    })

# API Endpoints - Evaluación
@app.route('/api/evaluations', methods=['GET', 'POST'])
def handle_evaluations():
    if request.method == 'POST':
        try:
            data = request.json
            nueva_evaluacion = Evaluacion(
                empleado_id=data.get('empleado_id'),
                evaluador_id=data.get('evaluador_id'),
                tipo=data.get('tipo'),
                periodo=data.get('periodo'),
                calificacion=float(data.get('calificacion', 0)) if data.get('calificacion') else None,
                estado='pendiente',
                comentarios=data.get('comentarios')
            )
            db.session.add(nueva_evaluacion)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Evaluación creada exitosamente",
                "data": nueva_evaluacion.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al crear evaluación: {str(e)}"
            }), 400
    
    # GET - Obtener todas las evaluaciones
    evaluaciones = Evaluacion.query.all()
    return jsonify({
        "success": True,
        "data": [e.to_dict() for e in evaluaciones]
    })

# Rutas de utilidad
@app.route('/api/employees', methods=['GET', 'POST'])
def handle_employees():
    if request.method == 'POST':
        try:
            data = request.json
            
            # Crear nuevo empleado
            nuevo_empleado = Empleado(
                nombre=data.get('nombre'),
                documento=data.get('identificacion'),
                email=data.get('email'),
                telefono=data.get('telefono'),
                cargo=data.get('cargo'),
                departamento=data.get('departamento'),
                salario=data.get('salario'),
                fecha_ingreso=datetime.strptime(data.get('fecha_ingreso'), '%Y-%m-%d') if data.get('fecha_ingreso') else datetime.utcnow(),
                estado='activo'
            )
            
            db.session.add(nuevo_empleado)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Empleado creado exitosamente",
                "data": nuevo_empleado.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al crear empleado: {str(e)}"
            }), 400
    
    # GET - Obtener todos los empleados activos
    empleados = Empleado.query.filter_by(estado='activo').all()
    return jsonify({
        "success": True,
        "data": [e.to_dict() for e in empleados]
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    stats = {
        'total_empleados': Empleado.query.filter_by(estado='activo').count(),
        'vacantes_activas': Vacante.query.filter_by(estado='activa').count(),
        'contratos_activos': Contrato.query.filter_by(estado='activo').count(),
        'capacitaciones_en_curso': Capacitacion.query.filter_by(estado='en_curso').count(),
        'evaluaciones_pendientes': Evaluacion.query.filter_by(estado='pendiente').count()
    }
    return jsonify({"success": True, "data": stats})

if __name__ == '__main__':
    app.run(debug=True)