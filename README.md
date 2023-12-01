# DoHMeter: features extraction automation

This module can extract features with the help of the module DoHMeter of DoHLyzer on multiple PCAP files in a specified folder and merge all the extracted features into a unique CSV file.

## Python environment installation

### DoHLyzer installation

First, install `tcpdump` with: `$ sudo apt install tcpdump`

Create a anaconda environment with Python version 3.6:
```
$ conda create -n DoHLyzer python=3.6
```

Activate the anaconda environment: `$ conda activate DoHLyzer`

Download the DoHLyzer tool on the GitHub repository or clone it with:
```
$ git clone https://github.com/ahlashkari/DoHLyzer.git
```

Add a `setup.py` file at the root of the folder of DoHLyzer with the following code:
```
#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="dohlyzer",
    description="Set of tools to capture HTTPS traffic, extract statistical and time-series features from it, and analyze them with a focus on detecting and characterizing DoH (DNS-over-HTTPS) traffic.  ",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ahlashkari/DoHlyzer",
    packages=find_packages(exclude=[]),
    python_requires=">=3.6",
    install_requires=open('requirements.txt').read().split('\n'),
    entry_points={
        "console_scripts": [
            "dohlyzer=meter.dohlyzer:main",
        ]
    },
)
```

Upgrade your version of pip:
```
$ python -m pip install --upgrade pip
```

Modify the `requirements.txt` file to have `scapy==2.4.3`.

Modify the file `DoHLyzer/meter/features/context/packet_flow_key.py` and replace the line `packet_direction.FORWARD` by `packet_direction.PacketDirection.FORWARD`.

Modify the file `DoHLyzer/meter/flow_session.py` at the line 103 and replace the number `120` by more (if it is huge pcap files, choose 20 000). Indeed, this causes flow splitting problems when flows are longer than 120 seconds.
Change also the condition with self.packets_count (if it is huge pcap files, choose 100 000).

In the `DoHLyzer` folder, process the installation by executing:
```
(DoHLyzer) $ pip install .
```

In case of modification of the files after installation, you need to make again the installation by executing again the previous command.

### Installation python packages

Install `pandas` version 1.0.5 with:

```
$ pip install pandas==1.0.5
```

## Usage

There are three options that you need to specify when running the script: the _DoHLyzer path_, the _PCAP files source folder_ and optionally, the _path of the merged file_.

The _destination path_ is specified by `-d [pathDoHLyzer]` 

The _PCAP files source folder_ is specified by using `-p [pcapFilesSourceFolder]`.

The _path of the merged file_ where we can choose the name of the merged CSV file by using `-o [pathMergedCSVFile]`. If the name is not precised, a default name will be used (merged.csv) and the merged file will be in the PCAP files source folder.

Example:
```
python3 dohmeter_automated.py -d /home/$USER/ -p /home/$USER/pcapFolder/ -o /home/$USER/Documents/features.csv
```
