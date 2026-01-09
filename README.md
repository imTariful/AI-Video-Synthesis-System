# Hybrid Video Generation System

A powerful hybrid tool that combines manual artistic style analysis with an automated AI-driven pipeline to generate educational videos using **Manim**.

## 🚀 Features

### 1. 🎨 Manual Style Research
- **Style Profile Template**: A structured Markdown template (`style_analysis_template.md`) for engineers to analyze and document the visual style of reference videos (color palettes, transition types, typography).

### 2. ⚡ Automatic Generation Pipeline
- **Topic-to-Video**: Input a simple text topic, and the system handles the rest.
- **Script Generation**: Automatically drafts a narration script and scene visuals based on the topic.
- **Blueprint Engine**: Converts the script into a technical animation blueprint, applying the defined "Style Profile".
- **Code Generation**: Produces executable Python code for Manim.

### 3. 🔊 Integrated TTS & Sync
- **Auto-Voiceover**: Uses `gTTS` (Google Text-to-Speech) to generate audio for each scene.
- **Auto-Sync**: Automatically calculates audio duration and adjusts video timing (`self.wait()`) to ensure perfect lip-sync.

### 4. 🛠️ Human-in-the-Loop Refinement
- The system generates a `generated_scene.py` file.
- **Manual Edit Support**: Engineers can tweak the generated Python code to add complex, high-fidelity animations (as demonstrated with the "AI Research Scene").
- **Robust Rendering**: Supports rendering without a full LaTeX installation by using native Manim `Text` objects.

---

## 📦 Installation

### Prerequisites
1.  **Python 3.10+**
2.  **FFmpeg**: Required for video rendering. [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your system PATH.
3.  **Manim Community**:
    ```bash
    pip install manim
    ```

### Setup
1.  Clone the repository.
2.  Install python dependencies:
    ```bash
    pip install gTTS mutagen numpy
    ```

---

## 💻 Usage

### Automatic Generation (CLI)
To generate a video from scratch:

```bash
python main.py --topic "Your Topic Here"
```
*Example: `python main.py --topic "Neural Networks"`*

This will:
1.  Generate a script.
2.  Create a visual blueprint.
3.  Generate `generated_scene.py`.
4.  Render the video to `media/videos/generated_scene/480p15/GeneratedScene.mp4`.

### Manual Refinement (Advanced)
1.  Open `generated_scene.py`.
2.  Edit the code to improve visuals or change narration.
3.  Re-render manually:
    ```bash
    manim -ql generated_scene.py AIResearchScene
    ```
    *Flags explanation:*
    *   `-ql`: Low quality (faster render). Use `-qh` for High Quality (1080p).
    *   `-p`: Preview (plays video after rendering).

---

## 📂 Project Structure

```text
visual_pattern/
├── main.py                  # CLI Entry point
├── generated_scene.py       # The generated Manim code (Editable)
├── style_analysis_template.md # Template for manual research
├── error.log                # Captures render errors for debugging
├── pipeline/                # Core logic modules
│   ├── script_gen.py        # Generates text Script from Topic
│   ├── blueprint_gen.py     # Converts Script -> Visual Blueprint
│   ├── renderer.py          # Converts Blueprint -> Manim Code & Renders
│   └── tts.py               # Handles Audio generation & duration logic
└── media/                   # Output directory (Videos, Audio, Textures)
```

## 🔧 Troubleshooting

- **LaTeX Error / `latex` not found**:
    - The system is designed to work *without* LaTeX by using `Text` instead of `Tex` or `MathTex`.
    - If you see LaTeX errors, ensure you are not using `DecimalNumber` or `Axes(include_numbers=True)` in your custom code.

- **Audio not playing**:
    - Check the `media/audio` folder to see if MP3s are generated.
    - Ensure `ffmpeg` is installed correctly.

- **Manim Crash**:
    - Check `error.log` for the detailed Python traceback.

---

## 👨‍💻 Credits
**Concept & Implementation**: Tarif
**Powered By**: Manim Community, gTTS

