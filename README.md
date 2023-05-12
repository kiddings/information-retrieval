# Usage of InnocentTrap
## First step: Dataset Downloading
In order to run the watermarking, first you need to download the datasets FashionMNIST and CIFAR10. Or you can download them through torchvision.
## Second step: Train an original model
The second step is to train a original model used to embed the watermark. Note that the network structure in this code must be used, because the network structure defined in this code contains some necessary operations needed for cropping.
   ```python
   python model_train.py --model_name ResNet18 --data_name CIFAR10 --size 64
   # size refers to the size of input image
   # you can also determine the epochs, batch and learning rate by using --epochs, --batch and --lr, respectively
   ```
## Third step: Watermark Embedding
Run the script watermarking.py to embed a watermark into the model from the previous training step.
```python
   python watermarking.py --model_name ResNet18 --data_name CIFAR10 --size 64
   # size refers to the size of input image
```
We take an interactive approach to allow the user to specify a pair of source and target labels. The above script runs and outputs suggestions for the specified labels, and the user can select a pair of labels accordingly.
