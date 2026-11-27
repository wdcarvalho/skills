#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import sqlite3
import string
import sys
import unicodedata
import uuid
from datetime import datetime, timedelta, timezone

DEFAULT_DB = os.path.join("~", ".orquestrar-agentes", "runs.sqlite")
ENV_FLAG = "ORQUESTRAR_HARNESS_FEEDBACK"

ALVOS = ("skill", "template", "ferramenta", "sandbox", "config", "contrato-saida", "outro")
SEVERIDADES = ("travou", "contornou-caro", "contornou-barato")
SEVERITY_WEIGHT = {"travou": 3, "contornou-caro": 2, "contornou-barato": 1}

OPEN_MARK = "HARNESS_FEEDBACK"
CLOSE_MARK = "FIM_HARNESS_FEEDBACK"
MAX_BLOCKS = 3
LIMIT_TEXT = 300
LIMIT_REF = 120
FINGERPRINT_SIZE = 12
KEYS = frozenset(("alvo", "ref", "obstaculo", "contorno", "severidade"))
STRIP_CHARS = "*_`~" + string.whitespace

RUN_FIELDS = (
    "parent_run", "papel", "modelo", "task", "repo", "branch", "base", "commit_sha",
    "pr_url", "status", "summary", "assumptions", "workarounds", "verification",
    "pending", "raw_report",
)
MASKED_RUN_FIELDS = ("task", "summary", "assumptions", "workarounds", "verification", "pending", "raw_report")

MARKERS = {
    "email": "[e-mail omitido]",
    "cnpj": "[CNPJ omitido]",
    "cpf": "[CPF omitido]",
    "cartao": "[cartão omitido]",
    "telefone": "[telefone omitido]",
    "bancario": "[dado bancário omitido]",
    "segredo": "[segredo omitido]",
}

# Quantificadores sempre limitados: com `+` solto uma linha longa sem "@" faria o regex custar O(n^2).
PERSONAL_DATA = (
    (re.compile(r"[\w.+-]{1,64}@[\w-]{1,63}(?:\.[\w-]{1,63}){1,8}"), MARKERS["email"]),
    (re.compile(r"\b\d{2}[.-]?\d{3}[.-]?\d{3}[/.-]?\d{4}[.-]?\d{2}\b"), MARKERS["cnpj"]),
    (re.compile(r"\b\d{3}[.-]?\d{3}[.-]?\d{3}[.-]?\d{2}\b"), MARKERS["cpf"]),
    (re.compile(r"\b(?:(?:\d{4}[ -]){4}\d{1,3}|(?:\d{4}[ -]){3}\d{1,4})\b"), MARKERS["cartao"]),
    (re.compile(r"(?:\+55\s?)?\(\d{2}\)\s?9?\d{4}-?\d{4}\b"), MARKERS["telefone"]),
    (re.compile(r"(?:\+55[ -]?)?\b[1-9]{2}[ -]?9?\d{4}[ -]?\d{4}\b"), MARKERS["telefone"]),
    (re.compile(r"\b9\d{4}-\d{4}\b"), MARKERS["telefone"]),
    (
        re.compile(
            r"\b(?:agência|agencia|ag\.|conta|c/c|cc)[ \t]{0,2}(?:(?::|nº)[ \t]{0,2})?\d{1,8}(?:-[\dXx])?\b",
            re.IGNORECASE,
        ),
        MARKERS["bancario"],
    ),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), MARKERS["segredo"]),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"), MARKERS["segredo"]),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), MARKERS["segredo"]),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"), MARKERS["segredo"]),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"), MARKERS["segredo"]),
    (re.compile(r"\blin_api_[A-Za-z0-9]{20,}"), MARKERS["segredo"]),
    (re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{16,}=*", re.IGNORECASE), "Bearer " + MARKERS["segredo"]),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"), MARKERS["segredo"]),
)

