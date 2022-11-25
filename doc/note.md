##### What Numba does

Look at the Python bytecode, analysis it and change it into LLVM IR, then call LLVM to interpret IR into machine code and utilize it's optimization.

Basically, Numba add type to each of the variables to get the acceleration.



##### What Numba has

- object mode: code still manipulate Python object, but with type information (not much faster than Python)
- nopython mode: code compiled for specific data type, not rely on Python Object (much faster than Python)

##### Compiler Architecture

- Numba IR: a intermediate representation for Numba
- LLVM: Numba use LLVM to compile IR into machine code

##### Compiler Stages

Numba @jit decorator call the compiler with `numba.compiler.compile_extra()` function.

###### Stage 1: Analyze bytecode

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

Output: typed Numba IR

Unsupported type will be marked as default type `pyobject` and will fall-back to object mode.

###### Stage 5a: Rewrite typed IR

Apply any high-level optimization that may benefit from the Numba IR type info.

As later optimization could be hard (ex. array op). Ex. loop fusion and shortcut deforestation

Input: typed Numba IR

Output: Optimized types Numba IR

###### Stage 5b: Automatic Parallelization

Extract the implicit parallelization in the ops and replace with explicit `parfor` operation; then combine consecutive `parfor` to single `parfor`.

auto parallelization have many sub passes:

1) CFG simplification: chains of blocks without loop -> single blocks (???)
2) Numpy canonicalization: different numpy calls to the same function -> the same way (ex. arr.sum() -> numpy.sum(arr))
3) array analysis: make sure the size and type for `parfor` operations are matched, prepare for later parfor fusion.
4) `prange()` -> `parfor`: explicitly marked parallelizable loop with `prange`-> `parfor`.
5) numpy -> `parfor`: Some functions in Numpy (ex. zeros, ones, dot) and random number generators -> `parfor`.
6) Setitem to `parfor`: range value assignment ->`parfor`. 
7) Simplification: copy propagation and dead code elimation pass.
8) Fusion：reorder instructions in a block, so that `parfor`s are closer and can be fused better; loop until no `parfor` can be fused.
9) push call objs and compute parfor params: parameters for `parfor`.

###### Stage 6a: Generate LLVM IR

Lowering process: generate native code. Call `llvmlite to get LLVM IR and optimize with LLVM toolchain.

Input: Numba IR

Output: LLVM IR

###### Stage 6b: Generate object mode LLVM IR

If typing failed and func is compiled in object mode: wll get longer LLVL IR, as almost all operations need to call Python C API.

Loop-lifting (???)

###### Stage 7: LLVM IR -> machine code

call LLVM JIT. 

Input: LLVM IR

Output: machine code and dynamic dispatcher.

##### Polymorphic dispatching (runtime)

- Dispatcher: a function that dispatches to the right implementation based on the types of the arguments.

- multiple dispatch

- two steps:
  
  1. infer **numba type**
     1. cannot simply lookup an object’s class and key a dictionary with it to obtain the corresponding Numba type.
     2. based on its Python type, query various properties to infer the appropriate Numba type
     - **typecode**: a unique integer for each Numba type
       - Hard-coded fast paths: for some important types, the typecode is hard-coded in the dispatcher.
       - Fingerprint-based typecode cache: For non-so-trivial types
         -  a simple bytestring, a low-level possible denotation of that Numba type: a fingerprint
         -  a cache mapping fingerprints to typecodes.
  2. select  specialization (or compile a new one)
      - select the specialization with the closest matching signature
      - loop over all the specializations and find the one with the closest matching signature
      - compability:
        - if convert is allowed
        - semantic cost of conversion
      - best match:
        - `(number of unsafe conversions, number of safe conversions, number of same-kind promotions, number of exact matches) `

##### Extension
1. typing
   1. type inference is assigning numba types to variables to enable code generation
2. lowering
   1. convert high-level Python operations into low-level LLVM operations (using the type information from the typing stage)