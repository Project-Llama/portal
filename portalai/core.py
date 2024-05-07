import ollama
import time
import sys
import itertools
import argparse

context = """
You are an AI that translates code from one programming language to another super accurately! You will only send the translated code. No speaking, for you only provide code and nothing else.
Always provide raw code (no comments, triple backticks, non-code text, language names, anything that is not the translated code)
Back ticks (Specifically triple back ticks: "```") are prohibited. You are converting code, so there is 0 need for backticks unless you are making comments with backticks.
"""


def portal():
    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description="Translate code from one language to another."
    )
    parser.add_argument("file_path", help="The path to the file to translate.")
    parser.add_argument("from_lang", help="The original language of the code.")
    parser.add_argument("to_lang", help="The language to translate the code into.")
    args = parser.parse_args()

    # Map languages to file extensions
    lang_to_extension = {
        "python": ".py",
        "javascript": ".js",
        "java": ".java",
        "c": ".c",
        "c++": ".cpp",
        "c#": ".cs",
        "ruby": ".rb",
        "swift": ".swift",
        "kotlin": ".kt",
        "typescript": ".ts",
        "php": ".php",
        "go": ".go",
        "rust": ".rs",
        "r": ".r",
        "scala": ".scala",
        "perl": ".pl",
        "bash": ".sh",
        "powershell": ".ps1",
        "html": ".html",
        "css": ".css",
        "sql": ".sql",
        "json": ".json",
        "xml": ".xml",
        "yaml": ".yaml",
        "markdown": ".md",
        "plaintext": ".txt",
        "restructured text": ".rst",
        "rst": ".rst",
        "gleam": ".gleam",
        "reason": ".re",
        "f#": ".fs",
        "crystal": ".cr",
        "htmx": ".htmx",
        "mojo": ".mojo",
        "": ".txt",  # Default to plain text
    }

    # Get the file extension for the target language
    file_extension = lang_to_extension.get(args.to_lang.lower(), ".txt")

    # Read the file content into a string
    with open(args.file_path, "r") as file:
        content = file.read()

    spinner = itertools.cycle(["-\n", "/\n", "|\n", "\\\n"])

    try:
        stream = ollama.chat(
            model="codellama",
            messages=[
                {
                    "role": "system",
                    "content": context
                    + f" You are converting code from {args.from_lang} to {args.to_lang}. You will be as accurate as possible.",
                },
                {"role": "user", "content": f"Code to convert:\n```\n{content}\n```"},
            ],
            stream=True,
        )
        with open(
            f"outputs/output_{args.file_path}{file_extension}", "w"
        ) as output_file:
            for chunk in stream:
                output_file.write(chunk["message"]["content"])
                output_file.flush()
                sys.stdout.write("Loading: " + next(spinner))  # Spin the spinner
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write("\033[A")  # Move the cursor up

        print(
            f"Translation complete! Check the outputs/output{file_extension} file for the translated code."
        )
    except KeyboardInterrupt as e:
        pass
