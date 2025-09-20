# Databricks: set credentials in a secret scope first (recommended)
# Replace <storageacct> and <tenant_id>/<sp_app_id>/<sp_secret> via Secrets.
storage_acct = "<storageacct>"
container_bronze = "bronze"
container_silver = "silver"
configs = {
f"fs.azure.account.auth.type": "OAuth",
f"fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
f"fs.azure.account.oauth2.client.id": dbutils.secrets.get("kv-scope", "sp-app-id"),
f"fs.azure.account.oauth2.client.secret": dbutils.secrets.get("kv-scope", "sp-sec"),
f"fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{dbutils.secrets.get('kv-scope', 'tenant-id')}/oauth2/token"
}

def mount(container):
    mount_point = f"/mnt/{container}"
    source = f"abfss://{container}@{storage_acct}.dfs.core.windows.net/"
    if any(m.mountPoint == mount_point for m in dbutils.fs.mounts()):
        print(f"{mount_point} already mounted.")
        return
    dbutils.fs.mount(
        source=source,
        mount_point=mount_point,
        extra_configs=configs
    )
    print(f"Mounted {source} to {mount_point}")

# Call the function for both containers
mount(container_bronze)
mount(container_silver)
