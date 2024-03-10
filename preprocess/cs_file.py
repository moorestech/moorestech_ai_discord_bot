import os

MOORESTECH_PATH = "/Users/sato-katsumi/moorestech"


def get_cs_files():
    results = []
    ignore_files = [
        "AssemblyInfo.cs",
        "AssemblyAttributes.cs",
        "FastNoiseLite.cs",
        "GlobalUsings.g",
        "Library",
        "MessagePack",
        "moorestech-client-private",
        "lilToon"]

    for root, dirs, files in os.walk(MOORESTECH_PATH):
        for file in files:
            if any(ignore_file in file for ignore_file in ignore_files):
                continue
            if any(ignore_file in root for ignore_file in ignore_files):
                continue

            if file.endswith(".cs"):
                cs_source_code = open(os.path.join(root, file), "r", encoding="utf-8").read()

                results.append(
                    {
                        "actual_path": os.path.join(root, file),
                        "relative_path": os.path.relpath(os.path.join(root, file), MOORESTECH_PATH),
                        "file_name": file,
                        "content": cs_source_code
                    }
                )

    # パスでソート
    results.sort(key=lambda x: x["relative_path"])
    return results


if __name__ == "__main__":
    cs_files = get_cs_files()
    for cs_file in cs_files:
        print(cs_file["content"])