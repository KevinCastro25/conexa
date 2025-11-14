/* ============================================
   CONEXA - JAVASCRIPT
   Funcionalidad e Interactividad
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

/* ==================== INICIALIZACIÓN ==================== */
const initializeApp = () => {
    initNavigation();
    initSmoothScroll();
    initAnimations();
    initForms();
    console.log('✓ Conexa RRHH System Initialized');
};

/* ==================== NAVEGACIÓN ==================== */
const initNavigation = () => {
    const nav = document.querySelector('.nav');
    
    if (!nav) return;
    
    // Efecto de scroll en navegación
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
    
    // Marcar enlace activo
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-list a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
};

/* ==================== SMOOTH SCROLL ==================== */
const initSmoothScroll = () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                const offsetTop = target.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
};

/* ==================== ANIMACIONES ==================== */
const initAnimations = () => {
    // Intersection Observer para animaciones de entrada
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observar cards y elementos
    const animatedElements = document.querySelectorAll('.card, .benefit-item, .stat-box');
    animatedElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = `all 0.6s ease ${index * 0.1}s`;
        observer.observe(el);
    });
};

/* ==================== FORMULARIOS ==================== */
const initForms = () => {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
        
        // Validación en tiempo real
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', () => {
                if (input.classList.contains('error')) {
                    validateField({ target: input });
                }
            });
        });
    });
};

const validateField = (e) => {
    const field = e.target;
    const value = field.value.trim();
    
    // Remover mensaje de error previo
    removeError(field);
    
    // Validar campo requerido
    if (field.hasAttribute('required') && !value) {
        showError(field, 'Este campo es obligatorio');
        return false;
    }
    
    // Validar email
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showError(field, 'Ingrese un email válido');
            return false;
        }
    }
    
    // Validar teléfono
    if (field.type === 'tel' && value) {
        const phoneRegex = /^[\d\s\-\+\(\)]+$/;
        if (!phoneRegex.test(value)) {
            showError(field, 'Ingrese un teléfono válido');
            return false;
        }
    }
    
    return true;
};

const showError = (field, message) => {
    field.classList.add('error');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    field.parentElement.appendChild(errorDiv);
    
    // Agregar estilos de error si no existen
    if (!document.getElementById('error-styles')) {
        const style = document.createElement('style');
        style.id = 'error-styles';
        style.textContent = `
            .error {
                border-color: var(--color-error) !important;
            }
            .error-message {
                color: var(--color-error);
                font-size: var(--text-xs);
                margin-top: var(--space-1);
            }
            .success-message {
                background: var(--color-success);
                color: white;
                padding: var(--space-4);
                border-radius: var(--radius-md);
                margin-bottom: var(--space-4);
                text-align: center;
            }
        `;
        document.head.appendChild(style);
    }
};

const removeError = (field) => {
    field.classList.remove('error');
    const errorMsg = field.parentElement.querySelector('.error-message');
    if (errorMsg) {
        errorMsg.remove();
    }
};

const handleFormSubmit = async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Validar todos los campos
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!validateField({ target: input })) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        return;
    }
    
    // Deshabilitar botón y mostrar loading
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
    
    // Recopilar datos del formulario
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    try {
        // Determinar el endpoint según el formulario
        let endpoint = '/api/submit';
        
        // Detectar el tipo de formulario
        if (form.id === 'newVacancyForm') endpoint = '/api/vacancies';
        else if (form.id === 'newContractForm') endpoint = '/api/contracts';
        else if (form.id === 'newAffiliationForm') endpoint = '/api/affiliations';
        else if (form.id === 'newLiquidationForm') endpoint = '/api/liquidations';
        else if (form.id === 'newTrainingForm') endpoint = '/api/training';
        else if (form.id === 'newEvaluationForm') endpoint = '/api/evaluations';
        else if (form.id === 'demo-form') endpoint = '/api/demo-request';
        
        // Realizar la petición
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Mostrar mensaje de éxito
            showSuccessMessage(form, result.message || '¡Operación exitosa!');
            
            // Resetear formulario
            form.reset();
            
            // Recargar datos si es necesario
            if (window.location.pathname.includes('/modulo/')) {
                setTimeout(() => {
                    location.reload();
                }, 2000);
            }
        } else {
            // Mostrar mensaje de error
            showErrorMessage(form, result.message || 'Ocurrió un error. Por favor intente nuevamente.');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showErrorMessage(form, 'Error de conexión. Por favor verifique su conexión a internet.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
};

const showSuccessMessage = (form, message) => {
    // Remover mensajes previos
    const prevMessages = form.parentElement.querySelectorAll('.success-message, .error-message');
    prevMessages.forEach(msg => msg.remove());
    
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
    
    form.parentElement.insertBefore(successDiv, form);
    
    // Remover después de 5 segundos
    setTimeout(() => {
        successDiv.remove();
    }, 5000);
    
    // Scroll al mensaje
    successDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
};

const showErrorMessage = (formOrElement, message) => {
    // Remover mensajes previos
    const parent = formOrElement.parentElement || formOrElement;
    const prevMessages = parent.querySelectorAll('.success-message, .error-message');
    prevMessages.forEach(msg => msg.remove());
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message-box';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    parent.insertBefore(errorDiv, formOrElement);
    
    // Remover después de 5 segundos
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
    
    // Scroll al mensaje
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
};

const simulateAPICall = (data) => {
    return new Promise((resolve) => {
        console.log('Datos del formulario:', data);
        setTimeout(resolve, 1500);
    });
};

/* ==================== API CALLS ==================== */
const apiCall = async (endpoint, method = 'GET', data = null) => {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
};

/* ==================== UTILIDADES ==================== */
const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
};

const formatDate = (date) => {
    return new Intl.DateTimeFormat('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
};

const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

/* ==================== EXPORT PARA MÓDULOS ==================== */
window.ConexaApp = {
    apiCall,
    formatCurrency,
    formatDate,
    debounce,
    showSuccessMessage,
    showError,
    removeError
};