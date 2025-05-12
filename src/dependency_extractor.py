# dependency_extractor.py - Extract vocabulary dependencies

import re
import os
import glob

class DependencyExtractor:
    def __init__(self, core_vocabularies=None):
        """
        Initialize the dependency extractor.
        
        Args:
            core_vocabularies (list): List of core vocabulary aliases
        """
        self.core_vocabularies = core_vocabularies or ["rdf", "rdfs", "xsd", "owl", "dc", "swrlb"]
        
    def extract_from_workspace(self, workspace_path):
        """
        Extract vocabulary dependencies from a workspace.
        
        Args:
            workspace_path (str): Path to workspace
            
        Returns:
            dict: Mapping of vocabulary aliases to their definitions
        """
        dependencies = {}
        
        # Add core vocabularies
        for vocab in self.core_vocabularies:
            dependencies[vocab] = f"Core vocabulary: {vocab}"
            
        # Find all OML files
        oml_files = glob.glob(os.path.join(workspace_path, "**/*.oml"), recursive=True)
        
        for file_path in oml_files:
            with open(file_path, 'r') as file:
                content = file.read()
                
                # Extract namespace and alias
                namespace_match = re.search(r'vocabulary\s+<([^>]+)>\s+as\s+(\w+)', content)
                if namespace_match:
                    namespace = namespace_match.group(1)
                    alias = namespace_match.group(2)
                    dependencies[alias] = f"Vocabulary {alias} defined at {namespace}"
                    
                # Extract extensions
                extension_matches = re.findall(r'extends\s+<([^>]+)>\s+as\s+(\w+)', content)
                for ext_namespace, ext_alias in extension_matches:
                    if ext_alias not in dependencies:
                        dependencies[ext_alias] = f"External vocabulary {ext_alias} from {ext_namespace}"
                        
        return dependencies
    
    def extract_from_build_files(self, workspace_path):
        """
        Extract dependencies from build.gradle or .yml files.
        
        Args:
            workspace_path (str): Path to workspace
            
        Returns:
            list: External dependencies
        """
        dependencies = []
        
        # Check build.gradle files
        gradle_files = glob.glob(os.path.join(workspace_path, "**/build.gradle"), recursive=True)
        for file_path in gradle_files:
            with open(file_path, 'r') as file:
                content = file.read()
                
                # Extract dependencies
                dep_matches = re.findall(r'dependencies\s*{([^}]*)}', content, re.DOTALL)
                for dep_block in dep_matches:
                    matches = re.findall(r'[\'"]([^:\'"]+):([^:\'"]+):([^\'"]+)[\'"]', dep_block)
                    for group, name, version in matches:
                        dependencies.append(f"{group}:{name}:{version}")
                        
        # Check .yml files
        yml_files = glob.glob(os.path.join(workspace_path, "**/*.yml"), recursive=True)
        for file_path in yml_files:
            with open(file_path, 'r') as file:
                content = file.read()
                
                # Extract dependencies (simple pattern)
                dep_matches = re.findall(r'dependencies:\s*([^}]*)', content, re.DOTALL)
                for dep_block in dep_matches:
                    matches = re.findall(r'-\s*([^\s:]+):([^\s:]+):([^\s]+)', dep_block)
                    for group, name, version in matches:
                        dependencies.append(f"{group}:{name}:{version}")
                        
        return dependencies
    
    def check_vocabulary_extensions(self, query, available_vocabularies):
        """
        Check if query contains extensions not available in workspace.
        
        Args:
            query (str): User query
            available_vocabularies (dict): Available vocabularies
            
        Returns:
            tuple: (bool, list) - (all available, missing vocabularies)
        """
        # Extract vocabularies mentioned in query after "extends"
        extends_match = re.search(r'extends\s+(?:the\s+)?([^\.]+)', query, re.IGNORECASE)
        if not extends_match:
            return True, []  # No extensions mentioned
            
        mentioned_vocabs = extends_match.group(1)
        
        # Extract vocabulary names, ignoring common words
        skip_words = ['and', 'or', 'the', 'vocabularies']
        vocab_names = [v.strip().lower() for v in re.split(r'[,\s]+', mentioned_vocabs) 
                      if v.strip().lower() not in skip_words and v.strip()]
        
        # Check if all mentioned vocabularies are available
        available_vocabs_lower = [v.lower() for v in available_vocabularies.keys()]
        missing_vocabs = [v for v in vocab_names if v not in available_vocabs_lower]
        
        return len(missing_vocabs) == 0, missing_vocabs
