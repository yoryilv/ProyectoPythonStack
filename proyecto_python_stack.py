from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3
)
from constructs import Construct

class ProyectoPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Definir el contexto del bootstrapVersion
        self.node.set_context("@aws-cdk/core:bootstrapVersion", 6)

        # Buscar la VPC por defecto
        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        # Asociar un Security Group existente usando su ID
        security_group = ec2.SecurityGroup.from_security_group_id(
            self, "SG", "sg-0a89f55892deaf213"
        )
        # Utilizar el Role IAM existente (LabRole)
        lab_role = iam.Role.from_role_arn(
            self, "LabRole", role_arn="arn:aws:iam::391666133763:role/LabRole"
        )

        # Crear una instancia EC2 con la nueva versión de MachineImage y keyPair
        instance = ec2.Instance(self, "MyInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            key_pair=ec2.KeyPair.from_key_pair_name(self, "MyKeyPair", "vockey"),
            security_group=security_group,  # Asigna el security group existente
            role=lab_role  # Asigna el rol LabRole a la instancia
        )

        # Referenciar un bucket S3 existente
        my_bucket = s3.Bucket.from_bucket_name(self, "MyExistingBucket", "bucket-cloud32")

        # Script para clonar los repositorios y ejecutar las aplicaciones web
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "sudo yum update -y",
            "sudo yum install -y git",
            "git clone https://github.com/yoryilv/websimple.git /home/ec2-user/websimple",
            "git clone https://github.com/yoryilv/webplantilla.git /home/ec2-user/webplantilla",
            # Subir archivos al bucket S3 existente usando la AWS CLI
            "aws s3 cp /home/ec2-user/websimple s3://bucket-cloud32/websimple --recursive",
            "aws s3 cp /home/ec2-user/webplantilla s3://bucket-cloud32/webplantilla --recursive"
        )
        instance.add_user_data(user_data.render())

        # Agregar permisos para S3
        instance.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )
