﻿# GfS-RAGmap
## 1. Prerequisites
- Python >= 3.10
- Conda (Anaconda or Miniconda)
- Git

## 2. Install Conda (if not installed)
Download from [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution)
And follow the instructions provided by official websites.

## 3. Create and activate conda environment
```bash
conda create -n gfsproj python=3.10
conda activate gfsproj
```
After activating conda environment, most dependencies can be use "pip" command to install into the current conda environment.
## 4.1 Install dependencies
Clone the repository and navigate to the directory "GfS-RAGmap", 
install PyTorch first(please install according to ypur system configuration), see details at website (https://pytorch.org/get-started/previous-versions/)
For example, for CUDA 11.8 and Python 3.10::
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
or for cpu use only:
```bash
pip install torch torchvision torchaudio
```
And install all common dependencies, run:
```bash
pip install -r requirements.txt
```
## 4.2 Install dependencies (without requirements.txt)
Or you might not wish to use requirements.txt or there are errors. Manual installation is also feasible.
Install faiss library, using cpu or gpu (if accessiable).
```bash
conda install faiss-cpu
conda install faiss-gpu
```
Install Oracle connection library (oracle client and cx_Oracle)
Download Oracle Instant Client from https://www.oracle.com/database/technologies/instant-client.html
```bash
conda install -c conda-forge cx_oracle
```
Install random number generation library, used for random sampling in auto evaluation.
```bash
pip install random
```
Install RAGAs evaluation framework
```bash
pip install ragas
```
Install openai library, used for send API requests
```bash
pip install openai
```
Install pandas, used for password retrieval and query construction
```bash
pip install pandas
```
Install Gradio, used for front-end demonstration
```bash
pip install gradio
```
Install time library, used for output time counting
```bash
pip install time
```
Install Folium, for map creation
```bash
pip install Folium
```
Install sentence transformer, which integrates various open-source models.
```bash
pip install sentence-transformers
```
Install pytorch, which supports CUDA accerleration. Recommend installing PyTorch via Conda, as it provides better compatibility with CUDA (for GPU acceleration) and handles dependencies more reliably than pip. For GPU-enabled environments (e.g., with CUDA 11.8), run:
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```
or only need the CPU version, use:
```bash
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```
## 5. Path configuration
The paths to api keys, oracle passwords, vector database and metadata need to be configurated.
The path constructions can be found in chatgptProcess.py, deepseekProcess.py, database_query, retrieval_agent.py

## 6. Run front-end demonstration
The module FrontTest will call the main function to do multi-turn dialogue (without memory), run:
```bash
python FrontTest,py
```

## 7. Run performance assessment
The performance assessment involves test samples generating, self answering and RAGAs assessing. The whole process is automatic, run:
```bash
python auto_eval.py
```
