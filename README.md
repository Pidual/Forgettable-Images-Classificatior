# Forgettable-Images-Classificatior (WIP)
![Screenshot from 2025-03-30 23-13-26](https://github.com/user-attachments/assets/9f7b97a2-f687-433d-bdf5-5d1ab8699a4e)

# Proyecto: Orquestacion de Microservicios con Traefik
## Integrantes
- **[CARLOS HERNANDO LOZANO PEREZ]**

## Descripción
Este proyecto implementa un entorno donde múltiples servicios se comunican entre sí a través de **Traefik**, aplicando balanceo de carga, seguridad, monitoreo y una configuración avanzada de ruteo.

## Requisitos Implementados

### 1. Balanceo de Carga
- **Configuración de Traefik** para distribuir las solicitudes entre tres instancias del servicio **users_service**.

### 2. Reglas de Enrutamiento Dinámico
- **Autenticación**: Usuarios autenticados son dirigidos a un grupo de servidores específicos. (No realmente pues se utiliza JWT en realidad no se redirige nada)
- **Acceso a /admin**: Solo usuarios con IP en lista blanca pueden acceder. (No implementado)
- **Alta Carga**: Se activa un servidor de respaldo si hay tráfico elevado. (No implementado)

### 3. Gestión de Errores Personalizada
- **Página de error personalizada** para servicios no disponibles, utilizando **Nginx**. (Se implemento)

### 4. Monitoreo
- **Integración con Prometheus y Grafana** para analizar el rendimiento del sistema. (No implementado)

---

## Estructura de Carpetas
```
├── docker-compose.yml        # Orquestación de los servicios
├── nginx/                    # Configuración de Nginx para errores
│   ├── error.html            # html que se muestra para errores 500-599
│   └── nginx.conf
├── users_service/            # Microservicio de usuarios
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── ...
├── images_service/           # Microservicio de imágenes
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── ...
├── inference_service/        # Microservicio de inferencia
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── ...
├── monitoring/               # Configuración de monitoreo
│   ├── prometheus.yml
│   ├── grafana/
│   └── ...
└── README.md                 # Documentación del proyecto
```

---

## Flujo de Tráfico en Traefik
1. **El usuario realiza una solicitud** a `http://users.localhost/`.
2. **Traefik analiza la petición** y aplica las reglas de ruteo.
3. **Si está autenticado**, es redirigido a un grupo específico de servidores.
4. **Si accede a /admin**, se verifica su IP antes de permitir el acceso.
5. **Si hay alta carga**, Traefik activa un servidor adicional.
6. **Si un servicio falla**, la solicitud es enviada a Nginx para mostrar un error personalizado.

---

## Respuestas a las Preguntas  🤑🤑🤑

### 1. ¿Cómo detecta Traefik los servicios configurados en Docker Compose?
Traefik detecta los servicios a través de la opción `--providers.docker=true` y usa etiquetas (`labels`) en los contenedores para configurar routers, middlewares y servicios.

### 2. ¿Qué rol juegan los middlewares en la seguridad y gestión del tráfico?
Los middlewares permiten modificar las solicitudes antes de enviarlas a los servicios. Se usan para autenticación, redirección, compresión, control de tráfico y restricciones de acceso.

### 3. ¿Cómo se define un router en Traefik y qué parámetros son esenciales?
Un router se define con etiquetas en Docker Compose o en un archivo de configuración (`traefik.yml`). Parámetros esenciales:
- `rule`: Define las condiciones para enrutar (ej., `Host("users.localhost")`).
- `entrypoints`: Define en qué puerto recibe tráfico (ej., `web`).
- `service`: Especifica el servicio de destino.

### 4. ¿Cuál es la diferencia entre un router y un servicio en Traefik?
- **Router**: Define cómo se enruta una petición basándose en reglas.
- **Servicio**: Representa el destino final donde Traefik enviará la solicitud (ej., un contenedor de una API).

### 5. ¿Cómo se pueden agregar más reglas de enrutamiento para diferentes rutas?
Se pueden definir múltiples routers con distintas reglas en Docker Compose o `traefik.yml`. Ejemplo:
```yaml
- "traefik.http.routers.api.rule=PathPrefix(`/api`)
- "traefik.http.routers.admin.rule=Host(`admin.localhost`) && PathPrefix(`/dashboard`)
```

---

## Instrucciones para Ejecutar el Proyecto
1. Clonar el repositorio:
   ```sh
   git clone <repo_url>
   cd <repo>
   ```
2. Levantar los servicios con Docker Compose:
   ```sh
   docker-compose up -d
   ```
3. Acceder a los servicios:
   - **Traefik Dashboard**: [http://localhost:8080](http://localhost:8080)
   - **Users Service**: [http://users.localhost](http://users.localhost)
   - **Images Service**: [http://images.localhost](http://images.localhost)
   - **Inference Service**: [http://inference.localhost](http://inference.localhost)
   - **Error Page**: [http://error.localhost](http://error.localhost)

---





Clona el repositorio:

git clone [<URL_DEL_REPO>](https://github.com/Pidual/Forgettable-Images-Classificatior)
cd <NOMBRE_DEL_PROYECTO>

Levanta los servicios con Docker Compose:

docker-compose up -d

Accede a los servicios:

Traefik Dashboard: http://localhost:8080

Usuarios: http://users.localhost

Imágenes: http://images.localhost

Inferencia: http://inference.localhost

🛠 Cómo Probar los Endpoints

Puedes probar los servicios con Postman 

