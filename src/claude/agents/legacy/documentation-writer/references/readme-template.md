# Documentation Writer - README Template

```markdown
# Project Name

Brief project description (1-2 sentences).

## Features

- Feature 1
- Feature 2
- Feature 3

## Prerequisites

- Node.js 18+
- PostgreSQL 15+
- Docker (optional)

## Installation

```bash
# Clone repository
git clone https://github.com/org/repo.git
cd repo

# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | - |
| `JWT_SECRET` | Secret for JWT signing | - |
| `PORT` | Server port | 3000 |

## Usage

```bash
# Development
npm run dev

# Production
npm run build
npm start

# Tests
npm test
```

## API Documentation

See [API Documentation](docs/api.md) for detailed endpoint information.

## Architecture

See [Architecture Documentation](docs/architecture.md) for system design.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

[License Type] - See LICENSE file for details.

## Support

- Documentation: [docs link]
- Issues: [GitHub issues]
- Email: support@example.com
```
