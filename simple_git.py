#!/usr/bin/env python3
import os
import subprocess

# Change to project directory
os.chdir('/workspaces/RasfatulPescarului-production')

print("🚀 Starting Git operations...")

# Git add
print("📁 Adding files...")
result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
print(f"Git add result: {result.returncode}")
if result.stderr:
    print(f"Add stderr: {result.stderr}")

# Git commit
print("💬 Committing...")
commit_msg = "🗺️ Fix map functionality and CSP for Leaflet - Updated CSP to allow unpkg.com, fixed hero.webp references, added AdSense content"
result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
print(f"Git commit result: {result.returncode}")
print(f"Commit stdout: {result.stdout}")
if result.stderr:
    print(f"Commit stderr: {result.stderr}")

# Git push
print("🚀 Pushing...")
result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print(f"Git push result: {result.returncode}")
print(f"Push stdout: {result.stdout}")
if result.stderr:
    print(f"Push stderr: {result.stderr}")

print("✅ Git operations complete!")
