from manim import *
import sys
import os

# Ensure we can import from pipeline
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pipeline.tts import generate_voice

class AI_ML_DL_Scene(Scene):
    def construct(self):
        try:
            self._construct_logic()
        except Exception as e:
            import traceback
            with open("error.log", "w") as f:
                f.write(traceback.format_exc())
                f.write(str(e))
            raise e

    def _construct_logic(self):
        # -------------------------------------------------------------
        # Helper Functions
        # -------------------------------------------------------------
        def speak_and_play(text, *anims, min_wait=0.0):
            """
            Generate voiceover, add sound, and play animations CONCURRENTLY.
            """
            try:
                audio_path, duration = generate_voice(text)
                self.add_sound(audio_path)
                
                if anims:
                    # Execute animations while audio plays
                    # We don't force run_time unless necessary, Manim defaults to 1s usually
                    # But we want to ensure we wait nicely
                    self.play(*anims)
                    
                    # Calculate remaining time
                    # Logic: play() blocks for some time (approx 1s usually per anim if not specified loops)
                    # We can't easily know exact play duration without inspecting anims or forcing it.
                    # Simple approach: assume standard play takes ~1-2s. 
                    # Better approach: We rely on self.wait() to fill the GAP.
                    # But self.play() consumes time. 
                    # Let's adjust: we expect the user to pass animations. We play them.
                    # Then we wait for max(0, duration - 1). 
                    # Assuming standard run_time=1.
                    
                    # More robust: Let animations finish naturally. Then Wait remainder.
                    # But if audio is shorter than animation? Audio stops, animation continues. acceptable.
                    
                    # Sync strategy:
                    # 1. Start audio.
                    # 2. Play animations.
                    # 3. Wait for any remaining audio timestamp.
                    # Problem: We don't track elapsed time easily in construct.
                    
                    # Simplified sync for this scale: 
                    # Audio usually longer than animation (2-4s audio, 1s animation).
                    # We assume play takes ~1s. 
                    self.wait(max(0, duration - 1.0))
                else:
                    self.wait(max(duration, min_wait))
                    
            except Exception as e:
                print(f"TTS Error: {e}")
                if anims:
                    self.play(*anims)
                self.wait(min_wait)

        def cleanup_scene():
            """Fade out all objects cleanly"""
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
            self.wait(0.2)

        # -------------------------------------------------------------
        # SCENE START
        # -------------------------------------------------------------
        self.camera.background_color = "#1e1e1e"  # Dark background

        # ==============================
        # 1. Kinetic Typography (Intro)
        # ==============================
        text_ai = Text("Artificial Intelligence", font_size=72, weight=BOLD, color=YELLOW).to_edge(UP)
        text_dl = Text("Deep Learning", font_size=60, weight=BOLD, color=BLUE).next_to(text_ai, DOWN, buff=1)
        text_ml = Text("Machine Learning", font_size=60, weight=BOLD, color=GREEN).next_to(text_dl, DOWN, buff=0.8)

        # Sync: Speak AND Write text
        speak_and_play(
            "Let's explore Artificial Intelligence, Deep Learning, and Machine Learning visually.",
            Write(text_ai),
            FadeIn(text_dl, shift=UP*0.2),
            Write(text_ml)
        )
        cleanup_scene()

        # ==============================
        # 2. 2D Explainer (AI Concept)
        # ==============================
        # Brain Diagram (AI Concept)
        brain = Circle(radius=2, color=YELLOW, fill_opacity=0.1).to_edge(UP)
        brain_label = Text("AI = Smart Machines", font_size=28, color=WHITE).next_to(brain, DOWN, buff=0.5)

        # Neural Connections inside Brain
        nodes = VGroup(*[Dot(point=brain.get_center()+np.array([x, y, 0])*0.5, color=BLUE) 
                         for x, y in [(-1,0.5),(0.5,1),(-0.5,-1),(1,-0.5)]])

        connections = VGroup(*[Line(nodes[i].get_center(), nodes[j].get_center(), color=WHITE) 
                               for i in range(len(nodes)) for j in range(i+1, len(nodes))])

        # Sync: Speak AND Show Diagrams
        speak_and_play(
            "Artificial Intelligence is about creating smart machines that can perform tasks like humans.",
            FadeIn(brain),
            Write(brain_label),
            *[FadeIn(node) for node in nodes],
            *[Create(line) for line in connections]
        )
        
        cleanup_scene()

        # ==============================
        # 3. Flowchart (AI -> ML -> DL)
        # ==============================
        # Create non-overlapping stacked rectangles
        ai_box = RoundedRectangle(height=1.5, width=5, color=YELLOW, corner_radius=0.2).to_edge(UP, buff=1)
        ml_box = RoundedRectangle(height=1.2, width=4, color=GREEN, corner_radius=0.2).next_to(ai_box, DOWN, buff=1.2)
        dl_box = RoundedRectangle(height=1.0, width=3, color=BLUE, corner_radius=0.2).next_to(ml_box, DOWN, buff=1)

        ai_label = Text("AI", font_size=24, color=BLACK).move_to(ai_box)
        ml_label = Text("Machine Learning", font_size=20, color=BLACK).move_to(ml_box)
        dl_label = Text("Deep Learning", font_size=18, color=BLACK).move_to(dl_box)

        arrow1 = Arrow(start=ai_box.get_bottom(), end=ml_box.get_top(), color=WHITE)
        arrow2 = Arrow(start=ml_box.get_bottom(), end=dl_box.get_top(), color=WHITE)

        # Sync: Speak AND Build Flowchart
        speak_and_play(
            "Machine Learning is a subset of AI, and Deep Learning is a subset of Machine Learning.",
            Create(ai_box), Write(ai_label),
            Create(ml_box), Write(ml_label),
            Create(dl_box), Write(dl_label),
            Create(arrow1), Create(arrow2)
        )
        cleanup_scene()

        # ==============================
        # 4. Infographic Motion Graphics (ML Workflow)
        # ==============================
        steps = ["Data", "Model", "Training", "Evaluation"]
        colors = [BLUE, GREEN, ORANGE, YELLOW]
        step_boxes = VGroup()
        step_texts = VGroup()

        for i, (step, color) in enumerate(zip(steps, colors)):
            box = RoundedRectangle(width=3, height=1, color=color, corner_radius=0.2)
            text = Text(step, font_size=22, color=BLACK)
            if i == 0:
                box.to_edge(LEFT, buff=1)
            else:
                box.next_to(step_boxes[i-1], RIGHT, buff=0.8)
            text.move_to(box)
            step_boxes.add(box)
            step_texts.add(text)

        arrows = VGroup(*[Arrow(start=step_boxes[i].get_right(), end=step_boxes[i+1].get_left(), color=WHITE)
                          for i in range(len(step_boxes)-1)])

        # Construct anim list dynamically
        anims = []
        for box, text in zip(step_boxes, step_texts):
            anims.append(Create(box))
            anims.append(Write(text))
        for arrow in arrows:
            anims.append(Create(arrow))

        # Sync: Speak AND Show Workflow
        speak_and_play(
            "Machine Learning has a workflow: Data Collection, Model Design, Training, and Evaluation.",
            *anims
        )
        cleanup_scene()

        # ==============================
        # 5. Character-based Storytelling (Neural Network Analogy)
        # ==============================
        input_node = Circle(radius=0.5, color=BLUE, fill_opacity=0.8).shift(LEFT*3)
        hidden_node = Circle(radius=0.5, color=GREEN, fill_opacity=0.8)
        output_node = Circle(radius=0.5, color=YELLOW, fill_opacity=0.8).shift(RIGHT*3)

        input_label = Text("Input Node", font_size=18).next_to(input_node, DOWN)
        hidden_label = Text("Hidden Node", font_size=18).next_to(hidden_node, DOWN)
        output_label = Text("Output Node", font_size=18).next_to(output_node, DOWN)

        conn1 = Line(input_node.get_right(), hidden_node.get_left(), color=WHITE)
        conn2 = Line(hidden_node.get_right(), output_node.get_left(), color=WHITE)

        # Sync: Speak AND Show Nodes
        speak_and_play(
            "Think of a neural network as a team passing messages to make decisions.",
            FadeIn(input_node), Write(input_label),
            FadeIn(hidden_node), Write(hidden_label),
            FadeIn(output_node), Write(output_label),
            Create(conn1), Create(conn2)
        )
        
        speak_and_play("Data flows from input to hidden layers and produces output.")
        cleanup_scene()

        # ==============================
        # 6. Whiteboard/Doodle Outro
        # ==============================
        board = Rectangle(width=12, height=7, color=WHITE, fill_opacity=1)
        self.camera.background_color = "#e0e0e0"

        summary_title = Text("Summary", font_size=50, color=BLACK, weight=BOLD).to_edge(UP)
        summary_items = VGroup(
            Text("✔ AI: Intelligence in Machines", font_size=28, color=BLACK),
            Text("✔ ML: Learning from Data", font_size=28, color=BLACK),
            Text("✔ DL: Neural Networks at Scale", font_size=28, color=BLACK)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(LEFT*2 + DOWN*1)
        
        credit = Text("Directed and coded by Tarif", font_size=40, color=BLUE, weight=BOLD).next_to(summary_items, DOWN, buff=1)

        # Sync: Speak AND Show Summary
        speak_and_play(
            "That's a visual journey through AI, Machine Learning, and Deep Learning.",
            FadeIn(board), Write(summary_title),
            Write(summary_items)
        )

        speak_and_play(
            "Directed and coded by Tarif.",
            Write(credit)
        )
        
        self.wait(2)
        self.play(FadeOut(board), FadeOut(summary_title), FadeOut(summary_items), FadeOut(credit), run_time=1)
