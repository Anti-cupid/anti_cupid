# Anti-Cupid
A beautiful end, just like its beginning.

This repository is an attempt to utilize and finetune LLM models to make judgements for court cases regarding divorce in South Korea.

The project is designed solely for educational purposes, and there is no intention of utilizing the data and subsequent models for commercial use.

## Installation
To use the Anti-Cupid directory, please clone via git, and then install it as an editable package.

1. **Clone the Repository**  
   First, clone the repository to your local machine:

   ```bash
   git clone https://github.com/Anti-cupid/Anti-Cupid.git

2. **Navigate to the Repository**  
    Navigate to the local repository directory.

    ```bash
    cd Anti-Cupid

3. **Install the Package in Editable Mode**  
    
    ```bash
    pip install -e .

4. **Confirm Installation**  
    If these steps are taken successfully, then this repository should be viewable as a package. This could be confirmed via:  
    
    ```bash
    python -c "import anti_cupid; print('Successfully imported Anti-Cupid')"

## Project Documentation
https://viridian-cloudberry-de0.notion.site/Anti-Cupid-Project-Documentation-ad2aa022a81e43d7a5b3fd3e165bfa96?pvs=4

## Data Information
### 이혼 판례 관련 데이터
https://casenote.kr

### 법전
4법/6법 법전 pdf (한국방송통신대학교 제공):
https://knou.ac.kr/bbs/law/2096/180952/artclView.do

## Algorithm
### Model
Currently, the base model being utilized for this project is the MLP-KTLim/llama-3-Korean-Bllossom-8B open-sourced Ko-LLM model provided by HuggingFace. Please refer to the following link for more details regarding the model.

https://huggingface.co/MLP-KTLim/llama-3-Korean-Bllossom-8B

## Contributions
This project was a team project with equal contributions by jkpizza and pyupya.