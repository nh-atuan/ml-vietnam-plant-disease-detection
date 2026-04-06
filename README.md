# Plant Disease Diagnosis System

This project is an end-to-end Machine Learning system for diagnosing diseases in Coffee and Rice leaves to support Vietnamese farmers.

## Quick Start

1. **Setup Environment**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train Model**:
   Follow `notebooks/04_model_training.ipynb` or run:
   ```bash
   python -m src.pipeline.train_pipeline
   ```

3. **Run API**:
   ```bash
   uvicorn app.api:app --reload
   ```

4. **Run UI**:
   ```bash
   streamlit run app.ui.py
   ```

## Architecture

- **Data**: Handled via `src/data/` with standardized transforms.
- **Models**: Includes Baseline (CNN), Custom CNN, and ResNet-18 (Advanced).
- **Deployment**: Containerized with Docker, ready for cloud deployment.
