from resume_data import EXPERIENCES, PROJECTS, SKILLS
from format_latex import format_experience, format_project, format_latex, format_link
import os
from openai import OpenAI
import dotenv
import json
dotenv.load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


# load the job description
with open("job_description.txt", "r") as f:
    job_description = f.read()

# extract specific details from the job description
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": f"You are an expert in resume writing, specifically in the tech industry.\n\nCarefully read the following job description:\n\n{job_description}\n\nList all of the following details that are important to highlight when writing a resume for this position. \n\nJob Title\n\nRequired Technical Skills\n\nRequired Soft Skills\n\nDesired Technical Skills\n\nDesired Soft Skills"
            }
        ]
        }
    ],
    temperature=0.9,
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
        "type": "json_schema",
        "json_schema": {
        "name": "job_details",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "job_title": {
                    "type": "string",
                    "description": "The job title of the position."
                },
                "responsibilities": {
                    "type": "array",
                    "description": "The responsibilities of the position.",
                    "items": {
                        "type": "string",
                        "description": "A responsibility of the position."
                    }
                },
                "required_technical_skills": {
                    "type": "array",
                    "description": "The required technical skills for the position.",
                    "items": {
                        "type": "string",
                        "description": "A required technical skill for the position."
                    }
                },
                "required_soft_skills": {
                    "type": "array",
                    "description": "The required soft skills for the position.",
                    "items": {
                        "type": "string",
                        "description": "A required soft skill for the position."
                    }
                },
                "desired_technical_skills": {
                    "type": "array",
                    "description": "The desired technical skills for the position.",
                    "items": {
                        "type": "string",
                        "description": "A desired technical skill for the position."
                    }
                },
                "desired_soft_skills": {
                    "type": "array",
                    "description": "The desired soft skills for the position.",
                    "items": {
                        "type": "string",
                        "description": "A desired soft skill for the position."
                    }
                }
            },
            "required": ["job_title", "responsibilities", "required_technical_skills", "required_soft_skills", "desired_technical_skills", "desired_soft_skills"],
            "additionalProperties": False
        }
    }
    }
)

response_json = response.choices[0].message.content
response_dict = json.loads(response_json)
job_skills = response_dict['required_technical_skills'] + response_dict['required_soft_skills'] + response_dict['desired_technical_skills'] + response_dict['desired_soft_skills']
job_details = f"""
Job Title: {response_dict["job_title"]}
Responsibilities: {', '.join(response_dict["responsibilities"])}
Required Technical Skills: {", ".join(response_dict["required_technical_skills"])}
Required Soft Skills: {', '.join(response_dict["required_soft_skills"])}
Desired Technical Skills: {', '.join(response_dict["desired_technical_skills"])}
Desired Soft Skills: {', '.join(response_dict["desired_soft_skills"])}
"""

print("-- THE JOB DESCRIPTION --")
print(job_details)



print("-- PROCESSING EXPERIENCES --")

experiences = []

