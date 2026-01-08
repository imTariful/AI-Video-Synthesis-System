import os
import subprocess

class Renderer:
    def __init__(self, output_file="generated_scene.py"):
        self.output_file = output_file

    def render(self, blueprint: dict):
        """
        Generates Manim code from blueprint and executes it.
        """
        print("Translating blueprint to Manim code...")
        
        manim_code = self._generate_manim_code(blueprint)
        
        with open(self.output_file, "w") as f:
            f.write(manim_code)
            
        print(f"Manim code written to {self.output_file}. Starting render...")
        
        # Command to run manim
        # -ql = Low quality for speed in prototype
        # Use python -m manim to ensure we use the installed module
        import sys
        cmd = f"{sys.executable} -m manim -ql {self.output_file} GeneratedScene"
        try:
            subprocess.run(cmd, shell=True, check=True)
            print("Rendering complete!")
        except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
            print(f"Rendering failed (Manim might not be installed): {e}")
            print("Skipping video generation step. Python scene file is saved.")

    def _generate_manim_code(self, blueprint: dict) -> str:
        code = "from manim import *\n\n"
        code += "class GeneratedScene(Scene):\n"
        code += "    def construct(self):\n"
        
        # Add title
        title = blueprint.get("title", "Video")
        
        for i, scene in enumerate(blueprint["scenes"]):
            code += f"        # Scene {i+1}\n"
            
            # Group for this scene to clean up later
            code += f"        scene_group_{i} = VGroup()\n"
            
            for visual in scene["visuals"]:
                v_type = visual["type"]
                name = f"elem_{i}_{visual.get('type')}_{id(visual)}"
                
                if v_type == "text":
                    content = visual["content"].replace('"', '\\"')
                    code += f"        {name} = Text(\"{content}\", font_size=24)\n"
                    if visual.get("position") == "center":
                        code += f"        {name}.move_to(ORIGIN)\n"
                    elif visual.get("position") == "bottom":
                        code += f"        {name}.to_edge(DOWN)\n"
                    code += f"        scene_group_{i}.add({name})\n"
                    
                elif v_type == "rectangle":
                    code += f"        {name} = Rectangle(color={visual.get('color', 'WHITE')})\n"
                    if visual.get("position") == "left":
                        code += f"        {name}.shift(LEFT * 2)\n"
                    elif visual.get("position") == "right":
                        code += f"        {name}.shift(RIGHT * 2)\n"
                    code += f"        scene_group_{i}.add({name})\n"
                    
                elif v_type == "circle":
                    code += f"        {name} = Circle(color={visual.get('color', 'WHITE')})\n"
                    code += f"        scene_group_{i}.add({name})\n"
                
                elif v_type == "arrow":
                    code += f"        {name} = Arrow(start=LEFT, end=RIGHT)\n"
                    code += f"        scene_group_{i}.add({name})\n"

                elif v_type == "grid":
                     code += f"        {name} = NumberPlane()\n"
                     code += f"        scene_group_{i}.add({name})\n"

            # Animation
            code += f"        # Narration: {scene.get('narration')}\n"
            code += f"        # self.add_sound('tts_{i}.mp3') # Placeholder for AI TTS\n"
            code += f"        self.play(FadeIn(scene_group_{i}))\n"
            code += f"        self.wait({scene.get('duration', 2)})\n"
            code += f"        self.play(FadeOut(scene_group_{i}))\n\n"
            
        return code

if __name__ == "__main__":
    # Test stub
    pass
