#ifdef __clang__
#define IGNORE
#else

#define PROBLEM "https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A"
#include <cstdio>

// clang++ says "error: C++ requires a type specifier for all declarations", but g++ doesn't
main() {
    printf("Hello World\n");
}

#endif
