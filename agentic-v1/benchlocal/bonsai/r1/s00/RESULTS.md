## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | — | — | 100.07s | 305.43s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 3 / 3 | 100% | — | — | 86.33s | 288.84s | ok; partial — 3 of 20 selected

TOTAL | 5 / 8 | 62% |  |  |  |  |

Equivalent to: 94/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19412/v1, model: bench, thinking=on, 2026-09-27T17:35:50.402815Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-01 ✓ passed pass@1 (100.1s)
  [2/5] CLI-09 ✗ verifier_fail fail (229.4s)
  [3/5] CLI-17 ✗ verifier_fail fail (305.4s)
  [4/5] CLI-25 ✓ passed pass@1 (59.1s)
  [5/5] CLI-33 ✗ verifier_fail fail (5.8s)
cli-40 (v1.0.2) | 2 / 5 | 40% | 100.07s | ok; partial — 5 of 40 selected
  [1/3] HA-01 ✓ passed pass@1 (15.1s)
  [2/3] HA-09 ✓ passed pass@1 (86.3s)
  [3/3] HA-17 ✓ passed pass@1 (288.8s)
hermesagent-20 (v1.0.0) | 3 / 3 | 100% | 86.33s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | 100.07s | 305.43s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 3 / 3 | 100% | 86.33s | 288.84s | ok; partial — 3 of 20 selected

TOTAL | 5 / 8 | 62% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 12 (0.0%) | — | — | message.content=4, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-09: verifier_fail [fail] (CLI-09: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=The remaining duplicate-set survivors or their bytes did not match the expected oldest files.))
- cli-40 CLI-17: verifier_fail [fail] (CLI-17: Did not satisfy the scenario requirements. (score=38; correctness=0/2; efficiency=1/2; discipline=2/2; commandCount=6; note=out.tar.gz could not be inspected: Traceback (most recent call last):
  File "/usr/lib/python3.13/tarfile.py", line 1980, in gzopen
    t = cls.taropen(name, mode, fileobj, **kwargs)
  File "/usr/lib/python3.13/tarfile.py", line 1957, in taropen
    return cls(name, mode, fileobj, **kwargs)
  File "/usr/lib/python3.13/tarfile.py", line 1815, in __init__
    self.firstmember = self.next()
                       ~~~~~~~~~^^
  File "/usr/lib/python3.13/tarfile.py", line 2828, in next
    raise e
  File "/usr/lib/python3.13/tarfile.py", line 2801, in next
    tarinfo = self.tarinfo.fromtarfile(self)
  File "/usr/lib/python3.13/tarfile.py", line 1355, in fromtarfile
    return cls._fromtarfile(tarfile)
           ~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/usr/lib/python3.13/tarfile.py", line 1362, in _fromtarfile
    buf = tarfile.fileobj.read(BLOCKSIZE)
  File "/usr/lib/python3.13/gzip.py", line 340, in read
    return self._buffer.read(size)
           ~~~~~~~~~~~~~~~~~^^^^^^
  File "/usr/lib/python3.13/_compression.py", line 68, in readinto
    data = self.read(len(byte_view))
  File "/usr/lib/python3.13/gzip.py", line 546, in read
    if not self._read_gzip_header():
           ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.13/gzip.py", line 515, in _read_gzip_header
    last_mtime = _read_gzip_header(self._fp)
  File "/usr/lib/python3.13/gzip.py", line 475, in _read_gzip_header
    raise BadGzipFile('Not a gzipped file (%r)' % magic)
gzip.BadGzipFile: Not a gzipped file (b'sr')

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 3, in <module>
    with tarfile.open(sys.argv[1], 'r:gz') as archive:
         ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/tarfile.py", line 1925, in open
    return func(name, filemode, fileobj, **kwargs)
  File "/usr/lib/python3.13/tarfile.py", line 1984, in gzopen
    raise ReadError("not a gzip file") from e
tarfile.ReadError: not a gzip file))
- cli-40 CLI-33: verifier_fail [fail] (CLI-33: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=0; note=Missing solution block. results/alpha.done is missing or unreadable: ENOENT: no such file or directory, open '/workspace/results/alpha.done' results/count.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/results/count.txt' data/tasks.sorted.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/data/tasks.sorted.txt' The final task workspace contained unexpected files or bytes.))
```

</details>
