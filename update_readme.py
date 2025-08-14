import os
import requests
import sys

def get_env_var(var_name):
    """Gets an environment variable or exits if it's not set."""
    value = os.getenv(var_name)
    if not value:
        print(f"Error: Environment variable {var_name} is not set.")
        sys.exit(1)
    return value

def get_repos(org_name, token):
    """Gets the list of public repositories for an organization."""
    url = f"https://api.github.com/orgs/{org_name}/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

def generate_readme(org_name, repos):
    """Generates the README content."""
    readme = f"# Welcome to the {org_name} organization!\n\n"
    readme += "This is a list of our public repositories:\n\n"
    readme += "| Repository | Description |\n"
    readme += "|------------|-------------|\n"
    for repo in sorted(repos, key=lambda r: r['name']):
        if not repo['private']:
            repo_name = repo['name']
            repo_desc = repo['description'] if repo['description'] else "No description provided."
            readme += f"| [{repo_name}]({repo['html_url']}) | {repo_desc} |\n"

    readme += "\n\n---\n*This README is automatically generated every week.*"
    return readme

def main():
    """Main function."""
    try:
        token = get_env_var("GITHUB_TOKEN")
        repo_full_name = get_env_var("GITHUB_REPOSITORY")
        org_name = repo_full_name.split('/')[0]
        output_filepath = "profile/README.md"

        repos = get_repos(org_name, token)
        readme_content = generate_readme(org_name, repos)

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_filepath)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_filepath, "w") as f:
            f.write(readme_content)

        print(f"{output_filepath} updated successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
