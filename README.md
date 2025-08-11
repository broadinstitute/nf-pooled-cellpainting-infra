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
# Bootstrap CDK (one-time setup)
uv run cdk bootstrap --profile your-profile-name

# Deploy with defaults (nf-pooled-cellpainting-sandbox bucket)
uv run cdk deploy --profile your-profile-name

# Or customize bucket name
uv run cdk deploy --profile your-profile-name --context bucketName=your-custom-bucket-name
```

## Resources Created

- IAM user with Seqera Forge and Launch permissions
- Access keys for Seqera Platform authentication
- S3 bucket with lifecycle rules
- Outputs: User credentials and bucket details

## Reference

Based on [Seqera AWS Batch](https://docs.seqera.io/platform-cloud/compute-envs/aws-batch#batch-forge) and [nf-tower-aws policies](https://github.com/seqeralabs/nf-tower-aws).