for experience in EXPERIENCES:
    # get the most relevant job title
    job_title = None
    if len(experience["position"]) > 1:

        job_title_options = experience["position"]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": "You are an expert in resume writing, specifically in the tech industry.\n\nCarefully read the following job description:\n\n{job_details}\n\nWhich of the following job title describes the position best for the given job description? \n\n" + '\n'.join(job_title_options)
                    }
                ]
                }
            ],
            temperature=0.9,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                "name": "job_title",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "most_relevant_title": {
                            "type": "string",
                            "description": "The most relevant job title from the list of job titles.",
                                "enum" : job_title_options
                            }
                        },
                        "required": ["most_relevant_title"],
                        "additionalProperties": False
                        }
                    }
                }
        )
        response_json = response.choices[0].message.content
        response_dict = json.loads(response_json)
        job_title = response_dict["most_relevant_title"]
    else:
        job_title = experience["position"][0]

    print(f"Writing points for {job_title}...")

    points_options = "\n".join(f"{i + 1}: {point}" for i, point in enumerate(experience["points"]))
  
    # get the relevant points
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": f"You are an expert in resume writing, specifically in the tech industry.\n\nCarefully read the following job description:\n\n{job_details}\n\nFor each point describing my experience as a {job_title} at {experience['company']}, output how relevant it is to the job description from 1 (not relevant at all) to 10 (exactly matches the job description). \n\n {points_options}"
            }
        ]
        }
    ],
    temperature=0.9,
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
        "type": "json_schema",
        "json_schema": {
        "name": "experience_points",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "points": {
                    "type": "array",
                    "description": f"A collection of points describing my experience as a {job_title} at {experience['company']}.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "index": {
                                "type": "integer",
                                "description": f"The index of the point in the list of points from the job description (ranging from 1 to {len(experience['points'])})",
                                "enum" : list(range(1, len(experience['points']) + 1))
                            },
                            "relevance_score": {
                                "type": "integer",
                                "description": "The relevance score of the point to the job description from 1 (not relevant at all) to 10 (exactly matches the job description).",
                                "enum" : list(range(1, 11))
                            },
                        },
                        "required": ["relevance_score", "index"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["points"],
            "additionalProperties": False
        }
    }
    }
)

    # conver json to dict
    response_json = response.choices[0].message.content
    response_dict = json.loads(response_json)
    points = response_dict["points"]
    experiences.append({
        "job_title": job_title,
        "company": experience["company"],
        "date": experience["date"],
        "location": experience["location"],
        "points": [{
            "relevance_score": point["relevance_score"],
            "point": experience["points"][point["index"] - 1]
        } for point in points]
    })
    print("\n".join([f"{point['relevance_score']}: {point['point']}" for point in experiences[-1]["points"]]))



print("-- PROCESSING PROJECTS --")
project_options = "\n".join([f"{i + 1}: {project['name']} ({', '.join(project['points'])})" for i, project in enumerate(PROJECTS)])
response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[
    {
    "role": "system",
    "content": [
        {
        "type": "text",
        "text": f"You are an expert in resume writing, specifically in the tech industry.\n\nCarefully read the following job description:\n\n{job_details}\n\nFor each project, output how relevant it is to the job description from 1 (not relevant at all) to 10 (exactly matches the job description). \n\n {project_options}"
        }
    ]
    }
],
temperature=0.9,
max_tokens=2048,
top_p=1,
frequency_penalty=0,
presence_penalty=0,
response_format={
    "type": "json_schema",
    "json_schema": {
    "name": "projects",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "projects": {
                "type": "array",
                "description": "A collection of relevant projects with their relevance scores.",
                "items": {
                    "type": "object",
                    "properties": {
                        "index": {
                            "type": "integer",
                            "enum": list(range(1, len(PROJECTS) + 1)),
                            "description": f"The index of the point in the list of points from the job description (ranging from 1 to {len(PROJECTS)})."
                        },
                        "relevant_skills" : {
                            "type": "array",
                            "description": "The relevant skills related to the project.",
                            "items": {
                                "type": "string",
                                "description": "A relevant skill related to the project.",
                                "enum" : SKILLS
                            }
                        },
                        "relevance_score": {
                            "type": "integer",
                            "description": "The relevance score of the project to the job description from 1 (not relevant at all) to 10 (exactly matches the job description)."
                        }
                    },
                    "required": ["index", "relevance_score", "relevant_skills"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["projects"],
        "additionalProperties": False
    }
}
}
)


response_json = response.choices[0].message.content
response_dict = json.loads(response_json)
projects = []
for project_result in response_dict["projects"]:
    project_data = PROJECTS[project_result["index"] - 1]
    projects.append({
        "name": project_data["name"],
        "link": project_data["link"] if "link" in project_data else None,
        "date": project_data["date"],
        "points": project_data["points"],
        "skills": project_result["relevant_skills"],
        "relevance_score": project_result["relevance_score"]
    })
    print(f"{project_result['relevance_score']}: {project_data['name']} ({', '.join(project_result['relevant_skills'])})")


print("-- PROCESSING SKILLS --")
# get the most relevant skills
response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[
    {
    "role": "system",
    "content": [
        {
        "type": "text",
        "text": f"You are an expert in resume writing, specifically in the tech industry.\n\nCarefully read the following job description:\n\n{job_details}\n\nList, which of the following skills are most relevant to the job description. Return the skills in a list sorted from most relevant to least relevant."
        }
    ]
    }
],
temperature=0.9,
max_tokens=2048,
top_p=1,
frequency_penalty=0,
presence_penalty=0,
response_format={
    "type": "json_schema",
    "json_schema": {
    "name": "relevant_skills",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "relevant_skills": {
                "type": "array",
                "description": "A collection of relevant skills.",
                "items": {
                    "type": "string",
                    "description": "Relevant skill",
                    "enum" : SKILLS
                }
            }
        },
        "required": ["relevant_skills"],
        "additionalProperties": False
    }
    }
}
)

