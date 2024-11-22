from dataclasses import dataclass, field

@dataclass
class Post:
    """
    A dataclass representing a LinkedIn post.
    
    Attributes:
        organization (str): Name of the organization that made the post
        followers (str): Number of followers at the time of the post
        date (str): Date when the post was published
        text (str): Content of the post
        likes (str): Number of likes on the post
        comments_count (str): Number of comments on the post
        link (str): URL link to the post
    """
    organization: str = ""
    followers: str = ""
    date: str = ""
    text: str = ""
    likes: str = ""
    comments_count: str = ""
    link: str = ""

@dataclass
class CompanyData:
    """
    A dataclass representing LinkedIn company information.
    
    Attributes:
        name (str): Company name
        industry (str): Industry the company operates in
        location (str): Company's primary location
        followers (str): Number of LinkedIn followers
        description (str): Brief company description
        total_employees (str): Total number of employees
        job_opportunities_link (str): URL to company's job listings
        follow_link (str): URL to follow the company
        about_us (str): Detailed company description
        website (str): Company's website URL
        company_size (str): Range of employee count
        headquarters (str): Company headquarters location
        company_type (str): Type of company (e.g., Public, Private)
        founded_year (str): Year the company was founded
        specialties (str): Company's areas of expertise
        posts (list): List of company's posts, each as Post object
    """
    name: str = ""
    industry: str = ""
    location: str = ""
    followers: str = ""
    description: str = ""
    total_employees: str = ""
    job_opportunities_link: str = ""
    follow_link: str = ""
    about_us: str = ""
    website: str = ""
    company_size: str = ""
    headquarters: str = ""
    company_type: str = ""
    founded_year: str = ""
    specialties: str = ""
    posts: list = field(default_factory=lambda: [Post])
