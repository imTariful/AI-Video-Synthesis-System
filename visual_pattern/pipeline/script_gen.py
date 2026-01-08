import json
import random

class ScriptGenerator:
    def __init__(self):
        # In a real system, this would be an LLM client
        pass

    def generate_script(self, topic: str) -> dict:
        """
        Generates a script for a video based on the given topic.
        Returns a dictionary with 'title', 'narration', and 'scenes'.
        """
        print(f"Generating script for topic: {topic}...")
        
        # Mock AI generation logic
        script = {
            "title": f"The Fundamentals of {topic}",
            "scenes": [
                {
                    "id": 1,
                    "type": "intro",
                    "text": f"Welcome to our quick guide on {topic}.",
                    "visual_concept": "Title card with smooth fade in"
                },
                {
                    "id": 2,
                    "type": "concept",
                    "text": f"At its core, {topic} is about connecting the dots.",
                    "visual_concept": "Flowchart nodes connecting"
                },
                {
                    "id": 3,
                    "type": "explanation",
                    "text": "It simplifies complex workflows into manageable steps.",
                    "visual_concept": "Complex mesh simplifying into a straight line"
                },
                {
                    "id": 4,
                    "type": "outro",
                    "text": f"And that's the basic idea behind {topic}. Thanks for watching.",
                    "visual_concept": "End screen with logo"
                }
            ]
        }
        
        return script

if __name__ == "__main__":
    gen = ScriptGenerator()
    print(json.dumps(gen.generate_script("Machine Learning"), indent=2))
