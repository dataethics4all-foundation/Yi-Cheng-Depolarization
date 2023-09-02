import main

# Just a way to simulate a conversation
def dialogue(topic, stance, query_type):
    # query_type: is this a request to /depolarize or /debate. Which function are we testing?
    # Choose a topic / have a list of topics that it iterates through
    # Send topic to survey, and create a response to it
    # Create a response that agrees and disagrees with the topic, and evaluate
    #   Metrics: depol agreement rate for persona, polarization change
    # For now, random, but eventually recursion
    # Test each function

    main.survey()

# How different personalities create depolarization rates
def persona(input, personality):
    context = personality + input   #TODO: build prompt
    main.query(personality)