## Gym Malmo 
A collection of Mincraft based environments for conducting reinforcement learning experiments under partial observability. 

#### *Update*
This repository in addition to implementing minecraft environments, also implements an "experiment" runner that manages a fixed number of open malmo clients and allows batches of experiments to share this pooled resource. It also implements logging and organization of model outputs, a database for viewing experiments, and a telegram bot for getting updates on these experiments. In the future I will be releasing this experiment runner in a stand-alone package for benchmarking RL agents in an efficent manner. For my most recent projects I have migrated to the VizDoom environment. 

#### Partial Observability 

In recent years, reinforcement learning agents have achieved above human performance 
in a variety of competitive domains such as Atari and Go. These environments and others in recent literature 
have been fully observed such that the agent can view at every step all aspects of the environment state. 
Existing frameworks such as the OpenAI gym do not offer experimental environments that focus on 
partially observability.

This package provides a collection of tasks which focus on evaluating agent's performance in partially observed
environments where reward functions are non markovian. 


#### Difference from similar packages 

This repo is loosely based on code from 
[gym_minecraft](https://github.com/tambetm/gym-minecraft) and follows some of the design elements from
[marLo](https://github.com/crowdAI/marLo) however the key difference is that it allows for user generated state 
observations. This package exposes a handler that allows for the parsing of the world state into a 
custom feature vector. Therefore models can be evaluated both as "grid worlds" and using visual inputs for a given 
environment.

Additionally this package wraps [Malmo](https://github.com/Microsoft/malmo) into a vectorized environment used by 
the [Open AI Baselines](https://github.com/openai/baselines) allowing batched observations from multiple game engines. 

#### Setup 
This package requires project [Malmo](https://github.com/Microsoft/malmo) a Minecraft based reinforcement learning engine. 
I have had considerably difficulty installing this on Mac OS so I figured I would share my lessons here. The following instructions
are for Python 3.6 on Mac OSX. 

* Install Java 
    * `brew cask install java8`
*  Download and extract the Malmo repository: 
    *  `git clone https://github.com/Microsoft/malmo.git`
*  Install the python client via this conda formula:
    
```
    # from https://github.com/Microsoft/malmo/issues/664
    # Env setup
    conda create python=3.6 --name malmo # you are free to replace '2.7' with python '3.5' or python '3.6' 
    source activate malmo
    conda config --add channels conda-forge
    
    # Install malmo
    conda install -c crowdai malmo
    
    # Test the malmo 
    python -c "import MalmoPython" #for use of the Python API
    malmo-server -port 10001 # For launching the minecraft client
```
*  Set the `MALMO_XSD_PATH` to be the folder that you extracted Malmo into. 
   * eg `export MALMO_XSD_PATH=MalmoPlatform/Schemas`
   
* You should now be able to run the Malmo Client from command-line `./MalmoPlatform/Minecraft/LaunchClient.sh` and connect
  to it from python. You can test it out via the examples provided in the Malmo Repository.
  
  ```
    # We can run one of the basic tutorial scripts to check everything
    # is working properly.
    python MalmoPlatform/Python_Examples/tutorial_1.py

  ```
* We can then install dependencies: 
    ```
        conda install tensorflow gym
    ```
* And the Open AI baselines: 
    ```
       git clone https://github.com/openai/baselines.git
       cd baselines
       
       # make sure you install all additional  
       # dependancies for the baselines. 
       python setup.py install
    ```
##### Using the Experiment Manager
   Within this project there is a service for managing experiments and sending push notifications 
   about their performance to the popular messaging service Telegram. 
   If you would like to use this service you will need to install additional packages.     
 
#### Running 

In order to run the minecraft client on a machine in a headless mode, you can use the following command. 


```
xvfb-run -a -e /dev/stdout -s '-screen 0 1400x900x24' ./launchClient.sh
```

#### Running on CSLab Machines at U of T

Make sure the following environment vars are set correctly. 
```
export PYTHONPATH="~/gym_malmo"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/pkgs_local/cuda-9.0/lib64
export CUDA_HOME=/pkgs_local/cuda-9.0/
```


