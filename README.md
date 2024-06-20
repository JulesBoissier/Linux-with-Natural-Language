# Using and Setting Up Translate Command Script

The `translate_command` script utilizes OpenAI's API to translate natural language commands into executable Linux commands. It optionally provides explanations and allows execution of the translated command.

### TODOs:

    - Add safety feature to block dangerous commands.
    - Add more context to system prompt, specifically:
        - Distro.
        - Location in file structure.
        - Available packages.

### Prerequisites

- Python 3.x installed on your system
- Access to OpenAI's API with an `OPENAI_API_KEY` set in your environment or `.env` file
- Installation of required Python packages (`dotenv`, `click`, `openai`)

### Setup

1. **Clone the Repository**

   Clone the repository containing the script from GitHub or your preferred version control system.

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**

   Install the required Python packages using pip. It's recommended to use a virtual environment (`venv`).

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

   - `dotenv` for loading environment variables from `.env` file.
   - `click` for command-line interface creation.
   - `openai` for interacting with OpenAI's API.

3. **Set Environment Variables**

   Create a `.env` file in the root of your project directory and add your OpenAI API key:

   ```plaintext
   OPENAI_API_KEY=your_api_key_here
   ```

   Replace `your_api_key_here` with your actual OpenAI API key.

4. **Add Alias to Shell Configuration**

   To use the script conveniently from any directory, add an alias to your shell configuration (`~/.zshrc` for zsh, `~/.bashrc` for bash):

   ```bash
   nano ~/.zshrc
   ```

   Add the alias at the end of the file:

   ```bash
   alias lnl='python /path/to/translate_command.py'
   ```

   Replace `/path/to/translate_command.py` with the actual path to your `translate_command.py` script.

5. **Save and Reload Configuration**

   Save the file (`Ctrl+O` in nano, then `Enter`, and `Ctrl+X` to exit), then reload your shell configuration:

   ```bash
   source ~/.zshrc
   ```

### Usage

The script provides options to translate a natural language command into a Linux command, optionally explain its functionality, and execute it.

```bash
lnl "Your natural language command here" --explain --model gpt-3.5-turbo --trust --sudo --timeout 30
```

#### Command-line Options:

- `query`: Required. The natural language command to be translated.
- `--model`: Specify the model to use for translation (default is `gpt-3.5-turbo`).
- `--explain`: Enable explanation of the translated command.
- `--trust`: Enable trusted mode for translation.
- `--sudo`: Enable sudo mode for translation.
- `--timeout`: Specify a timeout for the command execution (default is 30 seconds).

#### Example Usage:

Translate a command with explanation and execute it:

```bash
lnl "Count the number of files in ~/etc created in the last 24 hours" --explain
```

#### Output Example:

```plaintext
Translated command:  find ~/etc -type f -mtime -1 | wc -l
Explanation:
 1. `find ~/etc -type f -mtime -1`: This command searches for files (`-type f`) in the `~/etc` directory and its subdirectories that were modified less than 1 day ago (`-mtime -1`).

2. `|`: This symbol is a pipe, which takes the output from the command on the left and passes it as input to the command on the right.

3. `wc -l`: This command counts the number of lines in the input it receives.

Therefore, the whole command finds files modified in the last day in the `~/etc` directory and its subdirectories  and then counts how many of those files were found.
Run command? (Y/N): Y
Command output:
<output of the command execution>
```

---

This guide provides a comprehensive approach to setting up and using your `translate_command` script with the `lnl` alias for convenience. Adjust paths and configurations as per your specific project setup and requirements.
