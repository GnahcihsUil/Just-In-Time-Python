##### What Numba does

Look at the Python bytecode, analysis it and change it into LLVM IR, then call LLVM to interpret IR into machine code and utilize it's optimization.

Basically, Numba add type to each of the variables to get the acceleration.



##### What Numba has



##### Compiler Stages

Numba @jit decorator call the compiler with `numba.compiler.compile_extra()` function.

###### Stage 1: 分析bytecode

Control flow generation, dataflow analysis.

Input: Python bytecode

Output: The controlflow CFG (how the pc moves inside code block as a result of jumps) & dataflow analysis result

###### Stage2: Generate Numba IR

Input: stack machine representation used by Python interpreter

Output: reg machine representation use by LLVM

###### Stage3: Rewrite some IR

ex. `raise statement` with a implicit param will be rewrite to fit nopython mode.

Input: Numba IR

Output: Numba IR

###### Stage4: Infer types

Give type to each IR variables. Types comes from 1) the type said in @jit(xxx); 2) runtime actual type.

Input: Numba IR

Output: types Numba IR



