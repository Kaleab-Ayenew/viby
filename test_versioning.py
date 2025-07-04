#!/usr/bin/env python3
"""
Test script to verify automated versioning is working correctly
"""
import subprocess
import sys

def run_command(cmd):
    """Run a command and return its output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def test_versioning():
    """Test the versioning setup"""
    print("🔍 Testing Automated Versioning Setup\n")
    
    # Test 1: Check if we can import and get version
    print("1. Testing version import...")
    try:
        import vity
        print(f"   ✅ vity.__version__ = {vity.__version__}")
        

    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        print("   💡 Try: pip install -e .")
        return False
    
    # Test 2: Check git tags
    print("\n2. Testing git tag detection...")
    stdout, stderr, code = run_command("git tag --list 'v*' | tail -5")
    if code == 0 and stdout:
        print(f"   ✅ Found recent tags: {stdout.replace(chr(10), ', ')}")
    else:
        print("   ℹ️  No version tags found (this is normal for new repos)")
        print("   💡 Create a tag with: git tag v1.0.0")
    
    # Test 3: Check build system
    print("\n3. Testing build system...")
    stdout, stderr, code = run_command("python -c 'import hatch_vcs; print(\"hatch-vcs available\")'")
    if code == 0:
        print("   ✅ hatch-vcs is available")
    else:
        print("   ❌ hatch-vcs not found")
        print("   💡 Install with: pip install hatch-vcs")
    
    # Test 4: Test CLI versions
    print("\n4. Testing CLI version commands...")
    
    # Test vity CLI
    stdout, stderr, code = run_command("python -m vity.cli --version")
    if code == 0:
        print(f"   ✅ vity CLI version: {stdout}")
    else:
        print(f"   ❌ vity CLI version failed: {stderr}")
    
    # Test vity CLI
    stdout, stderr, code = run_command("python -m vity.cli --version")
    if code == 0:
        print(f"   ✅ vity CLI version: {stdout}")
    else:
        print(f"   ❌ vity CLI version failed: {stderr}")
    
    print("\n🎉 Testing complete!")
    print("\nNext steps:")
    print("1. Create a version tag: git tag v1.0.0")
    print("2. Push the tag: git push origin v1.0.0")
    print("3. Watch GitHub Actions build and release automatically!")
    
    return True

if __name__ == "__main__":
    success = test_versioning()
    sys.exit(0 if success else 1) 