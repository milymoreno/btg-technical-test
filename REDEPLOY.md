# Guía de Redespliegue y Limpieza

Este documento detalla los pasos para volver a desplegar la aplicación "User Management Hub" después de haber destruido la infraestructura.

## Cómo redesplegar (Paso a Paso)

Para volver a tener todo operativo, sigue este orden en la pestaña **Actions** de GitHub:

1.  **Infraestructura**: Ejecuta el pipeline `Terraform Infrastructure`.
    - Esto creará de nuevo la red, el balanceador y la base de datos.
    - **Nota**: Al finalizar, el ALB tendrá una nueva URL DNS (ejemplo: `btg-tech-test-alb-XXXXXX.us-east-1.elb.amazonaws.com`).
2.  **Backend**: Ejecuta el pipeline `Backend Deployment`.
    - Construirá la imagen y la desplegará en el nuevo ECS.
3.  **Frontend**: Ejecuta el pipeline `Frontend Deployment`.
    - Este paso es crucial: El frontend detectará automáticamente la nueva URL del balanceador durante la construcción.

## ¿Qué hacer si quieres borrar todo de nuevo?

Si tienes acceso a una terminal con Terraform configurado:

```bash
cd infra
AWS_PROFILE=mily-aws-student terraform destroy -auto-approve
```

O simplemente deja de usar la aplicación; los pipelines de GitHub no consumen recursos de AWS a menos que los ejecutes.

---

**Documentación generada para facilitar el mantenimiento del proyecto.**
