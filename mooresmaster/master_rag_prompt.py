import os

def create_master_rag():
    base_dir = '/Users/katsumi.sato/RiderProjects/mooresmaster/mooresmaster.Generator'
    ignore_files = [
        "AssemblyInfo.cs",
        "AssemblyAttributes.cs",
        "FastNoiseLite.cs",
        "GlobalUsings.g",
        "Library",
        "Dependencies",
        "MessagePack",
        "moorestech-client-private",
        "lilToon",
        "DOTween",
        "moorestechInputSettings",
    ]

    # 対象のディレクトリ名を指定してください
    result_prompt = ""
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if any(ignore_file in file for ignore_file in ignore_files):
                continue
            if any(ignore_file in root for ignore_file in ignore_files):
                continue

            if file.endswith('.cs'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_dir)
                result_prompt += f"{relative_path}\n"
                result_prompt += "```cs\n"
                with open(file_path, 'r', encoding='utf-8') as f:
                    result_prompt += f.read()
                result_prompt += "```\n"

    return result_prompt

if __name__ == "__main__":
    create_master_rag()
