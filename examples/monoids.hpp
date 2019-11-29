#pragma once
#include <algorithm>
#include <cstdint>

struct plus_monoid {
    typedef int64_t value_type;
    value_type unit() const { return 0; }
    value_type mult(value_type a, value_type b) const { return a + b; }
};

struct max_monoid {
    typedef int64_t value_type;
    value_type unit() const { return INT64_MIN; }
    value_type mult(value_type a, value_type b) const { return std::max(a, b); }
};

struct min_monoid {
    typedef int64_t value_type;
    value_type unit() const { return INT64_MAX; }
    value_type mult(value_type a, value_type b) const { return std::min(a, b); }
};
