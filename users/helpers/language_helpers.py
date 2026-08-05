from django.db import models

class CourseLanguage(models.TextChoices):
    # International Languages
    ENGLISH = 'en', 'English'
    SPANISH = 'es', 'Spanish'
    FRENCH = 'fr', 'French'
    GERMAN = 'de', 'German'
    MANDARIN = 'zh', 'Mandarin Chinese'
    ARABIC = 'ar', 'Arabic'
    PORTUGUESE = 'pt', 'Portuguese'
    RUSSIAN = 'ru', 'Russian'
    JAPANESE = 'ja', 'Japanese'
    KOREAN = 'ko', 'Korean'
    
    # National / Regional Languages (India focus as an example, common globally)
    HINDI = 'hi', 'Hindi'
    BENGALI = 'bn', 'Bengali'
    TELUGU = 'te', 'Telugu'
    MARATHI = 'mr', 'Marathi'
    TAMIL = 'ta', 'Tamil'
    URDU = 'ur', 'Urdu'
    GUJARATI = 'gu', 'Gujarati'
    MALAYALAM = 'ml', 'Malayalam'
    KANNADA = 'kn', 'Kannada'
    ODIA = 'or', 'Odia'
    PUNJABI = 'pa', 'Punjabi'
