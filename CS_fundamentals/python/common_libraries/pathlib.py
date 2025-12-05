from pathlib import Path

p = Path("example.txt")
text = p.read_text()
p.read_bytes()
p.write_bytes(b'hello')
p.write_text("Hello, world!")
p.exists()
p.is_file()
p.is_dir()

data_dir = Path("data_dir")
file_path = data_dir / "example.txt" # concatenates the file path
for file in Path("data").iterdir():
    # …
    pass