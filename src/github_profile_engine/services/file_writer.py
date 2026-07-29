from github_profile_engine.models.generated_file import GeneratedFile


class FileWriter:
    @staticmethod
    def write(file: GeneratedFile) -> None:
        file.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file.path.write_text(
            file.content,
            encoding="utf-8",
        )
