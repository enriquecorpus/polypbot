class PolypBot:
    GREETINGS = "Kamusta <@{user}>! It's time for our stand up meeting {dept} Standup. " \
                "When you are ready please answer the following question: \n\n *How are you feeling today?*"

    GREETINGS_BLOCK = [{"type": "section", "text": {"type": "mrkdwn",
                                                    "text": "YOUR_MESSAGE_WILL_APPAER_HERE"}},
                       {"type": "divider"}, {"type": "actions", "elements": [
            {"type": "button", "text": {"type": "plain_text", "text": ":neutral_face:", "emoji": True}, "value": "meh"},
            {"type": "button", "text": {"type": "plain_text", "text": ":slightly_smiling_face:", "emoji": True},
             "value": "slightly_smiling"},
            {"type": "button", "text": {"type": "plain_text", "text": ":smiley:", "emoji": True}, "value": "smiley"}]}]

    STAND_UP_QUESTIONS = {1: 'How are you feeling today?', 2: 'What did you do since yesterday?',
                          3: 'What will you do today?', 4: 'Anything blocking your progress?'}
