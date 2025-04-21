import os

from github import Github
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class GitHubLoader:
    def __init__(self):
        self.github = Github(os.getenv("GITHUB_TOKEN", ""))
        self.MAX_FILE_SIZE = 5 * 1024 * 1024  
        self.MAX_COMMITS = 50  
    
    def extract_repo_info(self, repo_url: str) -> Dict:
        """Extract owner and repo name from GitHub URL."""
        parts = repo_url.strip("/").split("/")
        owner = parts[-2]
        repo_name = parts[-1]
        return {"owner": owner, "repo_name": repo_name}
    
    def get_file_content(self, file_content) -> str:
        """Get decoded content of a file."""
        try:
            return file_content.decoded_content.decode()
        except:
            return ""
    
    def is_text_file(self, path: str) -> bool:
        """Check if file is likely to be a text file."""
        text_extensions = {
            # Source code files
            '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
            '.cs', '.go', '.rb', '.php', '.swift', '.kt', '.scala', '.rs', '.dart',
            # Web files
            '.html', '.css', '.scss', '.sass', '.less', '.xml', '.json', '.yaml', '.yml',
            # Configuration files
            '.env', '.config', '.ini', '.toml', '.properties',
            # Documentation
            '.md', '.txt', '.rst', '.adoc',
            # Scripts
            '.sh', '.bash', '.zsh', '.ps1', '.bat',
            # Build files
            '.gradle', '.pom', '.build', '.cmake', '.makefile',
            # Other text files
            '.gitignore', '.dockerignore', '.editorconfig', '.eslintrc', '.prettierrc'
        }
        return any(path.lower().endswith(ext) for ext in text_extensions)
    
    def get_repo_content(self, repo_url: str) -> Dict:
        """Fetch repository content including all files and commit history."""
        repo_info = self.extract_repo_info(repo_url)
        repo = self.github.get_repo(f"{repo_info['owner']}/{repo_info['repo_name']}")
        
        content = {
            "readme": "",
            "files": [],
            "commit_history": []
        }
        
        # Get README
        try:
            readme = repo.get_readme()
            content["readme"] = self.get_file_content(readme)
        except:
            pass
        
        # Get all files recursively
        def process_contents(contents, path=""):
            for item in contents:
                if item.type == "dir":
                    process_contents(repo.get_contents(item.path), item.path)
                else:
                    try:
                        # Skip binary files and large files
                        if item.size > self.MAX_FILE_SIZE:
                            print(f"Skipping large file: {item.path} ({item.size} bytes)")
                            continue
                        
                        # Skip non-text files
                        if not self.is_text_file(item.path):
                            print(f"Skipping non-text file: {item.path}")
                            continue
                            
                        file_content = self.get_file_content(item)
                        if file_content:  
                            content["files"].append({
                                "path": item.path,
                                "content": file_content,
                                "type": item.path.split(".")[-1] if "." in item.path else "unknown"
                            })
                    except Exception as e:
                        print(f"Error processing file {item.path}: {str(e)}")
                        continue
        
        process_contents(repo.get_contents(""))
        
        # Get commit history
        try:
            commits = list(repo.get_commits()[:self.MAX_COMMITS])
            for commit in commits:
                content["commit_history"].append({
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "date": commit.commit.author.date.isoformat(),
                    "author": commit.commit.author.name
                })
        except Exception as e:
            print(f"Error fetching commit history: {str(e)}")
        
        return content