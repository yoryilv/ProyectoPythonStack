#!/usr/bin/env python3
import os
import aws_cdk as cdk
from proyecto_python.proyecto_python_stack import ProyectoPythonStack

# Definir el ID de la cuenta de AWS
account_id = '391666133763'

# Crear una instancia del sintetizador personalizado
sintetizador = cdk.DefaultStackSynthesizer(
    cloud_formation_execution_role=f"arn:aws:iam::{account_id}:role/LabRole"
)

app = cdk.App()

# Crear la pila `ProyectoPythonStack` y pasar el sintetizador personalizado
ProyectoPythonStack(app, "ProyectoPythonStack",
    env=cdk.Environment(account=account_id, region='us-east-1'),
    synthesizer=sintetizador
)

# Sintetizar la aplicación para generar la plantilla de CloudFormation
app.synth()
