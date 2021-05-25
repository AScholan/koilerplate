# koilerplate - boilerplate code for kaggle

![PyPI](https://img.shields.io/pypi/v/koilerplate)
![PyPI - License](https://img.shields.io/pypi/l/koilerplate?style=flat)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/koilerplate)
![PyPI - Format](https://img.shields.io/pypi/format/koilerplate)
![PyPI - Status](https://img.shields.io/pypi/status/koilerplate)
![Read the Docs](https://img.shields.io/readthedocs/koilerplate)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

One of my great frustrations when building notebooks for [kaggle](https://kaggle.com) 
is the amount of boilerplate code I always add to the top of each notebook.

The whole idea behind this package is that a simple import can pull in a lot of this
boilerplate and allow me to focus on the competition in hand.

---
## folders

The **folders** module defines some simple constants that can be used as the root names
for the three primary folder paths used in Kaggle.

These are all defined relative to the working folder (which for a standard kaggle 
notebook is the _/kaggle/working_ folder). 

This module is also OS agnostic. This means that it's possible to download and use
the notebook outside kaggle. If this is the case then it will define the folders 
relative to your local project working folder. For example:

```text
c:\
  ├── dev                     # Somewhere you put all your project files
  .   ├── kaggle-projects     # You put all your kaggle projects here
  .   .   ├── input           # Put downloaded datasets here "INPUT_ROOT"
  .   .   ├── my-competition  # Your competition notebook in here "WORKING_ROOT"
          └── temp            # This is where temp files/folders will go "TEMP_ROOT"
```
### Usage
```python
from koilerplate import INPUT_ROOT, WORKING_ROOT, TEMP_ROOT

print(f"INPUT_ROOT={INPUT_ROOT}")
print(f"WORKING_ROOT={WORKING_ROOT}")
print(f"TEMP_ROOT={TEMP_ROOT}")
```
> INPUT_ROOT=/kaggle/input \
> WORKING_ROOT=/kaggle/working \
> TEMP_ROOT=/kaggle/temp

### Example kaggle notebook

- [koilerplate folders and zipout (public)](https://www.kaggle.com/andrewscholan/koilerplate-folders-and-zipout-public)

---
## zipout

The **zipout** folder is designed to overcome a limitation in the Kaggle working 
folder. There is an unspecified limit to the _number_ of files that can be placed 
in the working folder, and sub-folders of the working folder.

This means that if you are manipulating a dataset _it may fail silently_ if you 
place too many files in the folder, even if it is within the disk space quota defined
for the notebook.

To overcome this, the recommendation through the Kaggle forum is to first write the
files to a folder in /kaggle/temp and then zip up this folder and copy it to the
working folder. (The temp folder does not have this same restriction.)

This module contains a single python class **ZipOut** that does the heavy
lifting to accomplish this.

### Usage
```python
from koilerplate import ZipOut

# Create the temporary folder
my_dataset = ZipOut("my-dataset")

# Print out the path that was created
print(my_dataset.folder_path)
```
> /kaggle/temp/my-dataset
> 
```python
# Make a trivial file and place it into the folder
test_file_path = os.path.join(my_dataset.folder_path, "test.txt")
with open(test_file_path, "w") as f:
    for _ in range(1, 1000):
        f.write("Hello world!\n")
```
```python
# Convert the temporary folder into zip file
zip_file_path = my_dataset.make_zip_file()
print(zip_file_path)
```
>/kaggle/working/my-dataset.zip

### Example kaggle notebook

- [koilerplate folders and zipout (public)](https://www.kaggle.com/andrewscholan/koilerplate-folders-and-zipout-public)

---
## pushover

Pushover is a subscription based notification service: [pushover](https://pushover.net/)

The service [pricing](https://pushover.net/pricing) is trivially inexpensive (at 
the time of writing a one off payment of USD 5.00 per platform; I have subscribed
only for my phone).

On an internet enabled workbook you can use this to notify you of steps that are
occurring during a notebook run on the Kaggle servers (or elsewhere).

To use the service you need to set up an account on _pushover.net_ and obtain from
your account settings an API token and your user id.

### Usage

Create yourself a _**private**_ dataset called **pushover-credentials** which should 
consist of a single file called **pushover_credentials.json** (note underscore in
filename) which has the following structure:
```json
{
  "token": "<<<<<--- Your token hex code string --->>>>>"
  "user": "<<<<<--- Your user hex code string --->>>>>"
}
```
Now, add this dataset to your competition notebook. You're now all set up to use
pushover in your notebook.
```python
# Optionally define this before importing koilerplate
NOTEBOOK_NAME = "My competition notebook"

from koilerplate import pushover

# Send a notification
pushover("Hello Kaggle World!")
```
### Example kaggle notebook

- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Sorry, none yet.

## offline

Often, in code competitions on Kaggle, the notebook submission has to be run without
internet access. This is usually to stop notebooks handing off tasks to an external
processor farm. Usually, these competitions permit the use of external datasets and
libraries.

However, it is a non-trivial matter using a library that's not included in the standard
notebook image. You need to build yourself a custom dataset containing all the 
information that's needed for _pip_ to load them into your notebook whilst it's
running without an internet connection.

The **offline** module is designed to take the legwork out of preparing the dataset
that you will need to load the modules off-line. It contains a single function
_**offline_pip_prepare()**_ which will copy the modules needed into the WORKING folder
so that they can be uploaded to kaggle as a dataset.

## Usage

In this example we're going to prepare the libraries to be loaded as a specific verison
of PyTorch plus the very good cell segmentation library 
[cellpose](https://www.cellpose.org/). If we look at the install instructions for 
these libraries then we would see the recommended installion scripts for both are:

<pre>
pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 \
    --find-links https://download.pytorch.org/whl/torch_stable.html

pip install cellpose==0.6.1
</pre>

In order to prepare these for offline loading we have to note the module names and
versions and any locations where _pip_ should find links from. These should be each
placed into a list and these passed as parameters to the _**offline_pip_prepare()**_
function.

#### In a kaggle internet enabled notebook enter the following code cell:

```python
from koilerplate import offline_pip_prepare

PACKAGES = [
    "torch==1.7.1+cu110",
    "torchvision==0.8.2+cu110",
    "torchaudio==0.7.2",
    "cellpose==0.6.1",
]
LINKS = [
    "https://download.pytorch.org/whl/torch_stable.html"
]

offline_pip_prepare(packages=PACKAGES, links=LINKS)
```

_Note that this will take some time to run, as the function downloads the necessary
installation information and, if necessary, builds the wheel files that **pip** will 
use._

After the cell completes the WORKING folder will contain the following:

```text
/
└── kaggle
      ├── working                   # Working folder of your kaggle notebook
      .   ├── requirements.txt      # requirements file that you will use with pip
      .   └── wheels.zip            # the offline wheels files that pip will use
```
Once this is completed you need to save the notebook as a new version; Kaggle will
then execute your notebook in another kernel. Wait for this to finish then navigate
to the output section of the notebook and create a new dataset, call it, for example,
_competition-packages_. _Note that the above example produces a dataset of approximate
size 1.2GB._

Now, start a new notebook that will become your competition entry notebook and add
to it your newly created dataset. You will now see that this appears in your input
folder for the notebook _(note that kaggle will drop the hyphen in the dataset name)_:

```text
/
└── kaggle
      ├── input                     # Kaggle loads all datasets here
      │   ├── competitionpackages   # This is your newly created dataset
      │   .   ├── requirements.txt  # requirements file that you will use with pip
      │   .   └── wheels
      │           ├── ... .whl      # the offline wheels files that pip will use
      │           └── ... .whl      
      └── working                   # Working folder of your kaggle notebook
```
You now need to add the following code cell somewhere near the start of your competition
notebook:

```jupyter
!pip install \
   --requirement /kaggle/input/competitionpackages/requirements.txt \
   --no-index \
   --find-links file:///kaggle/input/competitionpackages/wheels
```
_Note that it's very important to include the **--no-index** flag or this will not 
work when the internet access for the notebook is disabled._

Don't forget that you also need to **import** the libaries, as you normally would,
before you use them:

```python
import torch
import cellpose
```
### Example kaggle notebooks/datasets

- Notebook describing process: [koilerplate offline (public)](https://www.kaggle.com/andrewscholan/koilerplate-offline-public)
- Example dataset using process: [competition-packages](https://www.kaggle.com/andrewscholan/competitionpackages)
- Example competition notebook: [koilerplate offline pip install example](https://www.kaggle.com/andrewscholan/koilerplate-offline-pip-install-example)

---
## Suggestions

Please add any suggestions to the [issue tracker](https://github.com/AScholan/koilerplate/issues)
and I'll try and get back to you.

# License

This is licensed under the MIT license. See LICENSE.txt for details.
