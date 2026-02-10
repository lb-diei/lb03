# 📄 Document Template System

**Generate Professional DOCX Documents from Customizable Templates**



## What It Does

| Input | Output |
|-------|---------|
| Markdown Template | DOCX Document |
| User Variables | Formatted Content |
| Template Name | Ready-to-Use File |


## Quick Start

```bash
# Install dependencies
pip install python-docx

# List available templates
python document_generator.py -l

# Generate a document
python document_generator.py notice -o my_document.docx

# Generate with custom variables
python document_generator.py notice -o my_doc.docx -v title="My Title" -v author="John"
```


## Template Structure

```
lb03/
├── document_generator.py    # Main program
├── templates/              # Template directory
│   ├── government/        # Government documents
│   │   └── notice.md      # Notice template
│   ├── enterprise/        # Business documents
│   │   └── notification.md
│   ├── legal/             # Legal documents
│   │   └── contract.md
│   └── academic/          # Academic papers
│       └── paper.md
├── README.md
└── requirements.txt
```


## Available Templates

### Government Documents
| Template | Description |
|----------|-------------|
| notice | Official government notice |

### Enterprise Documents
| Template | Description |
|----------|-------------|
| notification | Internal company notification |

### Legal Documents
| Template | Description |
|----------|-------------|
| contract | General contract template |

### Academic Documents
| Template | Description |
|----------|-------------|
| paper | Academic paper/essay format |


## How to Create Templates

Create a Markdown file in `templates/` directory:

```markdown
# Document Title

[variables]
title: Default Title
author: Author Name
date: 2026-01-01

[content]
## Section 1
Your content here.

## Section 2
More content...
```

### Template Format

| Section | Purpose |
|---------|---------|
| `# Title` | Document title (appears as heading) |
| `[variables]` | Default variable values |
| `[content]` | Document body content |


## Usage Examples

### List All Templates

```bash
python document_generator.py -l
```

Output:
```
Available templates:
  - notice
  - notification
  - contract
  - paper
```

### Generate with Defaults

```bash
python document_generator.py notice -o output.docx
```

### Generate with Custom Variables

```bash
python document_generator.py notice \
  -o report.docx \
  -v title="Annual Report" \
  -v author="Finance Dept" \
  -v content="Quarterly financial summary..."
```


## Command Options

| Option | Description |
|--------|-------------|
| template | Template name (without .md) |
| -o, --output | Output filename (default: output.docx) |
| -l, --list | List available templates |
| -v, --variable | Add variable (key=value) |


## Add New Template

1. Create a `.md` file in `templates/` subdirectory
2. Follow the template format
3. Test with:

```bash
python document_generator.py your_template -o test.docx
```


## Requirements

| Package | Version |
|---------|---------|
| python-docx | >=1.1.0 |


## License

MIT License - Free to use and modify


## Author

Created with Claude Code
