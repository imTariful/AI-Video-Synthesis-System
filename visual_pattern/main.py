import argparse
import json
import os
from pipeline.script_gen import ScriptGenerator
from pipeline.blueprint_gen import BlueprintGenerator
from pipeline.renderer import Renderer

def main():
    parser = argparse.ArgumentParser(description="Hybrid Video Generation System")
    parser.add_argument("--topic", type=str, required=True, help="Topic for the video")
    parser.add_argument("--style", type=str, default="default", help="Style config path (optional)")
    
    args = parser.parse_args()
    
    print(f"Starting Video Generation for Topic: {args.topic}")
    
    # 1. Generate Script
    script_gen = ScriptGenerator()
    script = script_gen.generate_script(args.topic)
    print("Script Generated:")
    print(json.dumps(script, indent=2))
    
    # save debug
    with open("debug_script.json", "w") as f:
        json.dump(script, f, indent=2)

    # 2. Generate Blueprint
    # Mocking the Manual Style Profile input
    mock_style_profile = {
        "primary_color": "BLUE",
        "shape_style": "geometric"
    }
    
    blueprint_gen = BlueprintGenerator()
    blueprint = blueprint_gen.create_blueprint(script, style_profile=mock_style_profile)
    print("\nBlueprint Generated:")
    print(json.dumps(blueprint, indent=2))

    with open("debug_blueprint.json", "w") as f:
        json.dump(blueprint, f, indent=2)

    # 3. Render
    renderer = Renderer()
    renderer.render(blueprint)
    
    print("Pipeline Finished.")

if __name__ == "__main__":
    main()