# UUID e SHA completo ficam de fora da máscara: corrompê-los quebra a correlação entre run, branch e PR.
IDENTIFIER = re.compile(
    r"(\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b|\b[0-9a-f]{40}\b)",
    re.IGNORECASE,
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    parent_run TEXT,
    papel TEXT,
    modelo TEXT,
    task TEXT,
    repo TEXT,
    branch TEXT,
    base TEXT,
    commit_sha TEXT,
    pr_url TEXT,
    status TEXT,
    summary TEXT,
    assumptions TEXT,
    workarounds TEXT,
    verification TEXT,
    pending TEXT,
    raw_report TEXT
);
CREATE TABLE IF NOT EXISTS harness_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL REFERENCES runs(id),
    created_at TEXT NOT NULL,
    papel TEXT,
    modelo TEXT,
    repo TEXT,
    alvo TEXT NOT NULL,
    ref TEXT,
    obstaculo TEXT NOT NULL,
    contorno TEXT,
    severidade TEXT NOT NULL,
    fingerprint TEXT NOT NULL,
    raw_block TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    fix_ref TEXT
);
CREATE INDEX IF NOT EXISTS idx_harness_feedback_fingerprint ON harness_feedback(fingerprint);
CREATE INDEX IF NOT EXISTS idx_harness_feedback_created_at ON harness_feedback(created_at);
CREATE INDEX IF NOT EXISTS idx_harness_feedback_status ON harness_feedback(status);
"""


def harness_feedback_enabled(environ=None):
    environ = os.environ if environ is None else environ
    return str(environ.get(ENV_FLAG, "1")).strip().lower() not in ("0", "false", "off", "no")


def mask(text):
    parts = IDENTIFIER.split(text)
    for index in range(0, len(parts), 2):
        for pattern, replacement in PERSONAL_DATA:
            parts[index] = pattern.sub(replacement, parts[index])
    return "".join(parts)


def cut_outside_marker(text):
    start = text.rfind("[")
    if start < 0:
        return text
    rest = text[start:]
    for marker in MARKERS.values():
        if len(rest) < len(marker) and marker.startswith(rest):
            return text[:start].strip()
    return text


def truncate(text, limit):
    if len(text) <= limit:
        return text
    return cut_outside_marker(text[:limit])


def normalize(text):
    decomposed = unicodedata.normalize("NFD", text)
    plain = "".join(ch for ch in decomposed if not unicodedata.category(ch).startswith("M")).lower()
    plain = re.sub(r"[0-9]+", "#", plain)
    plain = re.sub(r"[^a-z#]+", " ", plain)
    plain = re.sub(r"\s*#\s*", "#", plain)
    return plain.strip()


def fingerprint(alvo, ref, obstaculo):
    digest = hashlib.sha256(f"{alvo}|{normalize(ref)}|{normalize(obstaculo)}".encode("utf-8")).hexdigest()
    return digest[:FINGERPRINT_SIZE]


def _marker_of(line):
    return line.strip().strip(STRIP_CHARS).upper()


def _read_fields(lines):
    fields = {}
    for line in lines:
        cut = line.find(":")
        if cut < 0:
            continue
        key = line[:cut].strip().lower()
        if key not in KEYS or key in fields:
            continue
        fields[key] = line[cut + 1:].strip()
    return fields


def _render_block(alvo, ref, obstaculo, contorno, severidade):
    lines = [OPEN_MARK, f"alvo: {alvo}"]
    if ref:
        lines.append(f"ref: {ref}")
    lines.append(f"obstaculo: {obstaculo}")
    if contorno:
        lines.append(f"contorno: {contorno}")
    lines.extend((f"severidade: {severidade}", CLOSE_MARK))
    return "\n".join(lines)


def _build(lines):
    fields = _read_fields(lines)
    alvo = fields.get("alvo", "").strip().lower()
    severidade = fields.get("severidade", "").strip().lower()
    raw_obstaculo = fields.get("obstaculo", "")
    if alvo not in ALVOS or severidade not in SEVERIDADES or raw_obstaculo == "":
        return None
    ref = truncate(mask(fields.get("ref", "")), LIMIT_REF)
    obstaculo = truncate(mask(raw_obstaculo), LIMIT_TEXT)
    contorno = truncate(mask(fields.get("contorno", "")), LIMIT_TEXT)
    return {
        "alvo": alvo,
        "ref": ref,
        "obstaculo": obstaculo,
        "contorno": contorno,
        "severidade": severidade,
        "fingerprint": fingerprint(alvo, ref, obstaculo),
        "raw_block": _render_block(alvo, ref, obstaculo, contorno, severidade),
    }


def _parse(text):
    if not isinstance(text, str):
        return []
    items = []
    lines = None
    for line in text.splitlines():
        marker = _marker_of(line)
        if marker == OPEN_MARK:
            lines = []
            continue
        if marker == CLOSE_MARK:
            if lines is None:
                continue
            item = _build(lines)
            lines = None
            if item is None:
                continue
            items.append(item)
            if len(items) >= MAX_BLOCKS:
                break
            continue
        if lines is not None:
            lines.append(line)
    return items


def parse_feedback(text):
    # O parser roda sobre saída de agente: qualquer entrada estranha vira lista vazia, nunca exceção.
    try:
        return _parse(text)
    except Exception:
        return []


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def connect(path=None):
    path = os.path.expanduser(path or DEFAULT_DB)
    directory = os.path.dirname(path) or "."
    if not os.path.isdir(directory):
        os.makedirs(directory, mode=0o700, exist_ok=True)
        os.chmod(directory, 0o700)
    if not os.path.exists(path):
        os.close(os.open(path, os.O_CREAT | os.O_WRONLY, 0o600))
        os.chmod(path, 0o600)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def _as_text(value):
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return "\n".join(str(item) for item in value)
    return json.dumps(value, ensure_ascii=False)


def add_run(conn, data, now=None):
    if not isinstance(data, dict):
        raise ValueError("add-run espera um objeto JSON")
    run_id = _as_text(data.get("id")) or uuid.uuid4().hex[:12]
    values = {}
    for field in RUN_FIELDS:
        text = _as_text(data.get(field))
        if text is not None and field in MASKED_RUN_FIELDS:
            text = mask(text)
        values[field] = text
    columns = ["id", "created_at", *RUN_FIELDS]
    params = [run_id, now or _now(), *(values[field] for field in RUN_FIELDS)]
    with conn:
        conn.execute(
            f"INSERT INTO runs ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})",
            params,
        )
    return run_id


def add_feedback(conn, run_id, text, now=None, enabled=True):
    if not enabled:
        return 0
    run = conn.execute("SELECT papel, modelo, repo FROM runs WHERE id = ?", (run_id,)).fetchone()
    if run is None:
        raise ValueError(f"run não encontrado: {run_id}")
    items = parse_feedback(text)
    created_at = now or _now()
    with conn:
        for item in items:
            conn.execute(
                "INSERT INTO harness_feedback (run_id, created_at, papel, modelo, repo, alvo, ref, obstaculo,"
                " contorno, severidade, fingerprint, raw_block) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    run_id, created_at, run["papel"], run["modelo"], run["repo"], item["alvo"], item["ref"],
                    item["obstaculo"], item["contorno"], item["severidade"], item["fingerprint"], item["raw_block"],
                ),
            )
    return len(items)


def parse_since(value):
    match = re.fullmatch(r"([0-9]{1,4})([hdw])", value.strip().lower())
    if match is None:
        raise ValueError("--since espera um número seguido de h, d ou w, por exemplo 30d")
    unit = {"h": "hours", "d": "days", "w": "weeks"}[match.group(2)]
    return timedelta(**{unit: int(match.group(1))})


def atritos(conn, since="30d", top=20, now=None):
    current = now or datetime.now(timezone.utc)
    cutoff = (current - parse_since(since)).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = conn.execute(
        "SELECT fingerprint, alvo, ref, severidade, run_id, status FROM harness_feedback"
        " WHERE created_at >= ? ORDER BY created_at, id",
        (cutoff,),
    ).fetchall()
    groups = {}
    for row in rows:
        group = groups.get(row["fingerprint"])
        if group is None:
            group = groups[row["fingerprint"]] = {
                "fingerprint": row["fingerprint"],
                "alvo": row["alvo"],
                "ref": row["ref"],
                "severidade": row["severidade"],
                "total": 0,
                "runs": set(),
                "ultimo_run": row["run_id"],
                "status": row["status"],
            }
        group["total"] += 1
        group["runs"].add(row["run_id"])
        group["ultimo_run"] = row["run_id"]
        if SEVERITY_WEIGHT[row["severidade"]] > SEVERITY_WEIGHT[group["severidade"]]:
            group["severidade"] = row["severidade"]
        if row["status"] == "open":
            group["status"] = "open"
    ordered = sorted(groups.values(), key=lambda group: (-group["total"], group["fingerprint"]))
    result = []
    for group in ordered[: max(top, 0)]:
        result.append({**group, "runs": len(group["runs"])})
    return result


def mark_fixed(conn, fp, ref):
    if re.fullmatch(r"[0-9a-f]{12}", fp) is None:
        raise ValueError("fingerprint inválido: esperado 12 caracteres hexadecimais")
    fix_ref = truncate(mask(ref), LIMIT_REF)
    with conn:
        cursor = conn.execute(
            "UPDATE harness_feedback SET status = 'fixed', fix_ref = ? WHERE fingerprint = ? AND status = 'open'",
            (fix_ref, fp),
        )
    return cursor.rowcount


def list_runs(conn, limit=20):
    return conn.execute(
        "SELECT id, created_at, papel, modelo, status, task, pr_url FROM runs"
        " ORDER BY created_at DESC, id DESC LIMIT ?",
        (max(limit, 0),),
    ).fetchall()


def _read_input(path, stdin):
    if path is None or path == "-":
        return stdin.read()
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def _build_parser():
    parser = argparse.ArgumentParser(prog="report.py", description="Registro de runs e atritos do harness.")
    parser.add_argument("--db", default=None, help=f"caminho do banco SQLite (padrão: {DEFAULT_DB})")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="cria o banco e as tabelas")

    p_run = sub.add_parser("add-run", help="registra um run a partir de um JSON")
    p_run.add_argument("--file", default=None, help="arquivo JSON; sem ele lê o stdin")

    p_fb = sub.add_parser("add-feedback", help="extrai blocos HARNESS_FEEDBACK de um relatório")
    p_fb.add_argument("--run", required=True, help="id do run já registrado")
    p_fb.add_argument("--file", default=None, help="relatório ou saída do agente; sem ele lê o stdin")
    p_fb.add_argument("--no-harness-feedback", action="store_true", help="ignora o bloco, sem erro")

    p_at = sub.add_parser("atritos", help="agrupa os atritos por fingerprint")
    p_at.add_argument("--since", default="30d")
    p_at.add_argument("--top", type=int, default=20)
    p_at.add_argument("--json", action="store_true")

    p_fix = sub.add_parser("mark-fixed", help="marca um fingerprint como corrigido")
    p_fix.add_argument("fingerprint")
    p_fix.add_argument("--ref", required=True, help="PR ou commit da correção")

    p_list = sub.add_parser("list-runs", help="lista os runs mais recentes")
    p_list.add_argument("--limit", type=int, default=20)
    return parser


def main(argv=None, environ=None, stdin=None, stdout=None, stderr=None):
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "add-feedback" and (args.no_harness_feedback or not harness_feedback_enabled(environ)):
            print("harness_feedback desligado: 0 blocos registrados", file=stdout)
            return 0
        conn = connect(args.db)
        try:
            return _dispatch(conn, args, stdin, stdout)
        finally:
            conn.close()
    except (sqlite3.Error, OSError, ValueError) as error:
        print(f"erro: {error}", file=stderr)
        return 1


def _dispatch(conn, args, stdin, stdout):
    if args.command == "init":
        print(conn.execute("PRAGMA database_list").fetchone()["file"], file=stdout)
        return 0
    if args.command == "add-run":
        try:
            data = json.loads(_read_input(args.file, stdin))
        except json.JSONDecodeError as error:
            raise ValueError(f"JSON inválido: {error.msg}") from error
        print(add_run(conn, data), file=stdout)
        return 0
    if args.command == "add-feedback":
        count = add_feedback(conn, args.run, _read_input(args.file, stdin))
        print(f"{count} blocos registrados", file=stdout)
        return 0
    if args.command == "atritos":
        groups = atritos(conn, args.since, args.top)
        if args.json:
            print(json.dumps(groups, ensure_ascii=False, indent=2), file=stdout)
            return 0
        for group in groups:
            print(
                f"{group['fingerprint']} total={group['total']} runs={group['runs']} {group['severidade']}"
                f" {group['alvo']} {group['status']} ref={group['ref'] or '-'} ultimo_run={group['ultimo_run']}",
                file=stdout,
            )
        return 0
    if args.command == "mark-fixed":
        count = mark_fixed(conn, args.fingerprint, args.ref)
        if count == 0:
            raise ValueError(f"nenhum atrito aberto com o fingerprint {args.fingerprint}")
        print(f"{count} atritos marcados como corrigidos", file=stdout)
        return 0
    for row in list_runs(conn, args.limit):
        task = (row["task"] or "").replace("\n", " ")[:60]
        print(
            f"{row['id']} {row['created_at']} {row['papel'] or '-'} {row['modelo'] or '-'}"
            f" {row['status'] or '-'} {task} {row['pr_url'] or '-'}",
            file=stdout,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
