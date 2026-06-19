# Error Codes Reference

## Application Error Codes

### ERR_1001 — Database Connection Failed
Cause: Application cannot reach the database
Steps:
1. Check your database host and port in Settings > Integrations
2. Whitelist our IP range: 203.0.113.0/24 in your firewall
3. Verify database credentials have not expired
4. Test connection using the 'Test Connection' button

### ERR_2001 — File Upload Failed
Cause: File too large or unsupported format
Limits: Max file size 50MB. Supported: CSV, XLSX, JSON, PDF
Steps:
1. Compress the file if over 50MB
2. Convert to a supported format
3. Check for special characters in filename

### ERR_3001 — Export Timeout
Cause: Dataset too large for synchronous export
Steps:
1. Use the async export option for datasets over 100,000 rows
2. Apply filters to reduce dataset size
3. Schedule export during off-peak hours (midnight to 6am UTC)

### ERR_4001 — Webhook Delivery Failed
Cause: Your endpoint returned non-200 status or timed out
Steps:
1. Ensure endpoint responds within 10 seconds
2. Return HTTP 200 to acknowledge receipt
3. View failed webhook logs in Settings > Webhooks > Delivery Log

### ERR_5001 — Session Expired
Cause: Inactivity timeout after 30 minutes
Steps: Log in again. Enable 'Remember Me' for 30-day sessions.
