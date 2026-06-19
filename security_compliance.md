# Security and Compliance Guide

## Two-Factor Authentication (2FA)
Strongly recommended for all accounts. Setup:
1. Settings > Security > Enable Two-Factor Authentication
2. Scan QR code with Google Authenticator or Authy
3. Enter the 6-digit code to confirm
4. Save backup codes in a secure location

Once enabled, 2FA is required at every login.

## Single Sign-On (SSO)
Available on Enterprise plan:
- Supports SAML 2.0 and OAuth 2.0
- Compatible with Okta, Azure AD, Google Workspace
- Setup: Settings > Security > SSO Configuration
- Requires DNS verification of your domain

## Security Best Practices
- Use a unique, strong password (12+ characters)
- Enable 2FA on your account
- Never share API keys — rotate them regularly
- Review active sessions: Settings > Security > Active Sessions
- Revoke access for departed team members immediately

## Compliance Certifications
- SOC 2 Type II
- ISO 27001
- GDPR compliant
- HIPAA compliant (Enterprise plan with BAA)

## Reporting a Security Issue
If you discover a security vulnerability, contact security@example.com immediately.
Do not disclose publicly until we have patched the issue (responsible disclosure).
Bug bounty program available — see security.example.com/bounty
