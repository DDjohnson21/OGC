#!/usr/bin/env python3
"""Build script for OGC Vault contract"""

import os
from smart_contracts.ogc_vault.contract import app

def main():
    # Create artifacts directory
    artifacts_dir = "artifacts/ogc_vault"
    os.makedirs(artifacts_dir, exist_ok=True)
    
    # Build and export the contract
    print("Building OGC Vault contract...")
    app.build().export(artifacts_dir)
    print(f"Contract artifacts exported to {artifacts_dir}")
    
    # List generated files
    print("\nGenerated files:")
    for file in os.listdir(artifacts_dir):
        print(f"  {file}")

if __name__ == "__main__":
    main()