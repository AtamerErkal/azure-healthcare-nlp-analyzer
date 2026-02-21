from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv

class KeyVaultConfig:
    """
    Secure credential management with Azure Key Vault
    Falls back to .env if Key Vault unavailable (development mode)
    """
    
    def __init__(self):
        load_dotenv()
        
        # Try Key Vault first
        vault_url = os.getenv("KEY_VAULT_URL", "https://kv-healthcare-ai102.vault.azure.net/")
        
        try:
            credential = DefaultAzureCredential()
            self.kv_client = SecretClient(vault_url=vault_url, credential=credential)
            
            # Test connection
            _ = self.kv_client.list_properties_of_secrets(max_page_size=1)
            
            self.use_keyvault = True
            print("✅ Using Azure Key Vault for credentials")
        
        except Exception as e:
            self.use_keyvault = False
            print(f"⚠️  Key Vault unavailable, using .env: {str(e)[:50]}")
    
    def get_credential(self, key_name: str) -> str:
        """
        Get credential from Key Vault or .env
        
        Args:
            key_name: Name of the secret (e.g., 'LANGUAGE-KEY')
        
        Returns:
            Secret value
        """
        # Try Key Vault
        if self.use_keyvault:
            try:
                secret = self.kv_client.get_secret(key_name)
                return secret.value
            except Exception as e:
                print(f"⚠️  Key Vault fetch failed for {key_name}: {str(e)[:50]}")
        
        # Fallback to .env
        env_value = os.getenv(key_name.replace("-", "_"))  # LANGUAGE-KEY → LANGUAGE_KEY
        if not env_value:
            env_value = os.getenv(key_name)  # Try original format
        
        return env_value


# Quick test
if __name__ == "__main__":
    kv = KeyVaultConfig()
    
    endpoint = kv.get_credential("LANGUAGE-ENDPOINT")
    key = kv.get_credential("LANGUAGE-KEY")
    
    if endpoint and key:
        print(f"✅ Endpoint: {endpoint[:30]}...")
        print(f"✅ Key: {key[:10]}...{key[-5:]}")
    else:
        print("❌ Credentials not found")