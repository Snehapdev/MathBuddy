import os
import google.generativeai as genai
from django.conf import settings



def get_solution_steps(equation):

    # Access your API key as an environment variable.
    genai.configure(api_key=settings.GEN_LANGUAGE_API_KEY)
    # Choose a model that's appropriate for your use case.
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = "Give steps to solve the equation "+ equation

    response = model.generate_content(prompt)

    return response.text