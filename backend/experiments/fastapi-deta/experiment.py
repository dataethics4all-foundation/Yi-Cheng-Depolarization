import simulate
import main
# from simulate import *

#Evaluate in experiment / Analyze the simulated conversation
# TODO: parameterize everything
def session(count):
    for i in count:
        survey_questions = simulate.dialogue("Flat Earth", -5, "survey")
        survey_response = simulate.persona(survey_questions, "Flat earther")   # Response to survey

        initial_polarization = main.rate_depolarization(survey_response)

        article = main.get_article("Flat Earth", initial_polarization)
        debate_question = main.debater(5, article)
        debate_response = simulate.persona(debate_question, "Flat earther")

        final_polarization = main.rate_depolarization(debate_response)

        
        # Create change of survey_response and final_response
        # Simulate: Chose a topic, survey generated, response was generated, ...