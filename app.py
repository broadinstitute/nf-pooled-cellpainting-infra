#!/usr/bin/env python3
"""Infrastructure CDK App for Nextflow Pipeline Compute Environment"""

import aws_cdk as cdk
from infrastructure_stack import InfrastructureStack

app = cdk.App()

# Get bucket name from context or use default
bucket_name = app.node.try_get_context("bucketName") or "nf-pooled-cellpainting-sandbox"
stack_name = app.node.try_get_context("stackName") or "NfPooledCellPaintingSandboxStack"

InfrastructureStack(app, stack_name, bucket_name=bucket_name)

app.synth()
