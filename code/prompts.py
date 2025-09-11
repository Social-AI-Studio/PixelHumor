# Prompts for subjective tasks (Q1 - Q5)
system_prompt = "You are a humorous assistant that understands comics. You will be given comics and your task is to evaluate the comics."
question1 = "Do you understand the humor of this comics? Please output only a single word answer \"Yes\" or \"No\"."
question2 = "Analyze the comic and respond based on the following criteria regarding text-based sound effects: (a) If there are no sound effects present in the comic, output \"Absent\". (b) If sound effects are present and contributing to the humor, output \"Present, contribute\". (c) If sound effects are present but do not contribute to the humor, output \"Present, do not contribute\"."
question3 = "Which panel contributes the most to the humor of this comic? Please output only the labeled panel number."
question4 = "Is the text or the visual modality more important to the humor in this comic? Output \"Both\" if both modalities contribute humor to the comic. Please output only a single word answer \"Text\", \"Visual\", \"Both\"."
question5 =  """Which humor styles best describe the comic? Here are some guidelines for each humor style.

Comparison: This comic compares two or more objects/ideas to reference the differences or similarities. This comic is funny because of this comparison.
Personification: This comic has at least one animal/creature/plant that acts like a human (talking, running on two legs etc.). This comic is funny because of this personified creature/plant.
Exaggeration: This comic attempts to exaggerate (overemphasize or magnify) something out of proportion. This comic is funny because of this exaggeration/absurdity.
Pun: This comic is funny because of the linguistic elements. Linguistic elements include: uncommon uses of language, double-meanings in phrases or words etc.
Sarcasm: This comic expresses an idea/thought that is not the real intention of the character/comic. This comic is funny because of the sarcasm present.
Silliness: There are elements in the comic which are absurd and/or ridiculous. The characters are or did something foolish. This comic is funny because of the silly elements.
Surprise: There was a twist in the narrative or an unexpected element in the comic. This comic is funny because of the twist or unexpected elements.
Dark: There are potentially sensitive, taboo or ideas that violate the norm in this comic where if taken out of context in this comic, might be offensive to others. This comic is because of these benign violations or the dark humor present.

You may select multiple humor styles but output only the humor styles \"Comparison\", \"Personification\", \"Exaggeration\", \"Pun\", \"Sarcasm\", \"Silliness\", \"Surprise\" or \"Dark\"."""

# Prompt for humor interpretation task
humor_explanation = "Explain why this comic is funny or not funny in 3 sentences."

# Prompts for sequence recognition tasks
panel_recognition = "In what order should the panels be read? Respond with the panel numbers only. Write the panel numbers followed by a comma. For example the answer \"3,4,2,1\" will mean that panels will be read in order of panel 3, then panel 4, then panel 2 and finally panel 1."
text_recognition = "For each panel, what are the text inside? Respond as {panel_number}: {text_within_panel}."