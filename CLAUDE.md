# Infrastructure CDK Project

This repository contains AWS CDK infrastructure for Nextflow pipeline compute environments, specifically designed for pooled cell painting workflows.

## Architecture Approach

### Minimal CDK Structure
- **Manual setup over `cdk init`**: Created lean structure without unnecessary boilerplate (tests, complex directory structure)
- **Modern Python tooling**: Uses `uv` + `pyproject.toml` instead of traditional `pip` + `requirements.txt`
- **Single stack pattern**: Everything in one `InfrastructureStack` for simplicity

### Key Components
- **IAM Role**: Contains Seqera Forge policy with comprehensive AWS Batch, EC2, EFS, S3 permissions
- **S3 Bucket**: Nextflow work directory with lifecycle rules (30-day retention, 7-day multipart cleanup)
- **Configurable naming**: Context variables for bucket/stack names with sensible defaults

### Design Decisions
1. **Generic naming**: `InfrastructureStack` instead of `SeqeraStack` for future flexibility
2. **Embedded policies**: Seqera Forge policy directly in code rather than external files
3. **Lifecycle management**: Auto-delete objects and bucket for easy cleanup
4. **Minimal dependencies**: Only `aws-cdk-lib` and `constructs`

## File Structure
```
├── app.py                    # CDK app entry point
├── infrastructure_stack.py   # Main stack with IAM + S3 resources
├── pyproject.toml           # Dependencies and project config
├── cdk.json                 # CDK configuration with uv integration
└── README.md                # User-facing documentation
```

## Key Patterns Used

### Policy Integration
- Seqera Forge policy JSON embedded directly in stack code
- S3 bucket permissions granted via CDK `grant_read_write()` method
- Role naming includes stack name for uniqueness

### Resource Configuration
- S3 bucket with `DESTROY` removal policy for development environments
- Lifecycle rules for cost optimization
- CloudFormation outputs for role ARN and bucket details

### Modern Python Tooling
- `uv` for dependency management and execution
- `pyproject.toml` for project configuration
- CDK CLI installed globally via npm, project dependencies via uv

## Context Variables
- `bucketName`: Override default bucket name
- `stackName`: Override default stack name

## Future Extensions
This foundation can be extended with:
- VPC and networking resources
- Additional compute environments (ECS, Lambda)
- Monitoring and logging infrastructure
- Multi-environment configurations
