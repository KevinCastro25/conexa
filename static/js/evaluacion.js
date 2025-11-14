// Variable global para almacenar empleados
let allEmployees = [];

// Cargar empleados para los selectores
async function loadEmployees() {
    try {
        const response = await fetch('/api/employees');
        const result = await response.json();
        allEmployees = result.data || result;
        
        // Llenar selector de empleado evaluado
        const evaluatedSelect = document.getElementById('evaluatedEmployee');
        evaluatedSelect.innerHTML = '<option value="">Seleccione un empleado...</option>';
        
        // Llenar selector de plan de desarrollo
        const planSelect = document.getElementById('employeePlan');
        planSelect.innerHTML = '<option value="">Seleccione un empleado...</option>';
        
        allEmployees.forEach(emp => {
            const option1 = document.createElement('option');
            option1.value = emp.id;
            option1.textContent = `${emp.nombre} - ${emp.cargo || 'Sin cargo'}`;
            evaluatedSelect.appendChild(option1);
            
            const option3 = document.createElement('option');
            option3.value = emp.id;
            option3.textContent = `${emp.nombre} - ${emp.cargo || 'Sin cargo'}`;
            planSelect.appendChild(option3);
        });
        
        // Inicialmente llenar evaluadores con todos los empleados
        updateEvaluatorSelect();
        
        // Escuchar cambios en el empleado evaluado para actualizar evaluadores
        evaluatedSelect.addEventListener('change', function() {
            updateEvaluatorSelect(this.value);
        });
    } catch (error) {
        console.error('Error cargando empleados:', error);
    }
}

// Actualizar selector de evaluadores excluyendo al empleado seleccionado
function updateEvaluatorSelect(excludeEmployeeId = null) {
    const evaluatorSelect = document.getElementById('evaluator');
    const currentValue = evaluatorSelect.value;
    
    evaluatorSelect.innerHTML = '<option value="">Seleccione un evaluador...</option>';
    
    allEmployees.forEach(emp => {
        // No mostrar el empleado que está siendo evaluado
        if (emp.id.toString() !== excludeEmployeeId?.toString()) {
            const option = document.createElement('option');
            option.value = emp.id;
            option.textContent = `${emp.nombre} - ${emp.cargo || 'Sin cargo'}`;
            evaluatorSelect.appendChild(option);
        }
    });
    
    // Restaurar valor si aún está disponible
    if (currentValue && currentValue !== excludeEmployeeId) {
        evaluatorSelect.value = currentValue;
    }
}

// Cargar evaluaciones
async function loadEvaluations() {
    try {
        const response = await fetch('/api/evaluations');
        const result = await response.json();
        
        if (result.success && result.data) {
            const evaluations = result.data;
            updateEvaluationsTable(evaluations);
            updateEvaluationStats(evaluations);
        }
    } catch (error) {
        console.error('Error cargando evaluaciones:', error);
    }
}

