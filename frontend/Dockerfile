# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Archivos de configuración
COPY package.json package-lock.json* ./
RUN npm ci

# Copia código fuente
COPY . .

# Variables de entorno en build para apuntar a un path genérico en el container o dejar que NGINX reemplace
# Para simplificar en esta prueba, Vite usará variables en tiempo de compilación.
# En un escenario real con Nginx, el URL del backend a menudo es de un config map
ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}

# Compila el frontend estático
RUN npm run build

# Production stage con NGINX
FROM nginx:alpine

# Copiar configuración customizada de Nginx que reenvíe el tráfico base
# Sin embargo, si usamos ALB para enrutar el tráfico /api al backend, 
# Nginx solo servirá estáticos sin problemas.
COPY --from=build /app/dist /usr/share/nginx/html

# Exponer el puerto por el que se comunicará ECS/ALB
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
