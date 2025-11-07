# Conexa

## Requisitos
- Python 3.7+
- Flask
- Flask-CORS

## Instalación

1. Crear un entorno virtual:
```
python -m venv venv
```

2. Activar el entorno virtual:
- Windows:
```
venv\Scripts\activate
```

3. Instalar las dependencias:
```
pip install flask flask-cors
```

## Ejecutar la aplicación

1. Asegúrate de tener el entorno virtual activado
2. Ejecuta:
```
python app.py
```

3. Abre tu navegador en `http://localhost:5000`

## Estructura del proyecto
```
Conexa/
├── app.py              # Aplicación Flask principal
├── static/            # Archivos estáticos
│   ├── style.css     # Estilos CSS
│   └── main.js       # JavaScript principal
├── templates/         # Plantillas HTML
│   └── index.html    # Página principal
└── venv/             # Entorno virtual (generado al instalarlo)
```