// Actualizar tabla de evaluaciones
function updateEvaluationsTable(evaluations) {
    const tbody = document.getElementById('activeEvaluationsTable');
    
    if (evaluations.length > 0) {
        tbody.innerHTML = evaluations.map(evaluation => `
            <tr>
                <td><strong>${evaluation.empleado_nombre || 'Empleado #' + evaluation.empleado_id}</strong></td>
                <td>${formatEvaluationType(evaluation.tipo)}</td>
                <td>${evaluation.periodo || 'N/A'}</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${getEvaluationProgress(evaluation)}%"></div>
                    </div>
                    ${getEvaluationProgress(evaluation)}%
                </td>
                <td>
                    <button class="btn btn-sm btn-outline" onclick="verDetalleEvaluacion(${evaluation.id})">
                        <i class="fas fa-eye"></i> Ver Detalle
                    </button>
                </td>
            </tr>
        `).join('');
    } else {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-gray-600">
                    No hay evaluaciones registradas
                </td>
            </tr>
        `;
    }
}

// Actualizar estadísticas
function updateEvaluationStats(evaluations) {
    const completed = evaluations.filter(e => e.estado === 'completada' || e.estado === 'Completada').length;
    const pending = evaluations.length - completed;
    
    // Calcular promedio de calificaciones
    const completedEvals = evaluations.filter(e => e.calificacion && e.calificacion > 0);
    const average = completedEvals.length > 0 
        ? (completedEvals.reduce((sum, e) => sum + (e.calificacion || 0), 0) / completedEvals.length).toFixed(1)
        : '0';
    
    document.getElementById('averageScore').textContent = average + '/100';
    document.getElementById('completedEvaluations').textContent = completed;
    document.getElementById('pendingEvaluations').textContent = pending;
}

// Ver detalle de evaluación
async function verDetalleEvaluacion(id) {
    try {
        const response = await fetch('/api/evaluations');
        const result = await response.json();
        
        if (result.success && result.data) {
            const evaluation = result.data.find(e => e.id === id);
            
            if (!evaluation) {
                alert('No se encontró la evaluación');
                return;
            }
            
            // Crear modal
            const modal = document.createElement('div');
            modal.className = 'modal-overlay';
            modal.innerHTML = `
                <div class="modal-content" style="max-width: 700px;">
                    <div class="modal-header">
                        <h2><i class="fas fa-clipboard-check"></i> Detalle de Evaluación</h2>
                        <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="modal-body">
                        <!-- Información General -->
                        <div class="detail-section">
                            <h3 style="color: var(--color-accent); margin-bottom: 1rem; border-bottom: 2px solid var(--color-accent); padding-bottom: 0.5rem;">
                                <i class="fas fa-info-circle"></i> Información General
                            </h3>
                            <div class="detail-grid">
                                <div class="detail-item">
                                    <label><i class="fas fa-user"></i> Empleado Evaluado:</label>
                                    <span style="font-weight: 600;">${evaluation.empleado_nombre || 'Empleado #' + evaluation.empleado_id}</span>
                                </div>
                                <div class="detail-item">
                                    <label><i class="fas fa-user-tie"></i> Evaluador:</label>
                                    <span>${evaluation.evaluador_nombre || 'Evaluador #' + evaluation.evaluador_id}</span>
                                </div>
                                <div class="detail-item">
                                    <label><i class="fas fa-tag"></i> Tipo de Evaluación:</label>
                                    <span>${formatEvaluationType(evaluation.tipo)}</span>
                                </div>
                                <div class="detail-item">
                                    <label><i class="fas fa-calendar-alt"></i> Periodo:</label>
                                    <span>${evaluation.periodo || 'N/A'}</span>
                                </div>
                                <div class="detail-item">
                                    <label><i class="fas fa-signal"></i> Estado:</label>
                                    <span class="badge ${getStatusBadge(evaluation.estado)}">${getStatusLabel(evaluation.estado)}</span>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Resultados -->
                        ${evaluation.calificacion ? `
                        <div class="detail-section">
                            <h3 style="color: var(--color-accent); margin-bottom: 1rem; border-bottom: 2px solid var(--color-accent); padding-bottom: 0.5rem;">
                                <i class="fas fa-star"></i> Resultados
                            </h3>
                            <div class="detail-grid">
                                <div class="detail-item">
                                    <label><i class="fas fa-chart-line"></i> Calificación:</label>
                                    <span style="font-size: 1.5rem; color: ${getScoreColor(evaluation.calificacion)}; font-weight: bold;">
                                        ${evaluation.calificacion}/100
                                    </span>
                                </div>
                                <div class="detail-item">
                                    <label><i class="fas fa-tasks"></i> Progreso:</label>
                                    <span>
                                        <div class="progress-bar" style="width: 150px; display: inline-block; vertical-align: middle;">
                                            <div class="progress-fill" style="width: ${getEvaluationProgress(evaluation)}%"></div>
                                        </div>
                                        ${getEvaluationProgress(evaluation)}%
                                    </span>
                                </div>
                            </div>
                        </div>
                        ` : ''}
                        
                        <!-- Observaciones -->
                        ${evaluation.observaciones ? `
                        <div class="detail-section">
                            <h3 style="color: var(--color-accent); margin-bottom: 1rem; border-bottom: 2px solid var(--color-accent); padding-bottom: 0.5rem;">
                                <i class="fas fa-comment"></i> Observaciones
                            </h3>
                            <p style="color: var(--color-gray-700); line-height: 1.6; padding: 1rem; background: var(--color-gray-100); border-radius: var(--radius-md);">
                                ${evaluation.observaciones}
                            </p>
                        </div>
                        ` : ''}
                        
                        <!-- Fechas -->
                        <div class="detail-section">
                            <h3 style="color: var(--color-accent); margin-bottom: 1rem; border-bottom: 2px solid var(--color-accent); padding-bottom: 0.5rem;">
                                <i class="fas fa-calendar"></i> Fechas
                            </h3>
                            <div class="detail-grid">
                                ${evaluation.fecha_inicio ? `
                                <div class="detail-item">
                                    <label><i class="fas fa-play"></i> Fecha de Inicio:</label>
                                    <span>${formatDate(evaluation.fecha_inicio)}</span>
                                </div>
                                ` : ''}
                                ${evaluation.fecha_fin ? `
                                <div class="detail-item">
                                    <label><i class="fas fa-flag-checkered"></i> Fecha de Fin:</label>
                                    <span>${formatDate(evaluation.fecha_fin)}</span>
                                </div>
                                ` : ''}
                                ${evaluation.fecha_creacion ? `
                                <div class="detail-item">
                                    <label><i class="fas fa-calendar-plus"></i> Fecha de Creación:</label>
                                    <span>${formatDate(evaluation.fecha_creacion)}</span>
                                </div>
                                ` : ''}
                            </div>
                        </div>
                        
                        <!-- Registro -->
                        <div class="detail-section" style="background: var(--color-gray-100); padding: 1rem; border-radius: var(--radius-md); margin-top: 1.5rem;">
                            <div style="display: flex; justify-content: space-between; font-size: 0.875rem; color: var(--color-gray-600);">
                                <span><i class="fas fa-hashtag"></i> ID: ${evaluation.id}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="modal-footer">
                        <button class="btn btn-outline" onclick="this.closest('.modal-overlay').remove()">
                            <i class="fas fa-times"></i> Cerrar
                        </button>
                        ${evaluation.estado !== 'completada' ? `
                        <button class="btn" onclick="completarEvaluacion(${evaluation.id})">
                            <i class="fas fa-check"></i> Completar Evaluación
                        </button>
                        ` : ''}
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Cerrar al hacer clic fuera del modal
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.remove();
                }
            });
        }
    } catch (error) {
        console.error('Error cargando detalle:', error);
        alert('Error al cargar el detalle de la evaluación');
    }
}

