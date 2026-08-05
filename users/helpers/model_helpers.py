from django.db import models


class SignupType(models.TextChoices):
    EMAIL = 'email', 'Email'
    GOOGLE = 'google', 'Google'


class UserType(models.TextChoices):
    SUPERADMIN = 'superadmin', 'Superadmin'
    CREATOR = 'creator', 'Creator'
    LEARNER = 'learner', 'Learner'


class ExperienceRange(models.TextChoices):
    LESS_THAN_1 = '0-1', '0 - 1 Years'
    ONE_TO_THREE = '1-3', '1 - 3 Years'
    THREE_TO_FIVE = '3-5', '3 - 5 Years'
    FIVE_TO_TEN = '5-10', '5 - 10 Years'
    TEN_PLUS = '10+', '10+ Years'


class TeachingCategory(models.TextChoices):
    DEVELOPMENT = 'development', 'Software & Web Development'
    DATA_SCIENCE = 'data_science', 'Data Science & AI'
    DESIGN = 'design', 'UI/UX & Graphic Design'
    BUSINESS = 'business', 'Business & Finance'
    MARKETING = 'marketing', 'Digital Marketing'
    PERSONAL_DEVELOPMENT = 'personal_dev', 'Personal Development'
    OTHER = 'other', 'Other'


class Profession(models.TextChoices):
    SOFTWARE_ENGINEER = 'software_engineer', 'Software Engineer / Developer'
    DATA_SCIENTIST = 'data_scientist', 'Data Scientist / Analyst'
    DESIGNER = 'designer', 'Product / UI/UX Designer'
    EDUCATOR = 'educator', 'Educator / Teacher'
    CONTENT_CREATOR = 'content_creator', 'Content Creator / Influencer'
    CONSULTANT = 'consultant', 'Consultant / Freelancer'
    ENTREPRENEUR = 'entrepreneur', 'Entrepreneur / Founder'
    STUDENT = 'student', 'Student'
    OTHER = 'other', 'Other'


from users.helpers.location_helpers import STATE_CITIES_MAP, State  # noqa: F401
