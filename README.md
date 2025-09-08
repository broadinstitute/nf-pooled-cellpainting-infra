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

## Related Repositories

- [nf-pooled-cellpainting-assets](https://github.com/broadinstitute/nf-pooled-cellpainting-assets) - Supporting assets and test data
- [nf-pooled-cellpainting](https://github.com/seqera-services/nf-pooled-cellpainting) - Main nf-core pipeline

## Reference

IAM policies combine permissions for both compute environment types:
- **AWS Batch**: Based on [nf-tower-aws policies](https://github.com/seqeralabs/nf-tower-aws) for running Nextflow pipelines on AWS Batch
- **AWS Cloud**: Additional permissions from [Seqera Platform AWS Cloud Documentation](https://docs.seqera.io/platform-enterprise/compute-envs/aws-cloud#required-permissions) for single EC2 instances (Studios)

## Future Improvements

- **IAM Policy Structure**: Current implementation combines all permissions into a single policy. Consider restructuring into separate policies for AWS Batch vs AWS Cloud compute environments to follow least-privilege principles.
