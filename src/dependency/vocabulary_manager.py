# vocabulary_manager.py - Manage vocabulary relationships

import os
import re
import glob

class VocabularyManager:
    def __init__(self, workspace_path=None):
        """
        Initialize the vocabulary manager.
        
        Args:
            workspace_path (str): Path to workspace with OML files
        """
        self.workspace_path = workspace_path
        self.core_vocabularies = ["rdf", "rdfs", "xsd", "owl", "dc", "swrlb"]
        self.vocabularies = {}
        
        # Load vocabularies from workspace if provided
        if workspace_path:
            self.scan_workspace()
    
    def scan_workspace(self):
        """
        Scan workspace for OML files and extract vocabulary information.
        
        Returns:
            dict: Mapping of vocabulary aliases to their definitions
        """
        # Initialize with core vocabularies
        for vocab in self.core_vocabularies:
            self.vocabularies[vocab] = {
                'namespace': f"Core vocabulary: {vocab}",
                'alias': vocab,
                'path': None,
                'is_core': True
            }
            
        if not self.workspace_path:
            return self.vocabularies
            
        # Find all OML files
        oml_files = glob.glob(os.path.join(self.workspace_path, "**/*.oml"), recursive=True)
        
        for file_path in oml_files:
            with open(file_path, 'r') as file:
                content = file.read()
                
                # Extract namespace and alias
                namespace_match = re.search(r'vocabulary\s+<([^>]+)>\s+as\s+(\w+)', content)
                if namespace_match:
                    namespace = namespace_match.group(1)
                    alias = namespace_match.group(2)
                    
                    self.vocabularies[alias] = {
                        'namespace': namespace,
                        'alias': alias,
                        'path': file_path,
                        'is_core': False,
                        'extensions': []
                    }
                    
                    # Extract extensions
                    extension_matches = re.findall(r'extends\s+<([^>]+)>\s+as\s+(\w+)', content)
                    for ext_namespace, ext_alias in extension_matches:
                        self.vocabularies[alias]['extensions'].append(ext_alias)
                        
        return self.vocabularies
    
    def check_dependencies(self, query):
        """
        Check if query mentions vocabularies not in workspace.
        
        Args:
            query (str): User query
            
        Returns:
            tuple: (all_available, missing_vocabs)
        """
        # Extract vocabularies mentioned in query
        vocabs = self.extract_vocabs_from_query(query)
        
        if not vocabs:
            return True, []  # No vocabularies mentioned
            
        # Check which vocabularies are missing
        available_aliases = set(self.vocabularies.keys())
        missing_vocabs = [v for v in vocabs if v not in available_aliases]
        
        return len(missing_vocabs) == 0, missing_vocabs
    
    def extract_vocabs_from_query(self, query):
        """
        Extract vocabulary names from query.
        
        Args:
            query (str): User query
            
        Returns:
            list: Vocabulary names mentioned
        """
        # Look for "extends" pattern
        extends_match = re.search(r'extends\s+(?:the\s+)?([^\.]+)', query, re.IGNORECASE)
        if not extends_match:
            return []  # No extensions mentioned
            
        mentioned_vocabs = extends_match.group(1)
        
        # Extract vocabulary names, ignoring common words
        skip_words = ['and', 'or', 'the', 'vocabularies']
        vocab_names = [v.strip().lower() for v in re.split(r'[,\s]+', mentioned_vocabs) 
                      if v.strip().lower() not in skip_words and v.strip()]
                      
        return vocab_names
    
    def get_allowed_extensions(self):
        """
        Get list of allowed vocabulary extensions.
        
        Returns:
            list: Available vocabulary aliases
        """
        return list(self.vocabularies.keys())
    
    def format_vocabulary_restrictions(self):
        """
        Format vocabulary restrictions for prompt.
        
        Returns:
            str: Formatted restrictions
        """
        allowed = self.get_allowed_extensions()
        
        # Format as instruction
        restrictions = f"Your OML code MUST ONLY extend the following vocabularies:\n"
        restrictions += ", ".join(allowed)
        restrictions += "\n\nDo NOT introduce new vocabulary extensions that are not in this list."
        
        return restrictions
    
    def extract_dependencies_from_build_files(self):
        """
        Extract dependencies from build.gradle or .yml files.
        
        Returns:
            list: External dependencies
        """
        if not self.workspace_path:
            return []
            
        dependencies = []
        
        # Check build.gradle files
        gradle_files = glob.glob(os.path.join(self.workspace_path, "**/build.gradle"), recursive=True)
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
        yml_files = glob.glob(os.path.join(self.workspace_path, "**/*.yml"), recursive=True)
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
