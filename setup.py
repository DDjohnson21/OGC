#!/usr/bin/env python3
"""
Setup script for Python Algorand Smart Contract System
"""

import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_virtual_environment():
    """Setup virtual environment if needed"""
    if not os.path.exists("venv"):
        print("🐍 Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            print("✅ Virtual environment created!")
            print("💡 To activate it:")
            print("   source venv/bin/activate  (Linux/Mac)")
            print("   venv\\Scripts\\activate     (Windows)")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    else:
        print("✅ Virtual environment already exists!")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Python Algorand Smart Contract System\n")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Setup virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("\n📋 Available Python Scripts:")
    print("1. Deploy contract: python simple_deploy.py")
    print("2. Interact with contract: python simple_deposit.py <command>")
    print("3. Manage wallet: python simple_wallet.py <command>")
    print("\n💡 Quick start:")
    print("  python simple_deploy.py")
    print("  python simple_deposit.py optin")
    print("  python simple_deposit.py deposit 2")
    print("  python simple_wallet.py balance")

if __name__ == "__main__":
    main()
