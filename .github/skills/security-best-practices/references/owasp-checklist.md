# OWASP Top 10 — Actionable Checklist

Use this checklist during code review and implementation. Each item maps to an OWASP category with concrete checks.

---

## A01: Broken Access Control

- [ ] Every endpoint enforces authentication before processing
- [ ] Authorization checks use deny-by-default (whitelist, not blacklist)
- [ ] Direct object references (IDs in URLs) are validated against the current user's permissions
- [ ] CORS is configured to allow only trusted origins
- [ ] Directory listing is disabled on web servers
- [ ] JWT tokens are validated for signature, expiry, and issuer
- [ ] Rate limiting is applied to sensitive endpoints (login, password reset)
- [ ] File uploads validate type, size, and are stored outside the web root

## A02: Cryptographic Failures

- [ ] Sensitive data is encrypted at rest (AES-256 or equivalent)
- [ ] TLS 1.2+ is enforced for all data in transit
- [ ] Passwords are hashed with bcrypt, scrypt, or argon2 (never MD5/SHA1)
- [ ] API keys and secrets are stored in environment variables or a vault — never in code
- [ ] Database connection strings use encrypted transport
- [ ] Old/weak ciphers are disabled in TLS configuration
- [ ] Sensitive data is not logged (passwords, tokens, PII)

## A03: Injection

- [ ] SQL queries use parameterized statements or ORM queries — never string concatenation
- [ ] User input in HTML output is escaped (XSS prevention)
- [ ] OS commands avoid shell interpolation — use subprocess with argument lists
- [ ] LDAP, XPath, and NoSQL queries use safe query builders
- [ ] File paths from user input are validated against an allowlist of base directories
- [ ] `eval()`, `exec()`, `Function()` are never used with user-controlled input
- [ ] Template engines use auto-escaping by default

## A04: Insecure Design

- [ ] Threat modeling is performed for new features
- [ ] Business logic has server-side validation (never trust client-only checks)
- [ ] Error messages do not reveal internal implementation details
- [ ] Multi-step workflows enforce proper state sequencing
- [ ] Resource limits protect against abuse (file size, request rate, memory)

## A05: Security Misconfiguration

- [ ] Default credentials are changed before deployment
- [ ] Debug mode / verbose error pages are disabled in production
- [ ] Stack traces are never exposed to end users
- [ ] Unnecessary HTTP headers are removed (Server, X-Powered-By)
- [ ] Security headers are set: CSP, X-Content-Type-Options, X-Frame-Options, HSTS
- [ ] Directory traversal is prevented in file-serving code
- [ ] Cloud storage buckets and IAM roles follow least-privilege

## A06: Vulnerable and Outdated Components

- [ ] Dependencies are pinned to specific versions (lockfile committed)
- [ ] `pip audit`, `npm audit`, or equivalent runs in CI
- [ ] No dependencies with known CVEs at CRITICAL or HIGH severity
- [ ] Unused dependencies are removed
- [ ] Container base images are updated regularly
- [ ] Dependency update PRs are reviewed within 7 days

## A07: Identification and Authentication Failures

- [ ] Multi-factor authentication is available for privileged accounts
- [ ] Login brute-force is mitigated (lockout, CAPTCHA, or rate limiting)
- [ ] Session tokens are regenerated after login
- [ ] Session tokens are invalidated on logout
- [ ] Password requirements enforce minimum length (12+ characters)
- [ ] Credential recovery uses secure tokens, not security questions

## A08: Software and Data Integrity Failures

- [ ] CI/CD pipelines validate artifact integrity (checksums, signatures)
- [ ] Deserialization of untrusted data uses safe libraries (never `pickle.loads` on user input)
- [ ] Auto-update mechanisms verify signatures before applying
- [ ] Code review is required before merging to protected branches

## A09: Security Logging and Monitoring Failures

- [ ] Authentication successes and failures are logged
- [ ] Authorization failures are logged with user context
- [ ] Logs include timestamp, user ID, action, and resource
- [ ] Logs do NOT contain passwords, tokens, or PII
- [ ] Log injection is prevented (sanitize newlines and control characters)
- [ ] Alerts are configured for anomalous patterns (spike in 403s, login failures)

## A10: Server-Side Request Forgery (SSRF)

- [ ] User-supplied URLs are validated against an allowlist of domains/IPs
- [ ] Internal network addresses (10.x, 172.16.x, 192.168.x, 169.254.x) are blocked
- [ ] URL redirects do not follow user-controlled destinations without validation
- [ ] DNS rebinding is mitigated (resolve hostname and validate IP before fetching)

---

## Quick Regex — Forbidden Patterns

Use these to scan code for common violations:

| Pattern | Risk |
|---------|------|
| `eval(` | Code injection |
| `exec(` | Code injection |
| `pickle.loads(` | Insecure deserialization |
| `yaml.load(` (without `Loader=SafeLoader`) | Insecure deserialization |
| `chmod 777` | World-writable permissions |
| `password.*=.*["']` | Hardcoded credential |
| `secret.*=.*["']` | Hardcoded secret |
| `api.key.*=.*["']` | Hardcoded API key |
| `DEBUG\s*=\s*True` | Debug mode in production |
| `verify\s*=\s*False` | Disabled SSL verification |
| `shell=True` | Shell injection risk (Python subprocess) |
| `innerHTML\s*=` | XSS risk (DOM manipulation) |
| `dangerouslySetInnerHTML` | XSS risk (React) |
