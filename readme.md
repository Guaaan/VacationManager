# Vacation Manager — API Django

Este repositorio contiene una API mínima en **Django + Django REST Framework** para gestionar solicitudes de vacaciones y el saldo de días por usuario (SQLite). Esta README explica cómo levantar el proyecto localmente, ejecutar migraciones, crear un superusuario y probar los endpoints básicos.

> Esta primera versión incluye solo la API y la lógica de negocio básica. La integración con Microsoft Graph (auth y creación de eventos) se agregará en pasos posteriores.

---

## Requisitos

- Python 3.10+ (o 3.9+) instalado
- Git (opcional)
- Entorno virtual (recomendado): `venv` o `virtualenv`

---

## Preparar el proyecto (pasos rápidos)

A continuación se muestran los pasos para clonar (si aplica), preparar el entorno, instalar dependencias y levantar el servidor de desarrollo.

### 1. Clona el repo (si aplica)

```bash
# si ya tienes el proyecto local no es necesario
git clone <URL_DEL_REPO>
cd vacation_manager
```

### 2. Crear y activar entorno virtual

Unix / macOS:

```bash
python -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
# o en cmd: venv\Scripts\activate.bat
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install django djangorestframework
```

> Si en el futuro integras MSAL o requests para Graph, añade `msal requests` al pip install.

### 4. Configurar settings (opcional)

El proyecto usa SQLite por defecto. Revisa `vacation_manager/settings.py` para ver `AUTH_USER_MODEL = 'users.User'` y `INSTALLED_APPS`. Si quieres configurar variables sensibles (client secret, client id), crea un archivo `.env` y carga las variables en `settings.py` (no subas `.env` al repo).

Ejemplo de variables que podrías añadir más adelante:

```env
SECRET_KEY=tu_secret_key_de_django
DEBUG=True
AZURE_CLIENT_ID=...
AZURE_CLIENT_SECRET=...
AZURE_TENANT_ID=...
```

### 5. Migraciones y superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Sigue las instrucciones para crear el admin (usuario con permisos de superuser).

### 6. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Abre en el navegador: `http://127.0.0.1:8000/` y el admin en `http://127.0.0.1:8000/admin/`.

---

## Endpoints principales (base: `/api/`)

El proyecto usa `rest_framework.routers.DefaultRouter()` y expone dos recursos principales:

- `GET /api/users/` — lista de usuarios (Read-only por ahora)
- `GET /api/users/{id}/` — detalle de usuario (incluye `vacation_days`)
- `GET /api/vacations/` — lista de solicitudes de vacaciones
- `POST /api/vacations/` — crear solicitud de vacaciones
- `POST /api/vacations/{id}/approve/` — acción personalizada para aprobar la solicitud (actualiza `vacation_days` y marca la solicitud como `APPROVED`)

> Actualmente las `permission_classes` están en `AllowAny` para facilitar pruebas. En el siguiente paso implementaremos autenticación y permisos (JWT o similar).

---

## Ejemplos de uso con `curl`

> Si aún no tienes autenticación activa, el serializer permite pasar `user` en el payload para crear la solicitud.

1. Crear una solicitud (suponiendo que el usuario con id `1` existe):

```bash
curl -X POST http://127.0.0.1:8000/api/vacations/ \
  -H "Content-Type: application/json" \
  -d '{"user":1,"start_date":"2025-12-20","end_date":"2025-12-24"}'
```

Respuesta: objeto `VacationRequest` con `status: "PENDING"`.

2. Listar solicitudes:

```bash
curl http://127.0.0.1:8000/api/vacations/
```

3. Aprobar solicitud (id = 1):

```bash
curl -X POST http://127.0.0.1:8000/api/vacations/1/approve/
```

Al aprobar la solicitud, el sistema resta `days_requested` del campo `user.vacation_days`.

---

## Puntos importantes y recomendaciones

- **Autenticación**: ahora mismo los endpoints permiten acceso libre. En el siguiente paso recomendamos implementar JWT con `djangorestframework-simplejwt` y cambiar permisos:
  - Crear/editar solicitudes -> `IsAuthenticated`
  - Aprobar -> `IsAdminUser` (o permiso personalizado)

- **Validaciones adicionales**: para un producto real hay que agregar validaciones sobre solapamiento de solicitudes, manejo de días hábiles, feriados y medias jornadas.

- **Integración con Microsoft Graph**: cuando se integre, guarda las credenciales en variables de entorno y decide entre `client_credentials` (app-only) o `authorization_code` (delegated).

- **Producción**: cambia SQLite por Postgres, usa `gunicorn`/`uvicorn` y configura HTTPS, manejo de secretos y reverse proxy.

- **Background tasks**: para crear eventos en Graph es recomendable usar una cola (Celery/RQ) en vez de llamadas síncronas en la acción `approve`.

---

## Tests (opcional)

Si agregas tests, ejecútalos con:

```bash
python manage.py test
```

---

## Siguientes pasos sugeridos

1. Implementar autenticación JWT y proteger endpoints.
2. Añadir MSAL + lógica para crear eventos en Microsoft Calendar al aprobar.
3. Agregar validaciones de solapamiento y feriados.
4. Añadir front-end o una pequeña interfaz para solicitudes.

---


© Vacation Manager

