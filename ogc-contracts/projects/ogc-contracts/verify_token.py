#!/usr/bin/env python3
"""Verify OGC token exists"""

from beaker import sandbox

def verify_token():
    print("🔍 Verifying OGC Token...")
    
    algod = sandbox.get_algod_client()
    asset_id = 1033  # From create_ogc_token.py output
    
    try:
        # Get asset info
        asset_info = algod.asset_info(asset_id)
        params = asset_info["params"]
        
        print(f"✅ OGC Token Found!")
        print(f"   Asset ID: {asset_id}")
        print(f"   Name: {params['name']}")
        print(f"   Unit: {params['unit-name']}")
        print(f"   Total: {params['total']:,}")
        print(f"   Decimals: {params['decimals']}")
        print(f"   Creator: {params['creator']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Token not found: {e}")
        return False

if __name__ == "__main__":
    success = verify_token()
    print(f"🏁 Verification {'PASSED' if success else 'FAILED'}")