from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3_assets as Asset
import os
dirname = os.path.dirname(__file__)
class PythonAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # existing_vpc = ec2.Vpc.from_lookup(self, "Vpc",vpc_id="vpc-010081836644ace6a")
        #     #self, 'existing_vpc', vpc_id="vpc-010081836644ace6a")
            # 640168435046
        existing_vpc = ec2.Vpc(self, "vpc_test", max_azs=2, cidr= "10.1.0.0/16", 
                               subnet_configuration=[
                                   ec2.SubnetConfiguration(subnet_type=ec2.SubnetType.PUBLIC, name="public-subnet", cidr_mask=24),
                                   ec2.SubnetConfiguration(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT, name="private-subnet", cidr_mask=24)
                               ],
                               nat_gateways=1)
        ec2_role = iam.Role(self, "ec2_role", assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'))
        ec2_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))

        #ec2 instance
        ec2_instance = ec2.Instance(self, "application_ec2", instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.LARGE),
                                    machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                    vpc=existing_vpc,
                                    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                    role=ec2_role,
                                    )
        # script in s3 bucket
        # asset = Asset(self, "script", path=os.path.join(dirname, 'userdata.sh'))
        # local_path=ec2_instance.user_data.add_s3_download_command(bucket=asset.bucket, bucket_key=asset.s3_object_key)
        # ec2_instance.user_data.add_execute_file_command(file_path=local_path)
        # asset.grant_read(ec2_instance.ec2_role)
        
        # security group
        ec2_sg=ec2.SecurityGroup(self, "ec2_sg", vpc=existing_vpc,
                                description="sg from cdk",
                                security_group_name="cdk sg",
                                allow_all_outbound=True)
        ec2_sg.add_ingress_rule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(80), "allow http to public")
        ec2_sg.add_ingress_rule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(22), "allow ssh from anywhere")