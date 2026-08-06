from __future__ import annotations

import json

from .server import finance_kit_doctor


def main() -> None:
    print(json.dumps(finance_kit_doctor.fn(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
