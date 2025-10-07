# Day 11: Model Optimization and Inference Speed Benchmarking

## Overview
This project demonstrates model optimization by comparing the inference speed of two popular transformer models: **BERT (bert-base-uncased)** and **DistilBERT (distilbert-base-uncased-finetuned-sst-2-english)**. The experiment benchmarks their performance on a sentiment analysis task using the Hugging Face `transformers` library.

## Learning Topics
- Model Optimization
- DistilBERT vs BERT speed comparison
- Caching models for faster inference

## Practical Task
- Compare inference time for 50 sentences using both models
- Log performance results in a JSON file

## Code Summary (`main.py`)
- **Model Initialization:**
  - Loads BERT and DistilBERT sentiment analysis pipelines (cached in memory for efficiency).
- **Data Preparation:**
  - Uses 5 sample sentences, repeated 10 times to create a list of 50 sentences.
- **Benchmarking:**
  - For each model, measures the inference time (in milliseconds) for each sentence.
  - Results are stored as a list of dictionaries, each containing the model name, sentence, and inference time.
- **Results Logging:**
  - All results are saved to `day11_inference_results.json` for further analysis.

## Results Summary
- **BERT (bert-base-uncased):**
  - Average inference time per sentence: ~13 ms (after initial warm-up, first call is slower)
- **DistilBERT (distilbert-base-uncased-finetuned-sst-2-english):**
  - Average inference time per sentence: ~8 ms
- **Observation:**
  - DistilBERT is significantly faster than BERT for single-sentence inference, confirming its suitability for latency-sensitive applications.

## How to Run
1. Ensure you have Python and the `transformers` library installed.
2. Run `main.py`:
   ```bash
   python py_day11/main.py
   ```
3. Results will be saved in `py_day11/day11_inference_results.json`.

## Files
- `main.py`: Benchmarking script
- `day11_inference_results.json`: Inference time results

## References
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/index)
- [BERT Paper](https://arxiv.org/abs/1810.04805)
- [DistilBERT Paper](https://arxiv.org/abs/1910.01108)

