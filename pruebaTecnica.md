# Prueba técnica para el Rol de SER

## Descripción

Se propone desarrollar una aplicación sencilla de gestión de usuarios (CRUD) que permita:

- Crear usuarios
- Consultar usuarios
- Actualizar usuarios
- Eliminar usuarios

Cada usuario debe tener los siguientes campos:

- `id`
- `name`
- `email`

La aplicación puede desarrollarse en **cualquier lenguaje de programación**.

## Requisitos de despliegue

La aplicación debe:

- Ejecutarse en **contenedores utilizando Docker**
- Desplegarse en **AWS**
- Quedar **accesible desde internet**

## Arquitectura

El candidato debe:

- Proponer una **arquitectura de solución**
- **Justificar** las decisiones técnicas
- Elegir los **servicios de AWS** que considere adecuados

## Infraestructura como Código

Toda la infraestructura debe crearse utilizando **Infraestructura como Código (IaC)**, mediante herramientas como:

- Terraform
- AWS CloudFormation
- Serverless Framework

## CI/CD

Se deben implementar **pipelines de despliegue** para:

- Backend
- Frontend
- Infraestructura

Utilizando herramientas como:

- GitHub Actions
- GitLab CI/CD
- Azure DevOps

## Entregables

La solución debe entregarse en un **repositorio** que contenga:

- Código fuente de la aplicación
- Definición de la infraestructura
- Pipelines de despliegue
- Un archivo `README.md` que incluya:
  - Descripción de la arquitectura propuesta
  - Decisiones técnicas tomadas
  - Pasos necesarios para desplegar la solución