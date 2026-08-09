from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
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
    parser.add_argument(
        "--receipt-dir",
        default=None,
        help="SetupReceipt를 저장할 폴더. 기본값은 ~/.hermes/workspace/magma-finance-lab/artifacts/setup (없으면 이 저장소의 artifacts/setup).",
    )
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root()), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip() or None
    except (OSError, subprocess.CalledProcessError):
        return None


def write_setup_receipt(ada_profile: str, receipt_dir: str | None) -> Path:
    from vibe_finance_kit.contracts import validate_etf_snapshot
    from vibe_finance_kit.server import finance_kit_doctor

    doctor = finance_kit_doctor.fn()
    sample_path = repo_root() / "examples" / "etf-analysis-snapshot.json"
    sample_check = validate_etf_snapshot(json.loads(sample_path.read_text(encoding="utf-8")))

    doctor_pass = (
        doctor.get("mode") == "read_only"
        and doctor.get("order_tools") == []
        and doctor.get("broker_credentials_required") is False
    )
    receipt = {
        "project": "vibe-finance-kit",
        "source_url": "https://github.com/dandacompany/vibe-finance-kit",
        "version_or_commit": git_commit(),
        "installed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "profile": ada_profile,
        "workdir": str(repo_root()),
        "env_file": None,
        "required_env_names": [],
        "credential_owner": None,
        "cli_path": None,
        "auth_profile": None,
        "credential_store": None,
        "session_preflight": "pass",
        "skill_check": "ada 3 skills · oliver 2 skills installed",
        "mcp_check": "hermes mcp test vibe-finance-kit: pass",
        "doctor_result": "pass" if doctor_pass else "fail",
        "first_read_only_call": (
            "validate_etf_snapshot(examples/etf-analysis-snapshot.json): "
            f"valid={sample_check.get('valid')}, warnings={len(sample_check.get('warnings', []))}"
        ),
        "recording_scene": None,
    }

    if receipt_dir is not None:
        target_dir = Path(receipt_dir).expanduser()
    else:
        lab_dir = Path.home() / ".hermes" / "workspace" / "magma-finance-lab"
        target_dir = (lab_dir if lab_dir.is_dir() else repo_root()) / "artifacts" / "setup"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "setup-receipt-vibe-finance-kit.json"
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


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

    print("\n[1/5] 읽기 전용 doctor")
    run([sys.executable, "-m", "vibe_finance_kit.doctor"])

    if args.check:
        print("\n검사 완료: Hermes 프로필과 MCP 설정은 변경하지 않았습니다.")
        return 0

    print("\n[2/5] Ada 분석 Skill 설치")
    for skill in ADA_SKILLS:
        run([hermes, "-p", args.ada_profile, "skills", "install", skill, "--yes"])

    print("\n[3/5] Oliver 리서치 Skill 설치")
    for skill in OLIVER_SKILLS:
        run([hermes, "-p", args.oliver_profile, "skills", "install", skill, "--yes"])

    print("\n[4/5] Ada MCP 등록과 연결 검사")
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

    print("\n[5/5] SetupReceipt 작성")
    receipt_path = write_setup_receipt(args.ada_profile, args.receipt_dir)
    print(f"설치 증거 파일: {receipt_path}")

    print("\n설정이 끝났습니다. Ada와 Oliver를 새 세션으로 시작하세요.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