// Funciones auxiliares
function formatEvaluationType(tipo) {
    const types = {
        'desempeno': 'Desempeño General',
        'objetivos': 'Cumplimiento de Objetivos',
        'competencias': 'Evaluación de Competencias',
        '360': 'Evaluación 360°'
    };
    return types[tipo] || tipo || 'N/A';
}

function getEvaluationProgress(evaluation) {
    if (evaluation.estado === 'completada') return 100;
    if (evaluation.estado === 'en_proceso') return 50;
    return 0;
}

function getStatusBadge(estado) {
    const badges = {
        'pendiente': 'badge-warning',
        'en_proceso': 'badge-info',
        'completada': 'badge-success'
    };
    return badges[estado] || 'badge-warning';
}

function getStatusLabel(estado) {
    const labels = {
        'pendiente': 'Pendiente',
        'en_proceso': 'En Proceso',
        'completada': 'Completada'
    };
    return labels[estado] || estado || 'Pendiente';
}

function getScoreColor(score) {
    if (score >= 80) return '#2e7d32'; // Verde
    if (score >= 60) return '#f57c00'; // Naranja
    return '#d32f2f'; // Rojo
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-CO', { 
        day: 'numeric', 
        month: 'long', 
        year: 'numeric' 
    });
}

function completarEvaluacion(id) {
    alert('Completar evaluación #' + id + '\n\nEsta funcionalidad abrirá el formulario de evaluación completo.');
    document.querySelector('.modal-overlay')?.remove();
}

// Manejo del formulario de nueva evaluación
document.getElementById('newEvaluationForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    
    const formData = {
        empleado_id: document.getElementById('evaluatedEmployee').value,
        evaluador_id: document.getElementById('evaluator').value,
        tipo: document.getElementById('evaluationType').value,
        periodo: document.getElementById('period').value,
        estado: 'pendiente'
    };
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creando...';
    
    try {
        const response = await fetch('/api/evaluations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            if (window.ConexaApp && window.ConexaApp.showSuccessMessage) {
                window.ConexaApp.showSuccessMessage(e.target, '✓ Evaluación creada exitosamente');
            } else {
                alert('✓ Evaluación creada exitosamente');
            }
            e.target.reset();
            loadEvaluations();
        } else {
            alert('Error: ' + (result.message || 'No se pudo crear la evaluación'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear la evaluación. Por favor, intente nuevamente.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
}, true);

// Cargar datos al iniciar
document.addEventListener('DOMContentLoaded', () => {
    loadEmployees();
    loadEvaluations();
});
