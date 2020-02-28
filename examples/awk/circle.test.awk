# verify-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_4_B
# verify-helper: ERROR 1e-5
@include "examples/awk/circle.awk"
{
    print get_area($1), get_circumference($1);
}
