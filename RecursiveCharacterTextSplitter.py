class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size=1000, chunk_overlap=100, separators=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", " ", ""]

    def split_text(self, text):
        chunks = self._split_recursive(text, self.separators)
        return self._merge_chunks(chunks)

    def _split_recursive(self, text, separators):
        # Base case
        if len(text) <= self.chunk_size:
            return [text]

        separator = separators[0]

        # If separator is empty, split character by character
        if separator == "":
            return [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]

        splits = text.split(separator)

        # If separator not found, try next separator
        if len(splits) == 1:
            return self._split_recursive(text, separators[1:])

        result = []
        for split in splits:
            if len(split) <= self.chunk_size:
                result.append(split)
            else:
                result.extend(self._split_recursive(split, separators[1:]))

        return result

    def _merge_chunks(self, chunks):
        merged_chunks = []
        current_chunk = ""

        for chunk in chunks:
            chunk = chunk.strip()

            if not chunk:
                continue

            if len(current_chunk) + len(chunk) + 1 <= self.chunk_size:
                current_chunk += (" " if current_chunk else "") + chunk
            else:
                if current_chunk:
                    merged_chunks.append(current_chunk)

                if self.chunk_overlap > 0 and merged_chunks:
                    overlap_text = current_chunk[-self.chunk_overlap:]
                    current_chunk = overlap_text + " " + chunk
                else:
                    current_chunk = chunk

        if current_chunk:
            merged_chunks.append(current_chunk)

        return merged_chunks
    
text = """
LangChain is a framework for building LLM applications.

Recursive text splitting is useful for RAG pipelines.
It tries to split text by paragraphs first, then lines, then words, then characters.

This helps preserve meaning better than simple character splitting.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=80,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}:")
    print(chunk)
    print("-" * 40)    