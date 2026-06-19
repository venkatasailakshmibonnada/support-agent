# API Authentication Troubleshooting Guide

## Common API Error Codes

### 401 Unauthorized
Cause: Missing or invalid API key
Fix:
- Verify your API key is included in the Authorization header: Authorization: Bearer YOUR_API_KEY
- Ensure the key has not expired or been revoked
- Regenerate your key from the Developer Portal under Settings > API Keys

### 403 Forbidden
Cause: Valid key but insufficient permissions
Fix:
- Check your account plan — some endpoints require Pro or Enterprise plan
- Verify the API key has the correct scope enabled
- Contact your account admin to grant additional permissions

### 429 Too Many Requests
Cause: Rate limit exceeded
Fix:
- Free plan: 100 requests/minute
- Pro plan: 1000 requests/minute
- Enterprise: Custom limits
- Implement exponential backoff in your client code
- Check the Retry-After header for wait time

### 500 Internal Server Error
Cause: Server-side issue
Fix:
- Retry after 30 seconds
- Check status page at status.example.com
- If persists over 10 minutes, open a support ticket with your request ID

## Token Expiry
OAuth tokens expire after 3600 seconds (1 hour).
Refresh using: POST /oauth/token with grant_type=refresh_token
