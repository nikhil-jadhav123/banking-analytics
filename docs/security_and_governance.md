# Security & Governance
- Secrets: Azure Key Vault; use Managed Identities where possible.
- Access: RBAC on storage containers; private endpoints for ADF/Databricks/Synapse.
- Data: Synthetic dataset only (no real PII). For real data, pseudonymize and applypolicies.
