from models.file_model import FileModel


class AIService:

    def generate_new_filename(self, file: FileModel) -> str:
        """
        כאן ניתן לחבר ל-OpenAI / מודל אחר.
        כרגע דוגמה בסיסית.
        """

        if file.content:
            words = file.content.split()
            short_name = "_".join(words[:3])
            return short_name.lower()

        return file.name.lower()
