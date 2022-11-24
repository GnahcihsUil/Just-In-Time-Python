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

'after-inference': 

- RewriteStringLiteralGetitems: getitem(value=arr, index=\$XX) -> static_getitem(value=arr, index=\<literal value\>) (\$XX是一个string literal)
- RewriteStringLiteralSetitems: setitem(value=arr, index=\$XX) -> static_setitem(value=arr, index=\<literal value\>) (\$XX是一个string literal)

<class 'numba.np.ufunc.array_exprs.RewriteArrayExprs'>,

<class 'numba.core.inline_closurecall.RewriteArrayOfConsts'>]



TODO: 找出并执行对应的test，看看每个pass到底在干啥