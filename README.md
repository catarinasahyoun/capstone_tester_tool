# Capstone_Biochar_Tool
biochar-brazil
├── src                     # Source code for the application
│   ├── __init__.py        # Initializes the src package
│   ├── main.py            # Entry point for the application
│   ├── cli.py             # Command-line interface for user interactions
│   ├── config.py          # Configuration management
│   ├── data               # Data handling modules
│   │   ├── loader.py      # Functions to load data
│   │   ├── downloader.py   # Functions to download datasets
│   │   └── preprocessing.py # Data cleaning and preparation
│   ├── analysis           # Analysis modules
│   │   ├── suitability.py  # Suitability scoring logic
│   │   ├── risk_assessment.py # Risk assessment for biochar application
│   │   └── aggregation.py  # Aggregation of suitability scores
│   ├── models             # Models for analysis
│   │   ├── spatial_model.py # Spatial models for geospatial analysis
│   │   └── ml_model.py     # Machine learning models
│   ├── visualization       # Visualization modules
│   │   ├── map_renderer.py  # Interactive map rendering
│   │   └── plots.py        # Plotting functions
│   └── utils              # Utility functions
│       ├── geospatial.py   # Geospatial utility functions
│       └── io.py          # Input/output utility functions
├── notebooks               # Jupyter notebooks for exploration and modeling
│   ├── 01-data-exploration.ipynb
│   └── 02-modeling-workflow.ipynb
├── data                    # Data directories
│   ├── raw                # Original datasets
│   ├── processed          # Cleaned datasets
│   └── external           # External datasets
├── docs                    # Documentation
│   ├── functional_flow.md  # Functional flow of the application
│   └── architecture.md     # Architecture and design decisions
├── tests                   # Unit tests
│   ├── test_data_loader.py
│   └── test_suitability.py
├── scripts                 # Automation scripts
│   ├── fetch_data.sh      # Script to fetch datasets
│   └── run_pipeline.sh     # Script to run the analysis pipeline
├── configs                 # Configuration files
│   ├── config.yaml        # Application configuration
│   └── logging.yaml       # Logging configuration
├── .github                 # GitHub workflows
│   └── workflows
│       └── ci.yml         # Continuous integration workflow
├── Dockerfile              # Docker image instructions
├── pyproject.toml         # Project dependencies and settings
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore file
├── LICENSE                 # Licensing information
└── README.md               # Project overview and instructions
