## 📌 Dataset Description
The dataset will be published on [Zenodo](https://zenodo.org/) and will be freely available for research purposes.

## ⚙️ Training Models
This project refers to the following open-source models during experiments to validate the effectiveness of the dataset.

- **Event Extraction**:
  - [DuEE](https://github.com/jxlin98/DuEE)  
    We use their provided code to train the model, but with tuned parameters; the details are described in our paper.
  - [DEGREE](https://github.com/PlusLabNLP/DEGREE)  
    We use their provided code to train the model, but with tuned parameters; the details are described in our paper.

- **Entity & Relation Extraction**:
  - [DeepKE](https://github.com/zjunlp/DeepKE)  
    We use their provided code to train the model, but with tuned parameters; the details are described in our paper.

## 📝 Annotation Tool
Data annotation is conducted using [Doccano](https://github.com/doccano/doccano).  
We further use custom scripts to process the annotated data into a format suitable for model training.
