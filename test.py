import numpy as np
import hashlib
import pickle
from diskcache import Cache
import time
cache = Cache("./sim_cache")


import numpy as np
import hashlib
from diskcache import Cache

cache = Cache("./sim_cache")


# =========================================================
# GLOBAL registry (VERY FAST)
# =========================================================
_fingerprint_registry = {}
_version_registry = {}


# =========================================================
# FAST but FULL-CORRECT fingerprint (only when needed)
# =========================================================
def fingerprint(arr):
    arr = np.asarray(arr)

    h = hashlib.md5()
    h.update(str(arr.shape).encode())
    h.update(str(arr.dtype).encode())
    h.update(memoryview(arr))   # FULL correctness

    return h.digest()


# =========================================================
# Detect change cheaply
# =========================================================
def get_version(obj):
    """
    Returns a version number that only changes when data changes.
    """
    arr = np.asarray(obj)

    obj_id = id(arr)

    new_fp = fingerprint(arr)

    old_fp = _fingerprint_registry.get(obj_id)

    if old_fp != new_fp:
        _fingerprint_registry[obj_id] = new_fp
        _version_registry[obj_id] = _version_registry.get(obj_id, 0) + 1

    return _version_registry.get(obj_id, 0)


# =========================================================
# FAST CACHE KEY
# =========================================================
def make_cache_key(func_name, *args, **kwargs):
    h = hashlib.md5()
    h.update(func_name.encode())

    for a in args:
        arr = np.asarray(a)
        h.update(str(id(arr)).encode())   # fast identity
        h.update(str(get_version(arr)).encode())  # correctness

    for k in sorted(kwargs):
        arr = np.asarray(kwargs[k])
        h.update(str(k).encode())
        h.update(str(id(arr)).encode())
        h.update(str(get_version(arr)).encode())

    return h.hexdigest()


# =========================================================
# DECORATOR
# =========================================================
def cached(func):
    def wrapper(*args, **kwargs):
        key = make_cache_key(func.__name__, *args, **kwargs)

        if key in cache:
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


# =========================================================
# Cached function
# =========================================================
@cached
def rms_avg(Op, nested_list, time_values):
    X = np.array(nested_list)   # (N, T)
    t = np.array(time_values)   # (T,)

    delta_T = t[-1] - t[0]

    if Op == "RMS":
        integrals = np.trapezoid(X**2, x=t, axis=1)
        result = np.sqrt(integrals / delta_T)

    elif Op == "AVG":
        integrals = np.trapezoid(X, x=t, axis=1)
        result = integrals / delta_T

    else:
        raise ValueError("Op must be 'RMS' or 'AVG'")

    return result


# =========================================================
# Non-cached version (reference)
# =========================================================
def rms_avg_normal(Op, nested_list, time_values):
    X = np.array(nested_list)
    t = np.array(time_values)

    delta_T = t[-1] - t[0]

    if Op == "RMS":
        integrals = np.trapezoid(X**2, x=t, axis=1)
        result = np.sqrt(integrals / delta_T)

    elif Op == "AVG":
        integrals = np.trapezoid(X, x=t, axis=1)
        result = integrals / delta_T

    else:
        raise ValueError("Op must be 'RMS' or 'AVG'")

    return result


# =========================================================
# TEST / BENCHMARK
# =========================================================
if __name__ == "__main__":
    np.random.seed(42)

    N = 5000
    T = 20000

    t = np.linspace(0, 10, T)

    # create deterministic "real-world-like signals"
    nested_list = [
        (np.sin(t * (i % 5 + 1)) + 0.1 * np.cos(t * 3)).astype(np.float64).tolist()
        for i in range(N)
    ]

    time_values = t.tolist()

    print("\n" + "="*70)
    print("TIME COMPARISON: Normal Function vs Cached Function")
    print("="*70)

    # -----------------------------------------------------
    print("\n📊 TEST 1: FIRST CALL (No cache yet)")
    print("-" * 70)

    start = time.time()
    result_normal1 = rms_avg_normal("RMS", nested_list, time_values)
    normal_time1 = time.time() - start
    print(f"Normal function:  {normal_time1:.4f} seconds")

    start = time.time()
    result_cached1 = rms_avg("RMS", nested_list, time_values)
    cached_time1 = time.time() - start
    print(f"Cached function:  {cached_time1:.4f} seconds")

    # -----------------------------------------------------
    print("\n📊 TEST 2: SECOND CALL (Cached hit)")
    print("-" * 70)

    start = time.time()
    result_normal2 = rms_avg_normal("RMS", nested_list, time_values)
    normal_time2 = time.time() - start
    print(f"Normal function:  {normal_time2:.4f} seconds")

    start = time.time()
    result_cached2 = rms_avg("RMS", nested_list, time_values)
    cached_time2 = time.time() - start
    print(f"Cached function:  {cached_time2:.6f} seconds")

    # -----------------------------------------------------
    print("\n📊 TEST 3: 10 CALLS")
    print("-" * 70)

    start = time.time()
    for _ in range(10):
        rms_avg_normal("RMS", nested_list, time_values)
    normal_total = time.time() - start

    start = time.time()
    for _ in range(10):
        rms_avg("RMS", nested_list, time_values)
    cached_total = time.time() - start

    print(f"Normal total:  {normal_total:.4f}s")
    print(f"Cached total:  {cached_total:.6f}s")

    # -----------------------------------------------------
    print("\n✓ Verification:")
    print("Match 1:", np.allclose(result_normal1, result_cached1))
    print("Match 2:", np.allclose(result_normal2, result_cached2))

    print("\n⚡ Speedup:", normal_total / cached_total if cached_total > 0 else "∞")