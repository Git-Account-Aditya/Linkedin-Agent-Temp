from langchain_core.prompts import PromptTemplate

def trend_finalize_prompt():
    return PromptTemplate.from_template('''
        You are a social media manager.
        Based on the user's profile and trend analysis, select the best trend to use for post creation.

        Here is the profile information:
        {profile}

        Here is the trend analysis:
        {analysis}

        Return only the best trend for post creation.
    ''')

def content_creation_prompt():
    return PromptTemplate.from_template('''
        You are a social media manager.
        Based on the selected trend and analysis, create a LinkedIn post.

        Here is the selected trend:
        {trend}

        Here is the analysis:
        {analysis}

        Use analysis of the selected trend to inform your content creation.

        - Make sure the content is engaging and relevant to the audience.
        - Use a conversational tone and include relevant hashtags.
        - Make it concise and impactful.

        Return only the textual content for the LinkedIn post.
    ''')
