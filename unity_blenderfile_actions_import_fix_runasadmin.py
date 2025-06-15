#!/usr/bin/env python3
"""
Unity Blender Animation Fix Tool
Standalone script to fix bake_anim_use_all_actions=False bug in Unity's Blender importer
"""

import os
import sys
import shutil
import glob
from pathlib import Path

class UnityBlenderFixer:
    def __init__(self):
        self.unity_paths = []
        self.results = {
            'patched': 0,
            'already_fixed': 0,
            'errors': 0,
            'permission_errors': 0
        }
    
    def find_unity_installations(self):
        """Locate all Unity installations on the system"""
        possible_paths = [
            "C:/Program Files/Unity/Hub/Editor",
            "C:/Program Files (x86)/Unity/Hub/Editor", 
            "D:/Unity/Hub/Editor",
            "E:/Unity/Hub/Editor",
            "C:/Program Files/Unity",
            "C:/Program Files (x86)/Unity"
        ]
        
        for base_path in possible_paths:
            path = Path(base_path)
            if path.exists() and path.is_dir():
                for item in path.iterdir():
                    if item.is_dir():
                        tools_path = item / "Editor/Data/Tools"
                        if tools_path.exists():
                            self.unity_paths.append(item)
        
        # Remove duplicates
        self.unity_paths = list(set(self.unity_paths))
        return len(self.unity_paths) > 0
    
    def check_write_permission(self, file_path):
        """Test if we can write to the target file"""
        try:
            temp_file = file_path.parent / "temp_permission_test.tmp"
            temp_file.touch()
            temp_file.unlink()
            return True
        except (PermissionError, OSError):
            return False
    
    def create_backup(self, original_path):
        """Create backup of original file"""
        backup_path = Path(str(original_path) + ".backup")
        
        if backup_path.exists():
            return True, "Backup already exists"
        
        try:
            shutil.copy2(original_path, backup_path)
            return True, f"Backup created: {backup_path.name}"
        except Exception as e:
            return False, f"Backup failed: {str(e)}"
    
    def patch_blender_script(self, unity_path):
        """Patch the Unity-BlenderToFBX.py script in a specific Unity installation"""
        version_name = unity_path.name
        script_path = unity_path / "Editor/Data/Tools/Unity-BlenderToFBX.py"
        
        print(f"Processing Unity {version_name}...")
        
        if not script_path.exists():
            print(f"  Script not found: {script_path}")
            self.results['errors'] += 1
            return False
        
        # Read current content
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  Read error: {str(e)}")
            self.results['errors'] += 1
            return False
        
        # Check if already patched
        if "bake_anim_use_all_actions=False" not in content:
            print(f"  Already patched or different format")
            self.results['already_fixed'] += 1
            return True
        
        # Check write permissions
        if not self.check_write_permission(script_path):
            print(f"  Permission denied - administrator rights required")
            self.results['permission_errors'] += 1
            return False
        
        # Create backup
        backup_success, backup_msg = self.create_backup(script_path)
        if backup_success:
            print(f"  {backup_msg}")
        else:
            print(f"  Warning: {backup_msg}")
        
        # Apply patch
        try:
            patched_content = content.replace(
                "bake_anim_use_all_actions=False",
                "bake_anim_use_all_actions=True"
            )
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(patched_content)
            
            print(f"  Successfully patched!")
            self.results['patched'] += 1
            return True
            
        except Exception as e:
            print(f"  Write error: {str(e)}")
            self.results['errors'] += 1
            return False
    
    def attempt_admin_restart(self):
        """Try to restart the script with administrator privileges"""
        if sys.platform != "win32":
            return False
        
        try:
            import ctypes
            if ctypes.windll.shell32.IsUserAnAdmin():
                return False  # Already admin
            
            print("Attempting to restart with administrator privileges...")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            return True
        except Exception:
            return False
    
    def print_summary(self):
        """Print final results summary"""
        print("\n" + "="*50)
        print("RESULTS SUMMARY")
        print("="*50)
        print(f"Successfully patched:  {self.results['patched']}")
        print(f"Already fixed:         {self.results['already_fixed']}")
        print(f"Permission errors:     {self.results['permission_errors']}")
        print(f"Other errors:          {self.results['errors']}")
        
        total_processed = sum(self.results.values())
        if total_processed == 0:
            print("\nNo Unity installations processed.")
        elif self.results['patched'] > 0:
            print(f"\nSUCCESS! {self.results['patched']} Unity installation(s) fixed.")
            print("Your Blender files will now export all animations to Unity.")
        
        if self.results['permission_errors'] > 0:
            print(f"\nTo fix permission errors:")
            print("1. Close Unity and Unity Hub completely")
            print("2. Right-click this script and select 'Run as administrator'")
            print("3. Or run from administrator command prompt")
    
    def run(self):
        """Main execution flow"""
        print("Unity Blender Animation Fix Tool")
        print("Fixes bake_anim_use_all_actions=False bug in Unity's Blender importer")
        print("-" * 60)
        
        # Find Unity installations
        if not self.find_unity_installations():
            print("ERROR: No Unity installations found!")
            print("Make sure Unity is installed via Unity Hub.")
            input("Press Enter to exit...")
            return
        
        print(f"Found {len(self.unity_paths)} Unity installation(s):")
        for path in self.unity_paths:
            print(f"  {path.name}: {path}")
        print()
        
        # Process each Unity installation
        for unity_path in self.unity_paths:
            self.patch_blender_script(unity_path)
        
        # Show results
        self.print_summary()
        
        # Offer admin restart if needed
        if self.results['permission_errors'] > 0:
            user_input = input("\nAttempt to restart as administrator? (y/n): ").lower()
            if user_input == 'y':
                if self.attempt_admin_restart():
                    return  # Script restarted as admin
                else:
                    print("Failed to restart as administrator.")
        
        input("\nPress Enter to exit...")

def main():
    fixer = UnityBlenderFixer()
    fixer.run()

if __name__ == "__main__":
    main()