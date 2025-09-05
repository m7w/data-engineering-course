📦 customs_data

A lightweight Python package for fetching customs data and exporting it to customs_data.csv.
Designed for internal workflows, with both CLI and programmatic interfaces. 

🚀 Installation & CLI Usage

After building and installing the package locally: 
```bash
pip install dist/customs_data-0.1.0-py3-none-any.whl
```

You’ll gain access to the customs-fetch command:
```bash
customs-fetch
```

This will:
- Fetch customs data from the API
- Save it as customs_data.csv in the current directory
- Print a confirmation message

🧪 Example Usage via Python Script

Alternatively, you can use the package directly in your own scripts. A ready-to-run example is
provided:
```bash
python examples/run.py
```

This script:
- Imports the fetch_data() function from the package
- Executes the data retrieval logic
- Creates customs_data.csv in the same directory

🛠️ Notes
- The output file is overwritten on each run.
- API pagination and batching are handled internally.
- For newline consistency, the CSV is written with CRLF for cross-platform compatibility.
