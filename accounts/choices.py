from django.db import models


class UserAcademicRankChoices(models.TextChoices):
    PROFESSOR = 'Professor', 'Professor'
    ASSOCIATE_PROFESSOR = 'Associate Professor', 'Associate Professor'
    SENIOR_ASSISTANT = 'Senior Assistant', 'Senior Assistant'
    ASSISTANT = 'Assistant', 'Assistant'
    STUDENT = 'Student', 'Student'