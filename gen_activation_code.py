#!/usr/bin/env python3
import uuid

if __name__ == '__main__':
    code = str(uuid.uuid4())
    assert(30 < len(code) and len(code) <= 53)
    print(code)
