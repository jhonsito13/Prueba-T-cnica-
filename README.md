# Sistema de Gestión de Actas y Compromisos

Sistema web para gestionar actas, compromisos y gestiones con Django + React.

##  Funcionalidades

- Login con roles (Admin y Usuario Base)
- Lista de actas con filtros
- Detalle de actas con compromisos
- Crear gestiones con archivos adjuntos
- Protección de archivos por autenticación

##  Instalación

### Backend (Django)
```bash
cd backend
pip install django djangorestframework django-cors-headers pillow
python manage.py migrate
python manage.py loaddata initial_data.json
python manage.py runserver
```

### Frontend (React)
```bash
cd frontend
npm install react react-router-dom axios
npm start
```

##  Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| jhom4813@gmail.com | admin1234 | ADMIN |
| usuario@test.com | user123 | BASE |

##  URLs

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Admin Django: `http://localhost:8000/admin`


## Roles y Permisos

- **ADMIN**: Ve todas las actas
- **BASE**: Solo ve actas donde participa (como creador, participante o responsable)

##  Endpoints Principales

- `POST /api/login/` - Autenticación
- `GET /api/actas/` - Lista de actas
- `GET /api/actas/{id}/` - Detalle de acta
- `POST /api/gestiones/` - Crear gestión
