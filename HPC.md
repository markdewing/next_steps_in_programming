The current (fall of 2019) and future machines are all based around GPU acceleration from different vendors (Summit, Aurora, and Frontier).
There two major consequences on programming for such machines.

### Denoting offloaded code in the source
Portions of the source need to be marked for cross-compiling and execution on the accelerator.
Unlike Blue Gene, for which the entire code is cross compiled, only sections of the code are cross-compiled for GPU's.
Approaches for marking this code fall into
1. Separate code for the accelerator code - CUDA and OpenCL use this approach.
2. C++ lambdas - This is a solution that stays in the host language - Kokkos and Sycl are examples.
3. Pragmas - OpenMP and OpenACC use this

### Data movement
GPU accelerators have a separate memory that is smaller than main node memory, and there is a latency for moving memory contents to the GPU.
This latency needs to be accounted for in high performing applications.
Programming models must add some metadata to the memory locations to know what needs to be where and when.
1. CUDA and OpenCL explicitly manage locations and data copies.
2. Encoding the location in the type - Kokkos and Sycl use this
3. More pragmas for OpenMP and OpenACC


## Comparing programming models
For my own learning, I'm collecting implementations of kernels in various programming models.
The repository is [QMC kernels](https://github.com/markdewing/qmc_kernels).
The kernel with the most implemented variants is the vector add example.
It's the simplest kernel and the most basic place to start understanding the different models.


## Desired approach
These approaches are frustating because the compiler and runtime system should know exactly what memory needs to be where.
Instead an application could be written in a task-based data-flow style.
The chunks of code that could be offloaded are already identified (tasks) and data flow would make it easier to model the data movement.

I'm imagining something like Implicit Reference to Parameters in Fortran (IRPF) to describe each task.
From the set of statements in a function, the compiler already knows what values are read and written - writing the function signature is redundant.
The program graph can be constructed in a data-flow manner by connecting the names between tasks.