response_json = response.choices[0].message.content
response_dict = json.loads(response_json)
result_skills = response_dict["relevant_skills"]

print(', '.join(result_skills))

print("-- WRITING RESUME --")

MAX_LINES = 32
# each experience point is worth 1 point
# each project is worth 2 points

items = []
for i, experience in enumerate(experiences):
    for j, point in enumerate(experience["points"]):
        items.append({
            "type": "experience_point",
            "experience_index": i,
            "point_index": j,
            "relevance_score": experience["points"][j]["relevance_score"]
        })
for i, project in enumerate(projects):
    items.append({
        "type": "project",
        "project_index": i,
        "relevance_score": project["relevance_score"]
    })


# sort the items by relevance score
items_sorted = sorted(items, key=lambda x: x["relevance_score"], reverse=True)

lines = 0
has_experience = False
has_project = False
EXPERIENCE_HEADER_LINES = 1
EXPERIENCE_TITLE_LINES = 1
EXPERIENCE_POINT_LINES = 2
PROJECT_HEADER_LINES = 1
PROJECT_LINES = 3

# get the chosen experiences_points and projects and skills
chosen_experiences = {}
chosen_projects = []
for item in items_sorted:
    if item["type"] == "experience_point":
        if not has_experience:
            lines += EXPERIENCE_HEADER_LINES
            has_experience = True
        chosen_experience = experiences[item["experience_index"]]
        chosen_point = chosen_experience["points"][item["point_index"]]
        print(f"Adding Point {chosen_point['point'][:20]}... to {chosen_experience['job_title']}")
        lines += EXPERIENCE_POINT_LINES
        if chosen_experience["job_title"] not in chosen_experiences:
            lines += EXPERIENCE_TITLE_LINES
            chosen_experiences[chosen_experience["job_title"]] = ({
                "job_title": chosen_experience["job_title"],
                "company": chosen_experience["company"],
                "date": chosen_experience["date"],
                "location": chosen_experience["location"],
                "points": [chosen_point["point"]]
            })
        else:
            chosen_experiences[chosen_experience["job_title"]]["points"].append(chosen_point["point"])
    elif item["type"] == "project":
        if not has_project:
            lines += PROJECT_HEADER_LINES
            has_project = True
        chosen_project = projects[item["project_index"]]
        print(f"Adding Project {chosen_project['name'][:20]}")
        lines += PROJECT_LINES
        chosen_projects.append({
            "name": chosen_project["name"],
            "link": chosen_project["link"] if "link" in chosen_project and chosen_project["link"] is not None else None,
            "date": chosen_project["date"],
            "points": chosen_project["points"],
            "skills": chosen_project["skills"],
        })

    if lines > MAX_LINES:
        print("Max lines reached..")
        break

chosen_experiences = list(chosen_experiences.values())


MAX_CHARACTERS = 220
chosen_skills = []
for skill in result_skills:
    if len(chosen_skills) + len(skill) + 1 <= MAX_CHARACTERS:
        chosen_skills.append(skill)
    else:
        break

formatted_experiences = [format_experience(position=experience["job_title"], skills=[], company=experience["company"], date=experience["date"], location=experience["location"], points=experience["points"]) for experience in chosen_experiences]
formatted_projects = [format_project(name=format_link(project["name"], project["link"]) if "link" in project and project["link"] is not None else project["name"], date=project["date"], skills=project["skills"], points=project["points"]) for project in chosen_projects]

resume = format_latex(formatted_experiences, formatted_projects, chosen_skills)

print("Resume generated")
# write the resume
with open("resume.tex", "w") as f:
    f.write(resume.replace(r"\#", "#"))


print("Resume written to file")

    
    




    




