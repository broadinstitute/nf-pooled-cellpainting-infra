# Seqera Infrastructure

AWS CDK infrastructure for Seqera Platform with IAM roles and S3 bucket.

## Setup

```bash
# Install dependencies
uv sync

# Install CDK CLI (required)
npm install -g aws-cdk@latest
```

## Deploy

```bash
# Deploy with defaults (nf-pooled-cellpainting-sandbox bucket)
uv run cdk deploy

# Or customize bucket name
uv run cdk deploy --context bucketName=your-custom-bucket-name
```

## Resources Created

- IAM role with Seqera Forge permissions
- S3 bucket with lifecycle rules
- Outputs: Role ARN and bucket details

## Reference

Based on [Seqera AWS Batch](https://docs.seqera.io/platform-cloud/compute-envs/aws-batch#batch-forge) and [nf-tower-aws policies](https://github.com/seqeralabs/nf-tower-aws).
