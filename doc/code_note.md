state["func_ir"]的IR在first pass也就是TranslateByteCode已经被生成，然后在IR Processing被process：1）canonicalize_cfg (仔细看一下)；2）计算var的live time；3）为local var在用完之后插入del ；4）如果是生成器计算生成器信息

WithLifting: deal with `with` statement, if exist

inline: 把callee的代码直接复制到caller的代码中，而不用管context等等

InlineInlinables：如果jit装饰器kwarg inline为True就把函数直接inline到caller中

RewriteSemanticConstants：replace statement known to be constant to be the const value. ex. len(tuple) -> 20，为后面deadBranchPrune准备，增加可以kill的branch number。

DeadBranchPrune: 接在上一个后面，dead branch在此被认为是可推导的，在编译时不会执行，因为完全基于const（人话？）；directly mutate the IR

GenericRewrites：Run all before inference rewrites: match找到pattern，然后apply在IR上rewrite。

'before-inference': 

- RewriteConstGetitems: getitem(value=arr, index=\$constXX) -> static_getitem(value=arr, index=\<constant value\>) （\$constXX是const值）
- RewriteConstSetitems: setitem(value=arr, index=\$constXX) -> static_setitem(value=arr, index=\<constant value\>) （\$constXX是const值）
- RewriteConstRaises: raise(value) -> static_raise(exception_type, constant args), 当value是一个exception的实例化。这是为了在nopython mode中lowering，因为nopython无法获取runtime实例化的exception实例。
- DetectStaticBinops：当expr的rhs为const时，把rhs直接替换为const
- RewritePrintCalls：把到global print的call替换为专用的IR print nodes. var = call <print function>(...) -> 一系列的`print(...)`和 `var = const(None)` （？）
- DetectConstPrintArguments：找到print const的func，改成存储const参数到print node上。

MakeFunctionToJitFunction: 找出一个make_function opcode，并且替换为一个包含closure body的已编译函数，并且放到ir.Global里面（把function替换为jit的function？）；如果这里mutate了就重新IRprocess一下，重写var del bytecode。

InlineInlinables：如果jit装饰器kwarg inline为True就把函数直接inline到caller中

DeadBranchPrune: 接在上一个后面，dead branch在此被认为是可推导的，在编译时不会执行，因为完全基于const（人话？）；directly mutate the IR

？？？为啥上面这俩要再来一次？？？因为改写了jit code吗？如果是这样为什么这一次不用RewriteSemanticConstants呢？

FindLiterallyCalls：找到调用numba.literally()的代码，如果不是应用在literal type上就raise error（验证这个调用的正确性）；numba.literally()强制numba用对待一个literal的方式对待一个obj。

LiteralUnroll：？找赋值时是否有值为literal_unroll的赋值；没有直接return False了

ReconstructSSA：SSA-静态单赋值形式（每个var仅被赋值一次的IR），生成SSA，并且是minimal SSA（Choi et, al.）

LiteralPropagationSubPipelinePass：直接return了；否则会做partial type inference, literal value propagation, smantic rewrite和dead branch prune.

NoPythonTypeInference：？？？

PreLowerStripPhis：去除SSA引入的PHI nodes（ir.Expr.phi）转化为没有phi的正常表示，需要在lowering之前去掉Phi因为numba和LLVM的Phi nodes长得不一样，numba IR中的phi nodes可能会被转化成多个LLVM指令（那为什么还要先搞出来phi nodes再删掉？为什么不一步到位？）

**Phi Nodes**: LLVM IR中的一个表达式，用于将IR转化为SSA形式，可以方便地用于条件跳转。如果pc从%then调过来我们就返回calltmp的值，如果从%else跳过来就返回calltmp1的值：必须这样做因为是SSA形式。

https://stackoverflow.com/questions/11485531/what-exactly-phi-instruction-does-and-how-to-use-it-in-llvm

![image-20221124100439481](C:\Users\adali\AppData\Roaming\Typora\typora-user-images\image-20221124100439481.png)



InlineOverloads：如果装饰器inline = True的话，就把一个numba.extending.overload装饰器包裹的function直接插入到caller中。（此处可以在pass代码中设_DEBUG=True来看看到底干了啥）



NopythonRewrites：

执行所有after-inference的IR rewrites。

'after-inference': 

- RewriteStringLiteralGetitems: getitem(value=arr, index=\$XX) -> static_getitem(value=arr, index=\<literal value\>) (\$XX是一个string literal)
- RewriteStringLiteralSetitems: setitem(value=arr, index=\$XX) -> static_setitem(value=arr, index=\<literal value\>) (\$XX是一个string literal)
- RewriteArrayExprs：找到IR中的array exprs也就是**在array上的elementwise操作**（这里需要typing信息），替换为一个单个的operation，该operation后面会被拓展为类似一个ufunc call的东西。（再仔细看一下，可以展开讲）
- RewriteArrayOfConsts：找到从constant list创建的1D array，然后重写为array elements的初始化（而不必创建那个list）（？）



NoPythonSupportedFeatureValidation：验证IR是一种supported的格式

IRLegalization：把IR legalize（具体来说，保证没有任何phi nodes和del，然后再把del加回去）

AnnotateTypes：在IR中增加type annotation，格式是var = value :: type



NativeLowering：lowering是将高层指令转化为底层指令的过程。native lowering就是转化为机器码的过程？这个pss把function分解为block再分解为instruction。（？lowering.py）



NoPythonBackend：用numba IR生成LLVM IR，编译为machine code



DumpParforDiagnostics：打印parfor要用的诊断信息



TODO: 找出并执行对应的test，看看每个pass到底在干啥