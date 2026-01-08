import json

class BlueprintGenerator:
    def __init__(self):
        pass

    def create_blueprint(self, script: dict, style_profile: dict = None) -> dict:
        """
        Converts a script into a visual blueprint for the renderer.
        Uses style_profile to determine colors and shapes.
        """
        print("Generating animation blueprint...")
        
        # Default style if none provided
        style = {
            "primary_color": "WHITE",
            "background_color": "BLACK", 
            "shape_style": "geometric" 
        }
        if style_profile:
            style.update(style_profile)

        blueprint = {
            "title": script.get("title", "Untitled"),
            "style_settings": style,
            "scenes": []
        }
        
        for scene in script["scenes"]:
            bp_scene = {
                "id": scene["id"],
                "narration": scene["text"],
                "duration": 4.0, # Default duration
                "visuals": []
            }
            
            concept = scene["visual_concept"].lower()
            
            # Simple keyword matching to determine visuals (Prototype Logic)
            if "title" in concept:
                bp_scene["visuals"].append({
                    "type": "text",
                    "content": scene["text"],
                    "position": "center",
                    "scale": 0.8
                })
            elif "flowchart" in concept or "connect" in concept:
                bp_scene["visuals"].append({
                    "type": "rectangle",
                    "position": "left",
                    "color": style["primary_color"] 
                })
                bp_scene["visuals"].append({
                    "type": "rectangle",
                    "position": "right",
                    "color": "GREEN"
                })
                bp_scene["visuals"].append({
                    "type": "arrow",
                    "start": "left",
                    "end": "right"
                })
            elif "mesh" in concept or "complex" in concept:
                 bp_scene["visuals"].append({
                    "type": "grid",
                    "rows": 3,
                    "cols": 3
                })
            else:
                # Default fallback
                bp_scene["visuals"].append({
                    "type": "text",
                    "content": scene["text"],
                    "position": "bottom",
                    "scale": 0.6
                })
                bp_scene["visuals"].append({
                    "type": "circle",
                    "color": "RED" if style["shape_style"] == "geometric" else "ORANGE" 
                })

            blueprint["scenes"].append(bp_scene)
            
        return blueprint

if __name__ == "__main__":
    # Test
    script_mock = {
        "title": "Test",
        "scenes": [{"id":1, "text": "Hello", "visual_concept": "Title card"}]
    }
    gen = BlueprintGenerator()
    print(json.dumps(gen.create_blueprint(script_mock), indent=2))
