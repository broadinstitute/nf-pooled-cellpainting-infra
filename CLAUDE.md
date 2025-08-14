# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AWS CDK infrastructure project for Seqera Platform (formerly Nextflow Tower) compute environments. See README.md for basic setup and deployment instructions.

## Architecture

- `app.py`: CDK application entry point that creates the infrastructure stack with configurable context parameters (`bucketName`, `stackName`)
- `infrastructure_stack.py`: Main stack containing all AWS resources with Seqera-specific IAM policies
- Uses managed policies instead of inline policies to avoid IAM size limits (this was changed to fix deployment issues)
- IAM policies are based on official nf-tower-aws policies from Seqera Labs with comprehensive Forge and Launch permissions

## Development Commands

```bash
# Linting and formatting (uses ruff configuration from pyproject.toml)
ruff format .
ruff check .

# CDK synthesis for validation
uv run cdk synth --profile your-profile-name

# Deploy with custom stack name context
uv run cdk deploy --profile your-profile-name --context stackName=YourCustomStackName

# Destroy infrastructure
uv run cdk destroy --profile your-profile-name
```

## Key Implementation Details

- The stack creates IAM users with managed policies containing both Seqera Forge and Launch permissions in a single policy document
- S3 bucket includes lifecycle rules: 7-day multipart upload cleanup and 30-day object expiration
- CDK outputs provide all credentials and ARNs needed for Seqera Platform configuration
- Stack name and bucket name are configurable via CDK context parameters