from langchain_core.prompts import PromptTemplate

def research_trends_prompt():
    return PromptTemplate.from_template('''
        You are an expert in analyzing trends. Given the following trend data, provide a comprehensive analysis:

        Trend Details: {trends}

        Your analysis should include key insights, potential implications, and any relevant context.
        analysis :
            - future growth potential
            - high engagement accounts
            - potential challenges and risks

        Return in Json format
        {
            "analysis":
                { 
                "trend": 
                    {
                    "future_growth_potential": "...",
                    "high_engagement_accounts": "...",
                    "potential_challenges_and_risks": "..."
                    }
                }
        }
    ''')