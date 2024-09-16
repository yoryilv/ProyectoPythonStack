#!/usr/bin/env python3
import os

import aws_cdk as cdk

from proyecto_python.proyecto_python_stack import ProyectoPythonStack

# Definir el ID de la cuenta de AWS
account_id = '391666133763'
# Crear una instancia del sintetizador Legacy, que no requiere bootstrap
sintetizador = cdk.LegacyStackSynthesizer()

app = cdk.App()
ProyectoPythonStack(app, "ProyectoPythonStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    env=cdk.Environment(account='391666133763', region='us-east-1'),
    synthesizer=sintetizador

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
