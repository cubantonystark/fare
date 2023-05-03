# F.A.R.E
## Fast Area Rendering at the Edge

### Requirements

- An NVIDIA GPU.
- __[Git](https://git-scm.com/downloads)__.
- A __C++14__ capable compiler. The following choices are recommended and have been tested:
  - __Windows:__ Visual Studio 2019 or 2022
- A recent version of __[CUDA](https://developer.nvidia.com/cuda-toolkit)__. The following choices are recommended and have been tested:
  - __Windows:__ CUDA 11.5 or higher
- __[CMake](https://cmake.org/) v3.21 or higher__.
- __[Python](https://www.python.org/) 3.7 or higher__ for interactive bindings. Also, run `pip install -r requirements.txt`.
- __(optional) [OptiX](https://developer.nvidia.com/optix) 7.6 or higher__ for faster mesh SDF training.
- __(optional) [Vulkan SDK](https://vulkan.lunarg.com/)__ for DLSS support.
#### Clone this repo:<br>
```git clone https://github.com/cubantonystark/fare.git```
#### Change directory to the cloned repo:
```cd fare```
#### Next type: 
```install_neural_rendering.bat``` and hit ENTER
Then, use CMake to build the project: (on Windows, this must be in a [developer command prompt](https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-160#developer_command_prompt))
```sh
instant-ngp$ cmake . -B build
instant-ngp$ cmake --build build --config RelWithDebInfo -j
```
#### All dependencies should be installed after this step. Just double click in the ```fare.py``` file to start the server.
