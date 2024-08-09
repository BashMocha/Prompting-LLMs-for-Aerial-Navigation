## Prompting Large Language Models for Aerial Navigation
<b>Official implementation of the [UBMK 2024](https://ubmk.org.tr/) paper.</b>

Emirhan Balcı*, Barış Ata, Mehmet Sarıgül

[Demonstration](https://youtu.be/A9pKyYRqVNo)
## Abstract
Robots are becoming more prevalent and consequently utilized in numerous fields due to the latest advancements in artificial intelligence. Recent studies have shown promise in the human-robot interaction where non-experts are capable of handling the collaboration with robots. Whereas traditional interaction approaches are compact and rigid, natural language communication offers a coherent approach that allows interaction to be more versatile. The utilization of large language models (LLMs) makes it possible for non-expert users to take place in human-robot communications and manipulate robots to perform complex tasks such as aerial navigation, obstacle avoidance, and pathfinding. In this paper, we performed an experimental study to compare the performances of LLMs based on the generated source code from prompts to perform aerial navigation tasks in a simulated environment. The few-shot prompting technique is applied to LLMs such as ChatGPT, Gemini, Mistral, and Claude on Microsoft's AirSim drone simulation. We defined three test cases based on UAV-based aerial navigation, specified model prompts for each test, and extracted ground-truth trajectories for the test cases. Finally, we tested the models on the simulator with predefined prompts to compare the predicted trajectories with ground truth. Our findings indicate that no single model surpasses all test cases, using LLMs for aerial navigation remains a challenging task in robotic applications.


## Prerequisites
> [!IMPORTANT]
> The project was written/tested on Windows. Thus, it does not guarantee functionality on other operating systems,
> and it is recommended to run it on Windows.

- Prior to initiating the AirSim integration, it is essential to configure your API keys to enable access to the necessary models.
- Create a conda environment and install the AirSim client.
- Create the conda environment for a controlled and isolated space.
```
conda env create -f environment.yml
```
- Activate the environment and install the AirSim client.
```
conda activate llm-env
pip install airsim
```
- Clone the repository.
```
git clone https://github.com/CheesyFrappe/Prompting-LLMs-for-Aerial-Navigation.git
```
- Copy the API keys and paste them in the `API-KEY` field of the `./src/config.json` file.
- Download the simulation environment from [Releases](https://github.com/CheesyFrappe/Prompting-LLMs-for-Aerial-Navigation/releases/), and unzip the package.
- Copy `settings.json` to `C:\Users\<username>\Documents\AirSim\`.
- It is recommended to consult the [documentation](https://microsoft.github.io/AirSim/unreal_custenv/) for additional information on custom simulation environments if needed.

## Usage
- Execute the AirSim simulation by running ```.\run.bat``` from the simulation folder.
- Once the simulation is up and running, run the source file for the model being used.
```
python chatgpt_airsim.py \
  --testname first_test
  --model gpt-3.5-turbo
```
- The recording feature is enabled by default in this project. The trajectories can be found in `C:\Users\<username>\Documents\AirSim\`.
- Execute ```evaluation.py``` to obtain the results and plot the trajectories.
```
python evaluation.py \
  --reference_path ../dataset/first_test.txt
  --predicted_path <path-to-predicted-trajectory>
```



<!--- https://github.com/CheesyFrappe/Prompts-for-Robotics/assets/80858788/d4ef9ece-b2d5-49e3-a1dc-934031be7a6e --> 

Feel free to [contact](mailto:emirbalci360@gmail.com) for any questions.
