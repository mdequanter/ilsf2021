from google.cloud import dialogflow


def detect_intent_text(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    print(query_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input})
    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print("Detected intent: {} (confidence: {})\n".format(response.query_result.intent.display_name,
                                                          response.query_result.intent_detection_confidence,))
    print("Fulfillment text: {}\n".format(
        response.query_result.fulfillment_text))


def detect_intent_audio(project_id, session_id, audio_file_path, language_code):
    """Returns the result of detect intent with an audio file as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 44100

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    with open(audio_file_path, "rb") as audio_file:
        input_audio = audio_file.read()

    audio_config = dialogflow.InputAudioConfig(
        audio_encoding=audio_encoding,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
    )
    query_input = dialogflow.QueryInput(audio_config=audio_config)

    request = dialogflow.DetectIntentRequest(
        session=session,
        query_input=query_input,
        input_audio=input_audio,
    )
    response = session_client.detect_intent(request=request)

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print (response.query_result.fulfillment_text)


#detect_intent_audio("chatbot-ilsf", "123456789", "bonjour.wav", "fr")
detect_intent_text("chatbot-ilsf", "78451","Hallo", "nl")
