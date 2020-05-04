import macros

proc scanf(formatstr: cstring){.header: "<stdio.h>", varargs.}
proc nextInt(): int = scanf("%lld",addr result)
