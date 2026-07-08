"""Upload scan archives and related research files to XNAT."""

from __future__ import annotations

import argparse
import getpass
import os
import zipfile
from pathlib import Path
from typing import Any, Sequence


def require_file(path: str, *, zip_only: bool = False) -> Path:
    """Return an existing file path and optionally require a valid ZIP."""
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        raise ValueError(f"File does not exist: {file_path}")
    if zip_only and not zipfile.is_zipfile(file_path):
        raise ValueError(f"Scan import must be a valid ZIP file: {file_path}")
    return file_path


def connection_settings(args: argparse.Namespace) -> tuple[str, str, str]:
    """Read connection settings without storing credentials in source code."""
    server = args.server or os.environ.get("XNAT_SERVER")
    user = args.user or os.environ.get("XNAT_USER")
    password = os.environ.get("XNAT_PASSWORD")

    if not server:
        raise ValueError("Set XNAT_SERVER or provide --server.")
    if not user:
        raise ValueError("Set XNAT_USER or provide --user.")
    if not password:
        password = getpass.getpass("XNAT password: ")

    return server, user, password


def connect(args: argparse.Namespace) -> Any:
    """Open an XNAT session using xnatpy."""
    try:
        import xnat
    except ImportError as error:
        raise RuntimeError(
            "The xnat package is not installed. Run: pip install -r requirements.txt"
        ) from error

    server, user, password = connection_settings(args)
    options: dict[str, Any] = {
        "user": user,
        "password": password,
        "verify": not args.insecure,
    }
    return xnat.connect(server, **options)


def ensure_resource(session: Any, parent: Any, resource_name: str) -> Any:
    """Return an existing resource or create it."""
    if resource_name not in parent.resources:
        return session.classes.ResourceCatalog(parent=parent, label=resource_name)
    return parent.resources[resource_name]


def upload_scan(session: Any, args: argparse.Namespace, file_path: Path) -> None:
    """Import a scan archive to the prearchive."""
    existing = session.prearchive.find(
        args.project, args.subject, args.experiment
    )
    if existing and not args.allow_existing:
        print(f"Skipped {args.experiment}: a matching prearchive session exists.")
        return

    session.services.import_(
        str(file_path),
        project=args.project,
        subject=args.subject,
        experiment=args.experiment,
    )
    print(f"Imported {file_path.name} as experiment {args.experiment}.")


def upload_experiment_resource(
    session: Any, args: argparse.Namespace, file_path: Path
) -> None:
    """Upload one file to a resource attached to an experiment."""
    experiment = (
        session.projects[args.project]
        .subjects[args.subject]
        .experiments[args.experiment]
    )
    resource = ensure_resource(session, experiment, args.resource)
    remote_name = args.remote_name or file_path.name
    resource.upload(path=str(file_path), remotepath=remote_name)
    print(f"Uploaded {file_path.name} to {args.experiment}/{args.resource}.")


def upload_project_resource(
    session: Any, args: argparse.Namespace, file_path: Path
) -> None:
    """Upload one file to a project-level resource."""
    project = session.projects[args.project]
    resource = ensure_resource(session, project, args.resource)
    remote_name = args.remote_name or file_path.name
    resource.upload(path=str(file_path), remotepath=remote_name)
    print(f"Uploaded {file_path.name} to {args.project}/{args.resource}.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Upload scan archives and related files to XNAT."
    )
    parser.add_argument("--server", help="XNAT URL (or set XNAT_SERVER)")
    parser.add_argument("--user", help="XNAT username (or set XNAT_USER)")
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="disable TLS certificate verification",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and print the upload without connecting",
    )

    commands = parser.add_subparsers(dest="command", required=True)

    scan = commands.add_parser("scan", help="import a ZIP scan archive")
    scan.add_argument("file")
    scan.add_argument("--project", required=True)
    scan.add_argument("--subject", required=True)
    scan.add_argument("--experiment", required=True)
    scan.add_argument("--allow-existing", action="store_true")

    resource = commands.add_parser(
        "resource", help="upload an experiment resource file"
    )
    resource.add_argument("file")
    resource.add_argument("--project", required=True)
    resource.add_argument("--subject", required=True)
    resource.add_argument("--experiment", required=True)
    resource.add_argument("--resource", required=True)
    resource.add_argument("--remote-name")

    project_resource = commands.add_parser(
        "project-resource", help="upload a project resource file"
    )
    project_resource.add_argument("file")
    project_resource.add_argument("--project", required=True)
    project_resource.add_argument("--resource", required=True)
    project_resource.add_argument("--remote-name")

    return parser


def describe_upload(args: argparse.Namespace, file_path: Path) -> None:
    details = [f"file={file_path}", f"project={args.project}"]
    for name in ("subject", "experiment", "resource", "remote_name"):
        value = getattr(args, name, None)
        if value:
            details.append(f"{name}={value}")
    print(f"Dry run ({args.command}): " + ", ".join(details))


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        file_path = require_file(args.file, zip_only=args.command == "scan")
        if args.dry_run:
            describe_upload(args, file_path)
            return 0

        session = connect(args)
        try:
            if args.command == "scan":
                upload_scan(session, args, file_path)
            elif args.command == "resource":
                upload_experiment_resource(session, args, file_path)
            else:
                upload_project_resource(session, args, file_path)
        finally:
            session.disconnect()
    except (RuntimeError, ValueError) as error:
        parser.error(str(error))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
