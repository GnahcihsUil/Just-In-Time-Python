# Just-In-Time-Python

CS263 Team

## JIT in Python: Investigate and Extend Numba

Numba is a Just-In-Time (JIT) compiler for Python which excels in accelerating the widely used numerical computation library Numpy. In this project, we investigate Numba and extend it by adding a new supported type. However, instead of implementing a JIT compiler from scratch, Numba chose to convert Python bytecode to LLVM IR, and import the JIT compiler given by the LLVM toolchain to translate that LLVM IR to machine code. 

We investigate the source code of Numba to provide: 1, an overview of the stages of transferring native python byte code to LLVM Intermediate Representation (IR); 2, detailed investigation and explanation into type inference mechanism, before/after inference rewrites, phi node generation. Besides, we conducted an implementation part to extend Numba for the support of a new type.


## Steps for building/deploying project

### Required Packages
```
numpy
numba
```

### Environment

We only test it on Windows WSL. Hopefully, it should work on any X86_64 architecture.  Unfortunately, it does not work on ARM64 architecture (M1 Mac).

our test environment:
```
Unbuntu 20.04.3 LTS
python 3.8.10
numba 0.56.4
```
### Run Extend_LIF
```
cd Just-In-Time-Python
python3 src/Extend_LIF.py
```

### Alternative
Manually compile C++ file to use different compiler or optimization level, for example:
```
g++ -O3 -shared -0 src/LIF_gcc_o.so src/LIF_cpp.cpp
```

