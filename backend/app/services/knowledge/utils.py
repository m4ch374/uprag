class KnowledgeUtils:
    @staticmethod
    def is_valid_file_type(file_type: str):
        # uncomment if you want to play with other file types
        return file_type in [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            # "application/pdf",
            # "text/plain",
            # "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            # "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            # "text/xml",
        ]

    @staticmethod
    def get_rag_index_name(user_id: str):
        return f"rag-{user_id.replace('_', '-').lower()}"
