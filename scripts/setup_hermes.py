from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


ADA_SKILLS = (
    "dandacompany/vibe-finance-kit/finance-research-discipline",
    "dandacompany/vibe-finance-kit/etf-value-analysis",
    "dandacompany/vibe-finance-kit/backtest-audit",
)
OLIVER_SKILLS = ADA_SKILLS[:2]


def configure_output() -> None:
    if os.name == "nt":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")


def find_hermes() -> str | None:
    executable = "hermes.exe" if os.name == "nt" else "hermes"
    candidates = [shutil.which("hermes"), str(Path.home() / ".local" / "bin" / executable)]
    if os.name == "nt" and os.environ.get("LOCALAPPDATA"):
        candidates.append(
            str(
                Path(os.environ["LOCALAPPDATA"])
                / "hermes"
                / "hermes-agent"
                / "venv"
                / "Scripts"
                / executable
            )
        )
    return next((path for path in candidates if path and Path(path).is_file()), None)


def run(command: list[str]) -> None:
    print(f"+ {subprocess.list2cmdline(command)}", flush=True)
    subprocess.run(command, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Vibe Finance Kit을 Hermes의 Ada와 Oliver 프로필에 설정합니다."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="패키지와 실행 경로만 검사하고 Hermes 설정은 변경하지 않습니다.",
    )
    parser.add_argument("--ada-profile", default="ada", help=argparse.SUPPRESS)
    parser.add_argument("--oliver-profile", default="oliver", help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> int:
    configure_output()
    args = parse_args()
    hermes = find_hermes()
    if hermes is None:
        print("필수 명령을 찾을 수 없습니다: hermes", file=sys.stderr)
        return 1

    virtual_env = os.environ.get("VIRTUAL_ENV")
    if virtual_env is None:
        print("uv 프로젝트 환경을 찾을 수 없습니다. uv run으로 실행해 주세요.", file=sys.stderr)
        return 1

    environment_root = Path(virtual_env).resolve()
    scripts_dir = environment_root / ("Scripts" if os.name == "nt" else "bin")
    executable_name = "vibe-finance-kit.exe" if os.name == "nt" else "vibe-finance-kit"
    mcp_command = scripts_dir / executable_name
    if not mcp_command.is_file():
        print(f"MCP 실행 파일을 찾을 수 없습니다: {mcp_command}", file=sys.stderr)
        return 1

    print(f"운영체제: {platform.system()} {platform.release()}")
    print(f"Python: {Path(sys.executable).resolve()}")
    print(f"Hermes: {hermes}")
    print(f"MCP: {mcp_command}")

    print("\n[1/4] 읽기 전용 doctor")
    run([sys.executable, "-m", "vibe_finance_kit.doctor"])

    if args.check:
        print("\n검사 완료: Hermes 프로필과 MCP 설정은 변경하지 않았습니다.")
        return 0

    print("\n[2/4] Ada 분석 Skill 설치")
    for skill in ADA_SKILLS:
        run([hermes, "-p", args.ada_profile, "skills", "install", skill, "--yes"])

    print("\n[3/4] Oliver 리서치 Skill 설치")
    for skill in OLIVER_SKILLS:
        run([hermes, "-p", args.oliver_profile, "skills", "install", skill, "--yes"])

    print("\n[4/4] Ada MCP 등록과 연결 검사")
    print("도구 4개 활성화 질문이 나오면 Y를 입력하세요.")
    run(
        [
            hermes,
            "-p",
            args.ada_profile,
            "mcp",
            "add",
            "vibe-finance-kit",
            "--command",
            str(mcp_command),
        ]
    )
    run([hermes, "-p", args.ada_profile, "mcp", "test", "vibe-finance-kit"])

    print("\n설정이 끝났습니다. Ada와 Oliver를 새 세션으로 시작하세요.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
