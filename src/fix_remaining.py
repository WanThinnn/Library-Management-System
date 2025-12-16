#!/usr/bin/env python3
import os
import re

def fix_remaining_darkmode(filepath):
    """Fix remaining dark mode issues in HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Fix table rows with bg-white or even:bg-gray-50
        content = re.sub(
            r'\bbg-gray-50\b(?!.*?dark:bg)',
            'bg-gray-50 dark:bg-gray-700',
            content
        )
        
        # Fix table headers with bg-blue-600
        content = re.sub(
            r'\bbg-blue-600\b(?!.*?dark:bg)',
            'bg-blue-600 dark:bg-blue-700',
            content
        )
        
        # Fix placeholder text colors
        content = re.sub(
            r'\bplaceholder-gray-400\b(?!.*?dark:placeholder)',
            'placeholder-gray-400 dark:placeholder-gray-500',
            content
        )
        
        # Fix bg-gray-100
        content = re.sub(
            r'\bbg-gray-100\b(?!.*?dark:bg)(?!.*?dark:border)',
            'bg-gray-100 dark:bg-gray-700',
            content
        )
        
        # Fix bg-blue-50
        content = re.sub(
            r'\bbg-blue-50\b(?!.*?dark:bg)',
            'bg-blue-50 dark:bg-blue-900',
            content
        )
        
        # Fix bg-red-50
        content = re.sub(
            r'\bbg-red-50\b(?!.*?dark:bg)',
            'bg-red-50 dark:bg-red-900',
            content
        )
        
        # Fix bg-yellow-50
        content = re.sub(
            r'\bbg-yellow-50\b(?!.*?dark:bg)',
            'bg-yellow-50 dark:bg-yellow-900',
            content
        )
        
        # Fix bg-green-50
        content = re.sub(
            r'\bbg-green-50\b(?!.*?dark:bg)',
            'bg-green-50 dark:bg-green-900',
            content
        )
        
        # Fix bg-purple-50
        content = re.sub(
            r'\bbg-purple-50\b(?!.*?dark:bg)',
            'bg-purple-50 dark:bg-purple-900',
            content
        )
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"✗ Error: {filepath} - {e}")
        return False

def main():
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    count = 0
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if fix_remaining_darkmode(filepath):
                    count += 1
    
    print(f"\n✅ Fixed {count} files")

if __name__ == '__main__':
    main()
