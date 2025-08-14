"""Infrastructure Stack for Nextflow Pipeline Compute Environment"""

from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
)
from aws_cdk import (
    aws_iam as iam,
)
from aws_cdk import (
    aws_s3 as s3,
)
from constructs import Construct


class InfrastructureStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, bucket_name: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Seqera Forge Policy (from GitHub)
        forge_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "TowerForge0",
                    "Effect": "Allow",
                    "Action": [
                        "ssm:GetParameters",
                        "iam:CreateInstanceProfile",
                        "iam:DeleteInstanceProfile",
                        "iam:GetRole",
                        "iam:RemoveRoleFromInstanceProfile",
                        "iam:CreateRole",
                        "iam:DeleteRole",
                        "iam:AttachRolePolicy",
                        "iam:PutRolePolicy",
                        "iam:AddRoleToInstanceProfile",
                        "iam:PassRole",
                        "iam:DetachRolePolicy",
                        "iam:ListAttachedRolePolicies",
                        "iam:DeleteRolePolicy",
                        "iam:ListRolePolicies",
                        "iam:TagRole",
                        "iam:TagInstanceProfile",
                        "batch:CreateComputeEnvironment",
                        "batch:DescribeComputeEnvironments",
                        "batch:CreateJobQueue",
                        "batch:DescribeJobQueues",
                        "batch:UpdateComputeEnvironment",
                        "batch:DeleteComputeEnvironment",
                        "batch:UpdateJobQueue",
                        "batch:DeleteJobQueue",
                        "fsx:DeleteFileSystem",
                        "fsx:DescribeFileSystems",
                        "fsx:CreateFileSystem",
                        "fsx:TagResource",
                        "ec2:DescribeSecurityGroups",
                        "ec2:DescribeAccountAttributes",
                        "ec2:DescribeSubnets",
                        "ec2:DescribeLaunchTemplates",
                        "ec2:DescribeLaunchTemplateVersions",
                        "ec2:CreateLaunchTemplate",
                        "ec2:DeleteLaunchTemplate",
                        "ec2:DescribeKeyPairs",
                        "ec2:DescribeVpcs",
                        "ec2:DescribeInstanceTypeOfferings",
                        "ec2:GetEbsEncryptionByDefault",
                        "elasticfilesystem:DescribeMountTargets",
                        "elasticfilesystem:CreateMountTarget",
                        "elasticfilesystem:CreateFileSystem",
                        "elasticfilesystem:DescribeFileSystems",
                        "elasticfilesystem:DeleteMountTarget",
                        "elasticfilesystem:DeleteFileSystem",
                        "elasticfilesystem:UpdateFileSystem",
                        "elasticfilesystem:PutLifecycleConfiguration",
                        "elasticfilesystem:TagResource",
                    ],
                    "Resource": "*",
                },
                {
                    "Sid": "TowerLaunch0",
                    "Effect": "Allow",
                    "Action": [
                        "batch:DescribeJobQueues",
                        "batch:CancelJob",
                        "batch:SubmitJob",
                        "batch:ListJobs",
                        "batch:TagResource",
                        "batch:DescribeComputeEnvironments",
                        "batch:TerminateJob",
                        "batch:DescribeJobs",
                        "batch:RegisterJobDefinition",
                        "batch:DescribeJobDefinitions",
                        "ecs:DescribeTasks",
                        "ec2:DescribeInstances",
                        "ec2:DescribeInstanceTypes",
                        "ec2:DescribeInstanceAttribute",
                        "ecs:DescribeContainerInstances",
                        "ec2:DescribeInstanceStatus",
                        "ec2:DescribeImages",
                        "logs:Describe*",
                        "logs:Get*",
                        "logs:List*",
                        "logs:StartQuery",
                        "logs:StopQuery",
                        "logs:TestMetricFilter",
                        "logs:FilterLogEvents",
                        "ses:SendRawEmail",
                        "secretsmanager:ListSecrets",
                    ],
                    "Resource": "*",
                },
                {"Sid": "S3Access", "Effect": "Allow", "Action": ["s3:*"], "Resource": "*"},
            ],
        }

        # Create IAM user for Seqera programmatic access
        self.seqera_user = iam.User(
            self,
            "SeqeraUser",
            user_name=f"seqera-user-{self.stack_name}",
        )

        # Create managed policies (no size limit)
        forge_managed_policy = iam.ManagedPolicy(
            self,
            "SeqeraForgeManagedPolicy",
            document=iam.PolicyDocument.from_json(forge_policy),
            managed_policy_name=f"SeqeraForgePolicy-{self.stack_name}",
            description="Seqera Forge and Launch permissions for AWS Batch compute environments",
        )

        # Attach managed policy to user
        self.seqera_user.add_managed_policy(forge_managed_policy)

        # Create access key for the user
        self.access_key = iam.AccessKey(self, "SeqeraAccessKey", user=self.seqera_user)

        # Create S3 bucket for Nextflow work directory
        self.bucket = s3.Bucket(
            self,
            "SeqeraBucket",
            bucket_name=bucket_name,
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="DeleteIncompleteMultipartUploads", abort_incomplete_multipart_upload_after=Duration.days(7)
                ),
                s3.LifecycleRule(id="DeleteOldObjects", expiration=Duration.days(30), enabled=True),
            ],
        )

        # Add bucket policy to allow public listing of bucket contents
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:ListBucket"],
                resources=[self.bucket.bucket_arn],
                principals=[iam.AnyPrincipal()],
            )
        )

        # Add S3 bucket access permissions to user (already covered by s3:* in policy)

        # Outputs
        CfnOutput(self, "SeqeraUserName", value=self.seqera_user.user_name)
        CfnOutput(self, "SeqeraAccessKeyId", value=self.access_key.access_key_id)
        CfnOutput(
            self,
            "SeqeraSecretAccessKey",
            value=self.access_key.secret_access_key.unsafe_unwrap(),
            description="Store this securely - it will not be shown again",
        )
        CfnOutput(self, "SeqeraBucketName", value=self.bucket.bucket_name)
        CfnOutput(self, "SeqeraBucketArn", value=self.bucket.bucket_arn)
