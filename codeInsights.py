import openai
import requests

openai.api_key = 'your_api_key'


def get_pr_diff(github_repo, pr_number):
    url = f"https://api.github.com/repos/{github_repo}/pulls/{pr_number}/files"

    response = requests.get(url)

    if response.status_code == 200:
        pr_files_data = response.json()
        diffs = []
        for file in pr_files_data:

            if 'patch' in file:
                diffs.append(f"File: {file['filename']}\n{file['patch']}\n")
        return diffs
    else:
        raise Exception(f"Error fetching PR diff for PR {pr_number}: {response.status_code}")


def analyze_pr_with_openai(feature_description, github_repo, pr_number):
    try:

        diffs = get_pr_diff(github_repo, pr_number)

        messages = [
            {"role": "system", "content": "You are an AI that analyzes code changes and suggests improvements."},
            {"role": "user", "content": f"""
                Feature Description:
                {feature_description}

                GitHub PR Diffs:
                {''.join(diffs)}

                Please analyze the code changes in this PR and provide:
                1. Which parts of the system might be impacted by this feature?
                2. Are there any missing tests or edge cases to consider?
                3. Do you see any potential bugs or issues with the implementation?
                4. Any suggestions for code improvements or refactoring?
            """}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            temperature=0.5
        )

        ai_response = response['choices'][0]['message']['content'].strip()
        return ai_response

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    github_repo = "suryabalan/assessment"
    pr_number = 1

    feature_description = """
    The feature is to fetch account details for given id
    """

    analysis = analyze_pr_with_openai(feature_description, github_repo, pr_number)

    print("AI's Analysis of PR:")
    print(analysis)
