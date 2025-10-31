# Claude Code Plan Usage Policy

## Overview

Claude Code provides different plan tiers with varying usage limits and features for developers using the terminal-based AI coding assistant.

## Installation Requirements

- **Node.js**: Version 18 or higher required
- **Installation Command**: `npm install -g @anthropic-ai/claude-code`

## Key Features Across Plans

All Claude Code plans include:

- **Sonnet 4.5 AI Model**: Direct access to Claude's most powerful coding model
- **Codebase Search**: Instantly search through million-line codebases
- **Complex Workflow Automation**: Transform multi-step workflows into single commands
- **VS Code Integration**: Available via marketplace extension
- **Terminal-Native Experience**: "Deep coding at terminal velocity"

## Plan Tiers

Claude Code access is included in specific Claude.com subscription plans:

### Individual Plans

**Free**
- Chat on web/mobile
- Claude Code: NOT included

**Pro** ($20/month or $17/month annual)
- **Claude Code in terminal**: Included
- More usage than Free
- Unlimited projects
- Extended thinking
- Access to more models

**Max** (From $100/month)
- All Pro features
- **Claude Code in terminal**: Included
- 5x or 20x more usage
- Higher output limits
- Early feature access
- Priority access

### Team Plans

**Team Premium Seat** ($150/person/month, minimum 5 members)
- **Claude Code in terminal**: Included
- Collaboration features
- Central billing

**Team Standard Seat** ($30/person/month or $25 annual, minimum 5 members)
- Claude Code: NOT mentioned in features

### Enterprise Plan

- All Team features
- **Claude Code**: Included
- Enhanced context window
- SSO (Single Sign-On)
- Role-based access
- Audit logs
- Compliance API

## API Pricing

For developers using the Anthropic API directly (not Claude.com subscriptions):

**Per 1 Million Tokens**:
- **Opus 4.1**: $15 input / $75 output
- **Sonnet 4.5**: $3-6 input / $15-22.50 output
- **Haiku 3.5**: $0.80 input / $4 output

## Usage Best Practices

1. **API Key Management**: Always store API keys securely in environment variables or CI/CD secrets
2. **Cost Monitoring**: Be mindful of API usage in automated workflows (CI/CD)
3. **Rate Limiting**: Understand your plan's rate limits to avoid interruptions
4. **Model Selection**: Choose appropriate model sizes for tasks (Haiku for simple, Opus for complex)

## Cost Considerations

- **GitHub Actions**: Review costs before enabling automated workflows
- **GitLab CI/CD**: Each pipeline run consumes API credits
- **Extended Context**: `[1m]` models with 1 million token context may cost more

## Third-Party Provider Support

Claude Code supports alternative AI providers beyond Anthropic's API:

- **AWS Bedrock**: IAM-based authentication
- **Google Vertex AI**: GCP-native integration

This allows organizations to use their existing cloud provider relationships and credits.

## Fair Use Guidelines

1. Avoid excessive automated requests
2. Use appropriate model sizes for tasks
3. Implement caching where possible
4. Monitor usage through provider dashboards
5. Set up usage alerts and budgets

## Security Considerations

- Never commit API keys to version control
- Use masked/secret variables in CI/CD
- Review hook scripts before implementation (they execute with your credentials)
- Enable branch protection rules when using automated features

## References

- Official Product Page: https://www.claude.com/product/claude-code
- Documentation: https://docs.claude.com/en/docs/claude-code/
- GitHub Actions Guide: https://docs.claude.com/en/docs/claude-code/github-actions
- GitLab CI/CD Guide: https://docs.claude.com/en/docs/claude-code/gitlab-ci-cd
