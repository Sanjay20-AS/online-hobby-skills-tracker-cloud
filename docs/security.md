# Security Checklist

- Never commit `.env`.
- Keep JWT secret server-side.
- Never expose S3 secret credentials in React.
- Hash passwords.
- Validate ownership before updates/deletes.
- Restrict upload MIME types and file sizes.
- Use HTTPS in production.
- Configure CORS to the actual frontend origin.
- Add rate limiting and refresh-token rotation for a production-grade extension.
