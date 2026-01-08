from manim import *
import sys
import os

# Ensure we can import from pipeline
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pipeline.tts import generate_voice

class WebSocketScene(Scene):
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
        def speak(text, min_wait=0.0):
            try:
                audio_path, duration = generate_voice(text)
                self.add_sound(audio_path)
                wait_time = max(duration, min_wait)
                self.wait(wait_time)
            except Exception as e:
                print(f"TTS Error: {e}")
                self.wait(min_wait)

        def cleanup_scene():
            """Clears all mobjects from the scene seamlessly"""
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
            self.wait(0.2)

        # -------------------------------------------------------------
        # SCENE START
        # -------------------------------------------------------------
        self.camera.background_color = "#1e1e1e"

        # ==============================
        # 1. Kinetic Typography (Intro)
        # ==============================
        # Aesthetic: Bold, Centered, High Contrast
        text_ws = Text("WebSockets", font_size=72, weight=BOLD, color=BLUE).shift(UP*0.5)
        text_vs = Text("vs", font_size=36, weight=BOLD, color=GREY_B).next_to(text_ws, DOWN)
        text_http = Text("HTTP", font_size=60, weight=BOLD, color=RED).next_to(text_vs, DOWN)
        
        speak("We are here to master WebSockets. Let's visualize the 9 dimensions of this protocol.")
        
        self.play(Write(text_ws), run_time=0.8)
        self.play(FadeIn(text_vs, shift=UP*0.2))
        self.play(Write(text_http), run_time=0.8)
        self.wait(1)
        cleanup_scene()

        # ==============================
        # 2. 2D Explainer (Concept Diagram)
        # ==============================
        speak("First, the concept. Imagine a dedicated tunnel through the chaotic internet.")
        
        # Cloud Shape (Representing Internet)
        cloud = VGroup(
            Ellipse(width=5, height=3, color=WHITE, fill_opacity=0.1),
            Ellipse(width=3, height=2, color=WHITE, fill_opacity=0.1).shift(LEFT*1.5 + DOWN*0.5),
            Ellipse(width=3, height=2, color=WHITE, fill_opacity=0.1).shift(RIGHT*1.5 + UP*0.5)
        ).move_to(ORIGIN)
        cloud_label = Text("The Internet", font_size=24, color=GREY_A).next_to(cloud, UP)
        
        # Tunnel (Representing WebSocket)
        tunnel = Rectangle(width=6, height=1.2, color=BLUE, fill_opacity=0.2, stroke_width=4).move_to(ORIGIN)
        tunnel_lines = VGroup(
            Line(tunnel.get_left(), tunnel.get_right(), color=BLUE_E).shift(UP*0.3),
            Line(tunnel.get_left(), tunnel.get_right(), color=BLUE_E).shift(DOWN*0.3)
        )
        tunnel_label = Text("Persistent Tunnel", font_size=20, color=BLUE_B).move_to(tunnel)
        
        self.play(Create(cloud), FadeIn(cloud_label))
        self.play(Create(tunnel), Create(tunnel_lines), Write(tunnel_label))
        self.wait(1.5)
        cleanup_scene()

        # ==============================
        # 3 & 4. Flowchart + Arrows & Line-based (The Standard HTTP)
        # ==============================
        speak("In standard HTTP, we have a disjointed request-response loop.")
        
        client = RoundedRectangle(height=1.5, width=2.5, color=BLUE, corner_radius=0.2).to_edge(LEFT, buff=1.5)
        client_lbl = Text("Client", font_size=20).move_to(client)
        
        server = RoundedRectangle(height=1.5, width=2.5, color=GREEN, corner_radius=0.2).to_edge(RIGHT, buff=1.5)
        server_lbl = Text("Server", font_size=20).move_to(server)
        
        # Use curved arrows to show the 'loop' nature better and avoid overlap
        req_line = CurvedArrow(client.get_top(), server.get_top(), color=YELLOW, angle=-TAU/4)
        req_text = Text("Request", font_size=18, color=YELLOW).next_to(req_line, UP)
        
        res_line = CurvedArrow(server.get_bottom(), client.get_bottom(), color=ORANGE, angle=-TAU/4)
        res_text = Text("Response", font_size=18, color=ORANGE).next_to(res_line, DOWN)
        
        self.play(Create(client), Write(client_lbl), Create(server), Write(server_lbl))
        self.play(Create(req_line), FadeIn(req_text))
        self.play(Create(res_line), FadeIn(res_text))
        speak("Ask, wait, receive, close. Repeat.", min_wait=1)
        cleanup_scene()

        # ==============================
        # 7. Infographic Motion Graphics (The Handshake)
        # ==============================
        speak("To open our tunnel, we need a special 'Handshake'.")
        
        # Layout: Split screen or centered Card
        # Reduce text amount, increase font size compatibility
        panel = rounded_rect = RoundedRectangle(width=10, height=5, color=GREY_D, fill_opacity=0.1)
        
        header_req = Text("Client Request", font_size=24, color=BLUE).move_to(panel.get_top()).shift(DOWN*0.6)
        code_req = Text(
            "GET /chat HTTP/1.1\nUpgrade: websocket\nConnection: Upgrade",
            font_size=22, line_spacing=1.8, font="Consolas", color=WHITE,
            t2c={"Upgrade": YELLOW, "websocket": GREEN}
        ).next_to(header_req, DOWN, buff=0.4)
        
        self.play(Create(panel), Write(header_req))
        self.play(Write(code_req, run_time=2))
        
        # Separate the response clearly
        divider = Line(panel.get_left(), panel.get_right(), color=GREY).shift(DOWN*0.5)
        header_res = Text("Server Response", font_size=24, color=GREEN).next_to(divider, DOWN, buff=0.2)
        code_res = Text(
             "HTTP/1.1 101 Switching Protocols",
             font_size=28, weight=BOLD, color=GREEN_A
        ).next_to(header_res, DOWN, buff=0.3)
        
        self.play(Create(divider), FadeIn(header_res))
        self.play(TransformFromCopy(code_req, code_res))
        
        self.wait(1.5)
        cleanup_scene()

        # ==============================
        # 5 & 6. Character-based & Storytelling (Alice & Bob Chat)
        # ==============================
        speak("Now, let's see Alice and Bob communicate in real-time.")

        # Characters closer to center, less empty space
        alice_head = Circle(radius=0.5, color=PINK, fill_opacity=0.8, fill_color=PINK).shift(LEFT*3)
        alice_lbl = Text("Alice", font_size=20).next_to(alice_head, DOWN)
        
        bob_head = Circle(radius=0.5, color=TEAL, fill_opacity=0.8, fill_color=TEAL).shift(RIGHT*3)
        bob_lbl = Text("Bob", font_size=20).next_to(bob_head, DOWN)
        
        pipe = Line(alice_head.get_right(), bob_head.get_left(), color=BLUE_E, stroke_width=8)
        
        self.play(FadeIn(alice_head), Write(alice_lbl), FadeIn(bob_head), Write(bob_lbl))
        self.play(Create(pipe))

        # Chat bubbles that don't overlap the line
        msg_a = RoundedRectangle(width=1.5, height=0.6, color=WHITE, corner_radius=0.3).next_to(alice_head, UP)
        msg_text_a = Text("Hey!", font_size=18, color=BLACK).move_to(msg_a)
        
        self.play(GrowFromCenter(msg_a), Write(msg_text_a))
        
        # "Sending" animation
        packet = Dot(color=YELLOW).move_to(alice_head.get_right())
        self.play(MoveAlongPath(packet, pipe), run_time=0.5)
        self.remove(packet)

        msg_b = RoundedRectangle(width=1.5, height=0.6, color=WHITE, corner_radius=0.3).next_to(bob_head, UP)
        msg_text_b = Text("Hi!!", font_size=18, color=BLACK).move_to(msg_b)
        
        self.play(GrowFromCenter(msg_b), Write(msg_text_b))
        
        speak("Messages arrive instantly, no polling required.", min_wait=1)
        cleanup_scene()

        # ==============================
        # 8. UI Walkthrough (Browser DevTools Simulation)
        # ==============================
        speak("For developers, verification is key. We check the Network Tab.")
        
        # Cleaner UI Layout
        browser_frame = RoundedRectangle(width=11, height=6.5, color=GREY_C, corner_radius=0.1)
        url_bar = Rectangle(width=11, height=0.5, color=DARK_GREY, fill_opacity=1).align_to(browser_frame, UP)
        url_text = Text("ws://localhost:8080/chat", font_size=16, color=WHITE).move_to(url_bar).to_edge(LEFT, buff=1.5)
        
        devtools_panel = Rectangle(width=11, height=3, color=BLACK, fill_opacity=0.85).align_to(browser_frame, DOWN)
        tabs = VGroup(
            Text("Network", font_size=18, color=BLUE, weight=BOLD),
            Text("|", font_size=18, color=GREY),
            Text("Console", font_size=18, color=GREY),
        ).arrange(RIGHT, buff=0.2).align_to(devtools_panel, UP)
        tabs.move_to(devtools_panel.get_top() + DOWN*0.3 + LEFT*3)

        # Header Row
        headers = VGroup(
            Text("Name", font_size=16, color=GREY_B),
            Text("Status", font_size=16, color=GREY_B),
            Text("Type", font_size=16, color=GREY_B),
            Text("Time", font_size=16, color=GREY_B),
        ).arrange(RIGHT, buff=1.5).next_to(tabs, DOWN, buff=0.4).align_to(tabs, LEFT)

        # Data Row
        data_row = VGroup(
            Text("chat", font_size=16, color=WHITE),
            Text("101", font_size=16, color=GREEN),
            Text("websocket", font_size=16, color=GREY_A),
            Text("Pending", font_size=16, color=GREY_A),
        )
        # Align each data item to its header manually for table look
        for i, item in enumerate(data_row):
            item.match_x(headers[i])
        data_row.match_y(headers).shift(DOWN*0.5)

        self.play(Create(browser_frame), FadeIn(url_bar), Write(url_text))
        self.play(FadeIn(devtools_panel, shift=UP*0.2))
        self.play(Write(tabs))
        self.play(FadeIn(headers))
        self.play(Write(data_row))
        
        # Highlight the 101
        highlight = SurroundingRectangle(data_row[1], color=YELLOW, buff=0.1)
        self.play(Create(highlight))
        
        speak("Status 101 confirms the protocol switch. The connection remains 'Pending' indefinitely.", min_wait=2)
        cleanup_scene()


        # ==============================
        # 9. Whiteboard/Doodle (Outro & Credits)
        # ==============================
        speak("And that's a wrap on WebSockets!")
        
        # Paper background effect? Just using a light grey rect for the "Board"
        board = Rectangle(width=10, height=6, color=WHITE, fill_opacity=1) # Whiteboard
        self.camera.background_color = "#e0e0e0" # Light theme for whiteboard
        
        # Use a "handwritten" look font if available, otherwise just contrasting color
        # Since Manim default fonts are limited, we use standard sans-serif but dark color
        
        title_text = Text("Summary", font_size=40, color=BLACK, weight=BOLD).to_edge(UP)
        
        checklist = VGroup(
            Text("✔ Interactive", font_size=28, color=BLACK),
            Text("✔ Low Latency", font_size=28, color=BLACK),
            Text("✔ Standardized", font_size=28, color=BLACK),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(LEFT*1)
        
        self.play(FadeIn(board), Write(title_text))
        self.play(Write(checklist, run_time=1.5))
        
        speak("Directed and code Written by Tarif.", min_wait=1.5)
        
        credit = Text("Directed and code Written by Tarif", font_size=45, color=BLUE_E, weight=BOLD).next_to(checklist, DOWN, buff=1)
        self.play(Write(credit))
        
        self.wait(2)
        # Fade to black for final clean exit
        self.play(FadeOut(board), FadeOut(title_text), FadeOut(checklist), FadeOut(credit), run_time=1)
