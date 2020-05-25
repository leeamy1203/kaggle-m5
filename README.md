# Kaggle M5 Forecasting and Uncertainity

This repo explores two Kaggle competitions that are complementary. 
 - [M5 Forecasting - Accuracy](https://www.kaggle.com/c/m5-forecasting-accuracy/overview)
   - point estimate of the items that are sold
 - [M5 Forecasting - Uncertainty](https://www.kaggle.com/c/m5-forecasting-uncertainty/overview)
   - output probability distribution of those predictions
   
Both looks at the hierarchical sales data from Walmart to **forecast** daily sales for the next 28 days. 

Go to the [wiki](https://github.com/leeamy1203/kaggle-m5/wiki) for more details on the problem set and modeling work.

## Setup

### Tooling

- Install Python, minimum 3.7.5 ([pyenv](https://github.com/pyenv/pyenv) is the easiest way to install specific versions)
- Python Environment/Dependency Management via [poetry](https://python-poetry.org/) 
  - Install poetry - [instructions](https://python-poetry.org/docs/#installation)
- DVC for Data Pipeline Management
  - Install dvc - [instructions](https://dvc.org/doc/install/macos)
- Jupyter Notebook environment via Docker

A lot of opinions were pulled from [here](https://drivendata.github.io/cookiecutter-data-science/#directory-structure)

## General Usage

Because of the repository structure and poetry for dependency management, you can leverage auto-completion within the 
IDE and leverage that same code within the Jupyter Notebooks. In addition, the python packages you pull in will be the
same versions between your IDE and the Jupyter Notebook.

### Configure IDE for Usage

If using PyCharm, you'll need to set the project interpreter as the virtualenv that was created when getting 
dependencies installed. To do this, run `poetry env list --full-path` to get the full directory path of the 
Python environment.

### Configure Jupyter Notebook

Navigate into the root of the cloned directory, and run `docker-compose up` to launch a Jupyter Notebook server. If you
change any dependencies through poetry, you'll need to rebuild the container via `docker-compose build`. 

Note that the Jupyter notebook by default sets the root to be the repository root, so all files that are used for notebook
development should be within the repository. 

If you'd like to have a different port for your Jupyter server, you can run `JUPYTER_PORT=<new port> docker-compose up`
to use whatever port you'd like. The default messaging will still say port 8888, but it's allocated to whatever port
you pass in.

#### Use `src` in notebooks

Leverage the following code snippet to use the `src` directory in notebooks

```python
import sys
# This should navigate to the repository root
sys.path.append('../')

%reload_ext autoreload
%autoreload 2
```

## Data Gathering
All data are obtained from the kaggle website [here](https://www.kaggle.com/c/m5-forecasting-uncertainty/data)
- calendar.csv - Contains information about the dates on which the products are sold.
- sales_train_validation.csv - Contains the historical daily unit sales data per product and store [d_1 - d_1913]
- sample_submission.csv - The correct format for submissions. Reference the Evaluation tab for more info.
- sell_prices.csv - Contains information about the price of the products sold per store and date.
- sales_train_evaluation.csv - Available once month before competition deadline. Will include sales [d_1 - d_1941]

See under `notebook/exploratory/0.1-alee-initial-eda.ipynb` for details about each of these files.

## DVC Pipeline

