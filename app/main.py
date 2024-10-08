from fastapi import FastAPI, Query
import requests
import xml.etree.ElementTree as ET
from app.core.config import logger_config

logger = logger_config(__name__)

app = FastAPI(
    # servers=[
    #     {
    #         "url": "https://url.io",
    #         "description": "Testing server of the API"
    #     }
    # ]
)


@app.get("/fetch-jobs/")
def fetch_jobs(
    q: str = Query(..., description="Keyword for job search"),
    count: int = Query(10, description="Number of jobs to retrieve"),
    sort: str = Query("recency", description="Sort order of the jobs")
):
    # Construct the dynamic RSS feed URL
    base_url = "https://www.upwork.com/ab/feed/jobs/rss?"

    paging_param = f"paging=0%3B{count}"
    keyword_param = f"&q={q}"
    sort_param = f"&sort={sort}"
    
    security_token = "&securityToken="
    user_uid = "&userUid="
    org_uid = "&orgUid="

    url = f"{base_url}{paging_param}{keyword_param}{
        sort_param}{security_token}{user_uid}{org_uid}"

    logger.info(f"Fetching jobs with URL: {url}")

    # Fetch the RSS feed
    response = requests.get(url)

    # Parse the XML content
    root = ET.fromstring(response.content)

    jobs = []
    for item in root.findall(".//item"):
        job = {
            "title": item.find("title").text,
            "link": item.find("link").text,
            "description": item.find("description").text,
            "pubDate": item.find("pubDate").text
        }
        jobs.append(job)

    # Sort jobs by publication date to ensure most recent first
    jobs.sort(key=lambda x: x['pubDate'], reverse=True)

    return {"jobs": jobs}


# Policy Router for API Policies
@app.get("/policy", include_in_schema=False)
def get_policy():
    """
    Get the policy information for the API.
    """
    policy_info = {
        "policy": "This Microservice is for auto lead generation purposes only.",
        "contact": "mr.junaidshaukat@gmail.com",
        "email": "https://www.linkedin.com/in/mrjunaid/",
        "license": "Commercial",
    }
    return policy_info
