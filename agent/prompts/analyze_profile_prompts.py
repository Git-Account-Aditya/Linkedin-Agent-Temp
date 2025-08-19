from langchain_core.prompts import PromptTemplate

def profile_activity_level_prompt() -> PromptTemplate:
    return PromptTemplate.from_template("""
        Based on the user's recent activity, determine their LinkedIn activity level.

        Recent Post Time: {recent_post_time}
        Number of Posts: {no_of_posts}

        Activity Level for Recent post:
        - (8 - 10): Recent post within the last 7 days (High)
        - (4 - 7): Recent post within the last 14 days (Medium)
        - (1 - 3): No recent posts (Low)

        Activity Level for Number of post:
        - (8 - 10): More than 10 posts (High)
        - (4 - 7): 5 to 10 posts (Medium)
        - (0 - 3): Less than 5 posts (Low)

        Activity Level = 0.6 * [activity level for recent post] + 0.4 * [activity level for no of post]

        Only return Activity Level, no extra text.
    """)


def profile_keyword_analysis_prompt() -> PromptTemplate:
    return PromptTemplate.from_template("""
        Analyze the user's LinkedIn profile and extract the top keywords from their skills and experience.

        Skills: {skills}
        Experience: {experience}

        Only return the top keywords, no extra text.
    """)