# Label Studio Project Tool

A Streamlit application for managing Label Studio projects - export, combine, and merge multiple projects efficiently.

## Features

- **Lazy Project Loading**: Projects are loaded on-demand to improve performance
- **Accurate Annotation Counting**: Get precise counts of tasks and annotations per project
- **Label Config Compatibility Check**: Verify projects can be merged before export
- **Efficient Export Methods**: Stream or snapshot export options
- **Field Rewriting**: Transform data fields during export (rename, prefix URLs, regex)
- **Smart Deduplication**: Remove duplicate tasks based on configurable fields
- **Progress Tracking**: Real-time progress indicators for long operations
- **Project Merging**: Combine multiple projects into a new project

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Usage

### 1. Connect to Label Studio
- Enter your Label Studio URL (e.g., `http://localhost:8080`)
- Provide your API key (Personal Token)
- Click "Connect"

### 2. Load Projects
- Click "Load Projects" to fetch available projects
- Projects are loaded on-demand for better performance

### 3. Select Projects for Merging
- Choose 2 or more projects from the multiselect dropdown
- Click "Get Detailed Counts" to see accurate task/annotation counts
- Use "Check Label Config Compatibility" to ensure projects can be merged

### 4. Configure Export Options
- Choose between stream or snapshot export
- Configure field rewriting if needed:
  - **Key Renames**: Transform field names (e.g., `file_upload:image`)
  - **URL Prefixes**: Add base URLs to file paths
  - **Regex Replace**: Pattern-based field transformations
- Set deduplication field (optional)

### 5. Export and Merge
- Click "Export selected ➜ Apply rewrites ➜ JSON" to process projects
- Review merged results and download JSON if needed

### 6. Create Merged Project
- Set project title and description
- Configure import batch size
- Click "Create project & import merged tasks"

## Performance Tips

- Use snapshot export for large projects (>10K tasks)
- Increase batch size for faster imports (up to 50K)
- Use deduplication to avoid importing duplicate tasks
- Check label config compatibility before exporting

## Troubleshooting

### Common Issues

1. **Slow Loading**: Use "Load Projects" button instead of automatic loading
2. **Export Failures**: Check Label Studio connectivity and API permissions
3. **Memory Issues**: Use snapshot export for very large projects
4. **Import Errors**: Verify label config compatibility between projects

### Performance Optimization

- The app uses caching to avoid re-fetching project data
- Session state preserves exported data between operations
- Progress indicators show real-time status for long operations

## Requirements

- Python 3.8+
- Streamlit 1.28+
- Label Studio SDK 0.0.34+
- Access to Label Studio instance with API key