# ml-vietnam-plant-disease-detection
End-to-end machine learning system for detecting plant diseases (rice/coffee leaves) in Vietnam, including data collection, preprocessing, model training, evaluation, and deployment as a web application to support farmers.

# Install libraries for this project
First, install `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```
Then, install Playright:
```bash
crawl4ai-setup
```

# Label-Studio
## Installation
First, install `Homebrew` (Linux and MacOS only):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Note: The above command only work if you have sudo privilege. If you don't have it, try:
```bash
mkdir -p ~/homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C ~/homebrew
eval "$(~/homebrew/bin/brew shellenv)"
echo 'eval "$(~/homebrew/bin/brew shellenv)"' >> ~/.bashrc
source ~/.bashrc
brew update
```

After installing `Homebew`, run:
```bash
brew tap humansignal/tap
brew install humansignal/tap/label-studio
```

After installing Label Studio, initiate the server using the following command:
```bash
label-studio
```

For those who use Windowns, the `label-studio` can not be installed with the current project because of the dependency conflict. Therefore, try:
```powershell
uv venv --python 3.12 .venv-label-studio
.venv-label-studio\Scripts\activate
uv pip install label-studio     
```
## XML Configuration
After installing `label-studio`, open it and load the JSON file. Then, open the setting panel of the current project and paste the following snippet directly into the Code editor (replacing the default `<View></View>`):
```XML
<View>
  <Image name="image" value="$image" zoom="true" crossOrigin="anonymous"/>

  <Header value="Rice Disease Classification:" size="4"/>
  <Choices name="choice" toName="image" choice="single" showInline="true">
    <Choice value="Healthy" />
    <Choice value="BrownSpot" />
    <Choice value="Hispa" />
    <Choice value="LeafBlast" />
    <Choice value="Invalid" />
  </Choices>

  <View style="margin-top: 20px; padding: 15px; background-color: #1e1e1e; border-radius: 8px;">
    <Header value="Scraped Context" size="5"/>
    <Text name="context" value="$context" />
    
    <Header value="Source URL" size="5"/>
    <Text name="source_url" value="$source_url" />
  </View>
</View>
```
## Local Image Serving

Label Studio blocks local file access for security reasons. If your images are broken, you need to restart Label Studio with local file serving enabled by setting these environment variables in your terminal:

On Linux/macOS:
```bash
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/path/to/your/datasets/raw
label-studio
```

On Windows (PowerShell):
```powershell
set LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
set LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=C:\path\to\your\datasets\raw
label-studio
```

# References:
- [Label Studio Docs: Installation](https://labelstud.io/guide/install.html)
- [Unsloth: Gemma 4](https://unsloth.ai/docs/models/gemma-4)
- [Ultralytics: SAM 3](https://docs.ultralytics.com/models/sam-3/)
- [HuggingFace: SAM 3](https://huggingface.co/facebook/sam3)
