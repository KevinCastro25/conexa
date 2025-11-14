"""
Modelos de Base de Datos para Conexa RRHH
SQLAlchemy ORM Models
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ==================== MODELO: EMPLEADOS ====================
class Empleado(db.Model):
    __tablename__ = 'empleados'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    documento = db.Column(db.String(20), unique=True)
    fecha_nacimiento = db.Column(db.Date)
    direccion = db.Column(db.String(200))
    cargo = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    fecha_ingreso = db.Column(db.Date)
    salario = db.Column(db.Float)
    estado = db.Column(db.String(20), default='activo')  # activo, inactivo, retirado
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    contratos = db.relationship('Contrato', backref='empleado', lazy=True)
    afiliaciones = db.relationship('Afiliacion', backref='empleado', lazy=True)
    liquidaciones = db.relationship('Liquidacion', backref='empleado', lazy=True)
    evaluaciones = db.relationship('Evaluacion', foreign_keys='Evaluacion.empleado_id', backref='empleado', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'documento': self.documento,
            'cargo': self.cargo,
            'departamento': self.departamento,
            'salario': self.salario,
            'estado': self.estado,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }

# ==================== MODELO: VACANTES ====================
class Vacante(db.Model):
    __tablename__ = 'vacantes'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    departamento = db.Column(db.String(100), nullable=False)
    nivel = db.Column(db.String(50))  # junior, middle, senior, lead, manager
    cantidad = db.Column(db.Integer, default=1)
    descripcion = db.Column(db.Text)
    salario = db.Column(db.String(100))
    estado = db.Column(db.String(20), default='activa')  # activa, cerrada, pausada
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime)
    
    # Relaciones
    candidatos = db.relationship('Candidato', backref='vacante', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'departamento': self.departamento,
            'nivel': self.nivel,
            'cantidad': self.cantidad,
            'descripcion': self.descripcion,
            'salario': self.salario,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'candidatos_count': len(self.candidatos)
        }

# ==================== MODELO: CANDIDATOS ====================
class Candidato(db.Model):
    __tablename__ = 'candidatos'
    
    id = db.Column(db.Integer, primary_key=True)
    vacante_id = db.Column(db.Integer, db.ForeignKey('vacantes.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))
    documento = db.Column(db.String(20))
    cv_url = db.Column(db.String(200))
    estado = db.Column(db.String(30), default='nuevo')  # nuevo, en_proceso, entrevista, rechazado, contratado
    fecha_aplicacion = db.Column(db.DateTime, default=datetime.utcnow)
    notas = db.Column(db.Text)
    
    # Relaciones
    entrevistas = db.relationship('Entrevista', backref='candidato', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'vacante_id': self.vacante_id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'estado': self.estado,
            'fecha_aplicacion': self.fecha_aplicacion.isoformat()
        }

# ==================== MODELO: ENTREVISTAS ====================
class Entrevista(db.Model):
    __tablename__ = 'entrevistas'
    
    id = db.Column(db.Integer, primary_key=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidatos.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    entrevistador = db.Column(db.String(100))
    tipo = db.Column(db.String(50))  # tecnica, rrhh, gerencial
    estado = db.Column(db.String(20), default='programada')  # programada, realizada, cancelada
    calificacion = db.Column(db.Integer)  # 1-10
    comentarios = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidato_id': self.candidato_id,
            'candidato_nombre': self.candidato.nombre if self.candidato else 'Candidato desconocido',
            'fecha': self.fecha.isoformat(),
            'hora': self.hora.isoformat(),
            'entrevistador': self.entrevistador,
            'tipo': self.tipo,
            'estado': self.estado,
            'calificacion': self.calificacion
        }

# ==================== MODELO: CONTRATOS ====================
class Contrato(db.Model):
    __tablename__ = 'contratos'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # indefinido, fijo, obra
    cargo = db.Column(db.String(100), nullable=False)
    salario = db.Column(db.Float, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(20), default='activo')  # activo, finalizado, terminado
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'empleado_id': self.empleado_id,
            'empleado_nombre': self.empleado.nombre if self.empleado else None,
            'tipo': self.tipo,
            'cargo': self.cargo,
            'salario': self.salario,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'estado': self.estado
        }

# ==================== MODELO: AFILIACIONES ====================
class Afiliacion(db.Model):
    __tablename__ = 'afiliaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # eps, arl, pension, ccf
    entidad = db.Column(db.String(100))
    numero_afiliacion = db.Column(db.String(50))
    fecha_afiliacion = db.Column(db.Date)
    estado = db.Column(db.String(20), default='activo')  # activo, inactivo
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'empleado_id': self.empleado_id,
            'empleado_nombre': self.empleado.nombre if self.empleado else None,
            'tipo': self.tipo,
            'entidad': self.entidad,
            'numero_afiliacion': self.numero_afiliacion,
            'estado': self.estado,
            'fecha_afiliacion': self.fecha_afiliacion.isoformat() if self.fecha_afiliacion else None
        }

# ==================== MODELO: LIQUIDACIONES ====================
class Liquidacion(db.Model):
    __tablename__ = 'liquidaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # nomina, prima, cesantias, vacaciones, definitiva
    periodo_inicio = db.Column(db.Date, nullable=False)
    periodo_fin = db.Column(db.Date, nullable=False)
    salario_base = db.Column(db.Float, nullable=False)
    devengado = db.Column(db.Float)
    deducciones = db.Column(db.Float)
    neto = db.Column(db.Float)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, pagado
    fecha_pago = db.Column(db.Date)
    fecha_calculo = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'empleado_id': self.empleado_id,
            'empleado_nombre': self.empleado.nombre if self.empleado else None,
            'tipo': self.tipo,
            'periodo': f"{self.periodo_inicio.year}-{self.periodo_inicio.month:02d}",
            'periodo_inicio': self.periodo_inicio.isoformat(),
            'periodo_fin': self.periodo_fin.isoformat(),
            'salario_base': self.salario_base,
            'devengado': self.devengado,
            'total_devengado': self.devengado,  # Alias
            'deducciones': self.deducciones,
            'total_deducciones': self.deducciones,  # Alias
            'neto': self.neto,
            'neto_pagar': self.neto,  # Alias
            'estado': self.estado,
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None
        }

# ==================== MODELO: CAPACITACIONES ====================
class Capacitacion(db.Model):
    __tablename__ = 'capacitaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50))  # tecnica, habilidades, seguridad, normativa
    instructor = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date, nullable=False)
    duracion_horas = db.Column(db.Integer)
    costo = db.Column(db.Float)
    estado = db.Column(db.String(20), default='planificada')  # planificada, en_curso, completada
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    participantes = db.relationship('ParticipanteCapacitacion', backref='capacitacion', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'titulo': self.nombre,  # Alias para compatibilidad
            'tipo': self.tipo,
            'instructor': self.instructor,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'duracion_horas': self.duracion_horas,
            'costo': self.costo,
            'estado': self.estado,
            'participantes_count': len(self.participantes)
        }

# ==================== MODELO: PARTICIPANTES CAPACITACION ====================
class ParticipanteCapacitacion(db.Model):
    __tablename__ = 'participantes_capacitacion'
    
    id = db.Column(db.Integer, primary_key=True)
    capacitacion_id = db.Column(db.Integer, db.ForeignKey('capacitaciones.id'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    asistencia = db.Column(db.Boolean, default=True)
    calificacion = db.Column(db.Float)
    certificado = db.Column(db.Boolean, default=False)
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    
    empleado = db.relationship('Empleado', backref='capacitaciones_participadas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'capacitacion_id': self.capacitacion_id,
            'empleado_id': self.empleado_id,
            'asistencia': self.asistencia,
            'calificacion': self.calificacion,
            'certificado': self.certificado
        }

# ==================== MODELO: EVALUACIONES ====================
class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    evaluador_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
    tipo = db.Column(db.String(50), nullable=False)  # desempeno, objetivos, competencias, 360
    periodo = db.Column(db.String(20))  # 2025-Q1, 2025-Q2, etc.
    calificacion = db.Column(db.Float)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, en_proceso, completada
    comentarios = db.Column(db.Text)
    plan_desarrollo = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_completada = db.Column(db.DateTime)
    
    evaluador = db.relationship('Empleado', foreign_keys=[evaluador_id], backref='evaluaciones_realizadas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'empleado_id': self.empleado_id,
            'empleado_nombre': self.empleado.nombre if self.empleado else None,
            'evaluador_id': self.evaluador_id,
            'evaluador_nombre': self.evaluador.nombre if self.evaluador else None,
            'tipo': self.tipo,
            'periodo': self.periodo,
            'calificacion': self.calificacion,
            'estado': self.estado,
            'observaciones': self.comentarios,
            'fecha_inicio': None,  # Agregar si existe en el modelo
            'fecha_fin': None,  # Agregar si existe en el modelo
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_completada': self.fecha_completada.isoformat() if self.fecha_completada else None
        }
