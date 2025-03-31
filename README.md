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
   git clone https://github.com/Pidual/Forgettable-Images-Classificatior
   cd Forgettable-Images-Classificatior
   ```
2. Levantar los servicios con Docker Compose:
   ```sh
   docker-compose up -d
   ```
2.1 Agregar esta regla a /etc/hosts para que el DNS resuelva los endpoints
127.0.0.1   users.localhost images.localhost inference.localhost  
3. Acceder a los servicios:
   - **Traefik Dashboard**: [http://localhost:8080](http://localhost:8080)
   - **Users Service**: [http://users.localhost](http://users.localhost)
   - **Images Service**: [http://images.localhost](http://images.localhost)
   - **Inference Service**: [http://inference.localhost](http://inference.localhost)
   - **Error Page**: [http://error.localhost](http://error.localhost)

---


## 🛠 Cómo Probar los Endpoints
Puedes probar los servicios utilizando **Postman** o **cURL**.

### 🔑 1. Obtener un Token JWT (Usuarios)
REGISTRARSE
![Screenshot from 2025-03-30 23-31-44](https://github.com/user-attachments/assets/530709bc-c41d-429b-b9a4-1034f5299aec)
LOGGEARSE
![Screenshot from 2025-03-30 23-32-46](https://github.com/user-attachments/assets/74cd4759-f323-45bf-8d39-ab372ce4b6c5)


### 📤 2. Subir una Imagen

![image](https://github.com/user-attachments/assets/f799aaf8-c6ff-42ba-92b9-5da175555faf)
![Screenshot from 2025-03-30 23-34-11](https://github.com/user-attachments/assets/c95a9037-22b1-4bff-aae8-bf4c57ee930a)
![image](https://github.com/user-attachments/assets/1f27293f-72cb-41a9-8fa3-4f1fd81b4695)
RESPUESTA ESPERADA
![image](https://github.com/user-attachments/assets/e861b167-06c4-49f5-bd8f-6660dc532926)


### 🧠 3. Hacer una Inferencia
```sh
curl -X GET http://inference.localhost/predict/123 \
     -H "Authorization: Bearer jwt_token_here"
```
**Respuesta esperada:**
```json
{
    "prediction": "forgetable"
}
```
