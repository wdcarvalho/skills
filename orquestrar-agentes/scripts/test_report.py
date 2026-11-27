import io
import json
import os
import stat
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import report


def block(alvo="template", obstaculo="brief sem caminho do contexto", severidade="contornou-barato", ref=None, contorno=None):
    lines = ["HARNESS_FEEDBACK", f"alvo: {alvo}"]
    if ref is not None:
        lines.append(f"ref: {ref}")
    lines.append(f"obstaculo: {obstaculo}")
    if contorno is not None:
        lines.append(f"contorno: {contorno}")
    lines.append(f"severidade: {severidade}")
    lines.append("FIM_HARNESS_FEEDBACK")
    return "\n".join(lines)


class ParserTest(unittest.TestCase):
    def test_valid_block(self):
        items = report.parse_feedback("texto antes\n" + block(ref="templates/context.md", contorno="li o brief") + "\nPR: x")
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item["alvo"], "template")
        self.assertEqual(item["ref"], "templates/context.md")
        self.assertEqual(item["obstaculo"], "brief sem caminho do contexto")
        self.assertEqual(item["contorno"], "li o brief")
        self.assertEqual(item["severidade"], "contornou-barato")
        self.assertEqual(len(item["fingerprint"]), 12)

    def test_optional_fields_can_be_empty(self):
        item = report.parse_feedback(block(severidade="travou"))[0]
        self.assertEqual(item["ref"], "")
        self.assertEqual(item["contorno"], "")

    def test_invalid_blocks_are_discarded_whole(self):
        invalid = [
            block(alvo="guia-papel"),
            block(severidade="grave"),
            block(obstaculo=""),
            "HARNESS_FEEDBACK\nalvo: skill\nseveridade: travou\nFIM_HARNESS_FEEDBACK",
            "HARNESS_FEEDBACK\nalvo: skill\nobstaculo: sem fechamento\nseveridade: travou",
            "FIM_HARNESS_FEEDBACK",
        ]
        for text in invalid:
            with self.subTest(text=text):
                self.assertEqual(report.parse_feedback(text), [])

    def test_invalid_block_does_not_discard_valid_neighbours(self):
        text = block(alvo="inexistente") + "\n" + block(obstaculo="segundo bloco valido")
        items = report.parse_feedback(text)
        self.assertEqual([item["obstaculo"] for item in items], ["segundo bloco valido"])

    def test_fourth_block_is_ignored(self):
        text = "\n".join(block(obstaculo=f"obstaculo distinto {word}") for word in ("alfa", "beta", "gama", "delta"))
        items = report.parse_feedback(text)
        self.assertEqual(len(items), 3)
        self.assertNotIn("delta", " ".join(item["obstaculo"] for item in items))

    def test_repeated_key_keeps_first(self):
        text = "HARNESS_FEEDBACK\nalvo: skill\nalvo: sandbox\nobstaculo: primeiro\nobstaculo: segundo\nseveridade: travou\nFIM_HARNESS_FEEDBACK"
        item = report.parse_feedback(text)[0]
        self.assertEqual(item["alvo"], "skill")
        self.assertEqual(item["obstaculo"], "primeiro")

    def test_unknown_key_is_ignored(self):
        text = "HARNESS_FEEDBACK\nfingerprint: abc\nalvo: skill\nobstaculo: x\nextra: y\nseveridade: travou\nFIM_HARNESS_FEEDBACK"
        item = report.parse_feedback(text)[0]
        self.assertNotEqual(item["fingerprint"], "abc")
        self.assertNotIn("extra", item["raw_block"])

    def test_agent_fingerprint_never_wins(self):
        with_agent = "HARNESS_FEEDBACK\nfingerprint: 000000000000\nalvo: skill\nobstaculo: x\nseveridade: travou\nFIM_HARNESS_FEEDBACK"
        without = "HARNESS_FEEDBACK\nalvo: skill\nobstaculo: x\nseveridade: travou\nFIM_HARNESS_FEEDBACK"
        self.assertEqual(report.parse_feedback(with_agent)[0]["fingerprint"], report.parse_feedback(without)[0]["fingerprint"])

    def test_markers_ignore_case_and_spacing(self):
        text = "  harness_feedback  \nALVO: Skill\n obstaculo : algo travou \nSeveridade: TRAVOU\n  fim_harness_feedback "
        items = report.parse_feedback(text)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["alvo"], "skill")
        self.assertEqual(items[0]["severidade"], "travou")

    def test_markdown_decorated_markers(self):
        text = "**HARNESS_FEEDBACK**\nalvo: config\nobstaculo: x\nseveridade: travou\n`FIM_HARNESS_FEEDBACK`"
        self.assertEqual(len(report.parse_feedback(text)), 1)

    def test_never_raises(self):
        for value in (None, 123, b"bytes", ["lista"], "\x00\x01HARNESS_FEEDBACK\n\xff", ""):
            with self.subTest(value=value):
                self.assertEqual(report.parse_feedback(value), [])


class FingerprintTest(unittest.TestCase):
    def test_numeric_variants_share_group(self):
        fingerprints = {
            report.fingerprint("ferramenta", "t3", f"timeout de {value} no lancamento")
            for value in ("30s", "300s", "45 s")
        }
        self.assertEqual(len(fingerprints), 1)

    def test_accents_and_case_are_ignored(self):
        self.assertEqual(
            report.fingerprint("skill", "SKILL.md", "Instrução AMBÍGUA"),
            report.fingerprint("skill", "skill.md", "instrucao ambigua"),
        )

    def test_different_alvo_or_text_changes_fingerprint(self):
        base = report.fingerprint("skill", "", "brief ambiguo")
        self.assertNotEqual(base, report.fingerprint("template", "", "brief ambiguo"))
        self.assertNotEqual(base, report.fingerprint("skill", "", "brief quebrado"))

    def test_normalize(self):
        self.assertEqual(report.normalize("  Falha 30 s em Ação!! "), "falha#s em acao")

    def test_parser_groups_numeric_variants(self):
        fingerprints = {
            report.parse_feedback(block(obstaculo=f"CLI demorou {value} para responder"))[0]["fingerprint"]
            for value in ("30s", "300s", "45 s")
        }
        self.assertEqual(len(fingerprints), 1)


class MaskingTest(unittest.TestCase):
    def test_email_is_masked(self):
        item = report.parse_feedback(block(obstaculo="enviei para pessoa.teste@example.com e falhou"))[0]
        self.assertNotIn("@", item["obstaculo"])
        self.assertIn("[e-mail omitido]", item["obstaculo"])
        self.assertNotIn("@", item["raw_block"])

    def test_cpf_is_masked(self):
        item = report.parse_feedback(block(contorno="usei 123.456.789-09 no teste"))[0]
        self.assertNotIn("123.456.789-09", item["contorno"])
        self.assertIn("[CPF omitido]", item["contorno"])

    def test_phone_and_token_are_masked(self):
        text = "ligar (11) 91234-5678 com ghp_" + "a" * 24
        item = report.parse_feedback(block(obstaculo=text))[0]
        self.assertIn("[telefone omitido]", item["obstaculo"])
        self.assertIn("[segredo omitido]", item["obstaculo"])
        self.assertNotIn("ghp_", item["obstaculo"])

    def test_ref_is_masked(self):
        item = report.parse_feedback(block(ref="pessoa.teste@example.com"))[0]
        self.assertNotIn("@", item["ref"])

    def test_masking_happens_before_truncation(self):
        obstaculo = "x" * 290 + " pessoa.teste@example.com"
        item = report.parse_feedback(block(obstaculo=obstaculo))[0]
        self.assertNotIn("pessoa", item["obstaculo"])
        self.assertNotIn("@", item["obstaculo"])

    def test_uuid_and_full_sha_are_kept(self):
        identifier = "2e98a37" + "0" * 33
        uuid_value = "123e4567-e89b-12d3-a456-426614174000"
        item = report.parse_feedback(block(obstaculo=f"commit {identifier} e run {uuid_value}"))[0]
        self.assertIn(identifier, item["obstaculo"])
        self.assertIn(uuid_value, item["obstaculo"])


class TruncationTest(unittest.TestCase):
    def test_limits(self):
        item = report.parse_feedback(block(obstaculo="o" * 500, contorno="c" * 500, ref="r" * 500))[0]
        self.assertEqual(len(item["obstaculo"]), report.LIMIT_TEXT)
        self.assertEqual(len(item["contorno"]), report.LIMIT_TEXT)
        self.assertEqual(len(item["ref"]), report.LIMIT_REF)

    def test_text_within_limit_is_untouched(self):
        item = report.parse_feedback(block(obstaculo="o" * 300))[0]
        self.assertEqual(len(item["obstaculo"]), 300)

    def test_cut_never_leaves_half_a_marker(self):
        prefix = "x" * (report.LIMIT_TEXT - 5)
        item = report.parse_feedback(block(obstaculo=prefix + "a@b.co fim"))[0]
        self.assertNotIn("[e-m", item["obstaculo"].replace("[e-mail omitido]", ""))


class FlagTest(unittest.TestCase):
    def test_default_is_on(self):
        self.assertTrue(report.harness_feedback_enabled({}))

    def test_off_values(self):
        for value in ("0", "false", "OFF", "no"):
            with self.subTest(value=value):
                self.assertFalse(report.harness_feedback_enabled({report.ENV_FLAG: value}))

    def test_on_values(self):
        for value in ("1", "true", "on", ""):
            with self.subTest(value=value):
                self.assertTrue(report.harness_feedback_enabled({report.ENV_FLAG: value}))


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "dados", "runs.sqlite")

    def run_cli(self, *argv, stdin="", environ=None):
        out, err = io.StringIO(), io.StringIO()
        code = report.main(["--db", self.path, *argv], environ=environ, stdin=io.StringIO(stdin), stdout=out, stderr=err)
        return code, out.getvalue(), err.getvalue()

    def new_run(self, **extra):
        data = {"id": "run-1", "papel": "implementacao", "modelo": "claude-sonnet-5-5", "repo": "exemplo/repo", "status": "feito"}
        data.update(extra)
        code, out, _ = self.run_cli("add-run", stdin=json.dumps(data))
        self.assertEqual(code, 0)
        return out.strip()

    def count(self, table="harness_feedback"):
        conn = report.connect(self.path)
        try:
            return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        finally:
            conn.close()

    def test_init_creates_private_files(self):
        code, _, _ = self.run_cli("init")
        self.assertEqual(code, 0)
        self.assertEqual(stat.S_IMODE(os.stat(os.path.dirname(self.path)).st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(os.stat(self.path).st_mode), 0o600)

    def test_schema_and_indexes(self):
        conn = report.connect(self.path)
        try:
            tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
            indexes = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'index'")}
            columns = [row[1] for row in conn.execute("PRAGMA table_info(harness_feedback)")]
        finally:
            conn.close()
        self.assertLessEqual({"runs", "harness_feedback"}, tables)
        self.assertLessEqual(
            {"idx_harness_feedback_fingerprint", "idx_harness_feedback_created_at", "idx_harness_feedback_status"}, indexes
        )
        self.assertEqual(
            columns,
            ["id", "run_id", "created_at", "papel", "modelo", "repo", "alvo", "ref", "obstaculo", "contorno",
             "severidade", "fingerprint", "raw_block", "status", "fix_ref"],
        )

    def test_add_feedback_stores_blocks_with_run_context(self):
        run_id = self.new_run()
        code, out, _ = self.run_cli("add-feedback", "--run", run_id, stdin=block(ref="SKILL.md"))
        self.assertEqual(code, 0)
        self.assertIn("1 blocos", out)
        conn = report.connect(self.path)
        try:
            row = conn.execute("SELECT * FROM harness_feedback").fetchone()
        finally:
            conn.close()
        self.assertEqual((row["papel"], row["modelo"], row["repo"], row["status"]), ("implementacao", "claude-sonnet-5-5", "exemplo/repo", "open"))

    def test_add_feedback_from_file(self):
        run_id = self.new_run()
        report_file = os.path.join(self.tmp.name, "relatorio.md")
        with open(report_file, "w", encoding="utf-8") as handle:
            handle.write(block())
        code, _, _ = self.run_cli("add-feedback", "--run", run_id, "--file", report_file)
        self.assertEqual(code, 0)
        self.assertEqual(self.count(), 1)

    def test_flag_off_by_option_is_silent(self):
        run_id = self.new_run()
        code, out, err = self.run_cli("add-feedback", "--run", run_id, "--no-harness-feedback", stdin=block())
        self.assertEqual((code, err), (0, ""))
        self.assertIn("desligado", out)
        self.assertEqual(self.count(), 0)

    def test_flag_off_by_env_is_silent_even_with_unknown_run(self):
        code, _, err = self.run_cli("add-feedback", "--run", "nao-existe", stdin=block(), environ={report.ENV_FLAG: "0"})
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(self.count(), 0)

    def test_flag_on_by_env_registers(self):
        run_id = self.new_run()
        code, _, _ = self.run_cli("add-feedback", "--run", run_id, stdin=block(), environ={report.ENV_FLAG: "1"})
        self.assertEqual(code, 0)
        self.assertEqual(self.count(), 1)

    def test_unknown_run_is_an_error_when_enabled(self):
        code, _, err = self.run_cli("add-feedback", "--run", "nao-existe", stdin=block())
        self.assertEqual(code, 1)
        self.assertIn("run não encontrado", err)

    def test_report_without_block_registers_zero(self):
        run_id = self.new_run()
        code, out, _ = self.run_cli("add-feedback", "--run", run_id, stdin="estado: feito\nsem atrito")
        self.assertEqual(code, 0)
        self.assertIn("0 blocos", out)

    def test_add_run_masks_free_text(self):
        self.new_run(summary="falou com pessoa.teste@example.com", task="CPF 123.456.789-09")
        conn = report.connect(self.path)
        try:
            row = conn.execute("SELECT summary, task FROM runs").fetchone()
        finally:
            conn.close()
        self.assertNotIn("@", row["summary"])
        self.assertNotIn("123.456.789-09", row["task"])

    def test_add_run_rejects_invalid_json(self):
        code, _, err = self.run_cli("add-run", stdin="{nao e json")
        self.assertEqual(code, 1)
        self.assertIn("JSON inválido", err)

    def test_atritos_groups_by_fingerprint_and_orders_by_total(self):
        for index in range(3):
            run_id = self.new_run(id=f"run-{index}")
            self.run_cli("add-feedback", "--run", run_id, stdin=block(obstaculo=f"CLI demorou {30 * (index + 1)}s", severidade="contornou-caro"))
        other = self.new_run(id="run-x")
        self.run_cli("add-feedback", "--run", other, stdin=block(alvo="sandbox", obstaculo="sem rede", severidade="travou"))
        code, out, _ = self.run_cli("atritos", "--since", "30d", "--top", "20", "--json")
        self.assertEqual(code, 0)
        groups = json.loads(out)
        self.assertEqual([group["total"] for group in groups], [3, 1])
        self.assertEqual(groups[0]["runs"], 3)
        self.assertEqual(groups[0]["alvo"], "template")
        self.assertEqual(groups[1]["severidade"], "travou")

    def test_atritos_top_and_since(self):
        conn = report.connect(self.path)
        try:
            report.add_run(conn, {"id": "r1", "papel": "p"}, now="2020-01-01T00:00:00Z")
            report.add_feedback(conn, "r1", block(obstaculo="antigo"), now="2020-01-01T00:00:00Z")
            report.add_run(conn, {"id": "r2", "papel": "p"})
            report.add_feedback(conn, "r2", block(obstaculo="novo um") + "\n" + block(obstaculo="novo dois"))
            self.assertEqual(len(report.atritos(conn, "30d", 20)), 2)
            self.assertEqual(len(report.atritos(conn, "30d", 1)), 1)
            self.assertEqual(len(report.atritos(conn, "9999d", 20)), 3)
            self.assertEqual(len(report.atritos(conn, "1d", 20)), 2)
        finally:
            conn.close()

    def test_atritos_text_output(self):
        run_id = self.new_run()
        self.run_cli("add-feedback", "--run", run_id, stdin=block(ref="SKILL.md"))
        code, out, _ = self.run_cli("atritos")
        self.assertEqual(code, 0)
        self.assertIn("total=1", out)
        self.assertIn("ref=SKILL.md", out)

    def test_invalid_since(self):
        code, _, err = self.run_cli("atritos", "--since", "ontem")
        self.assertEqual(code, 1)
        self.assertIn("--since", err)

    def test_mark_fixed(self):
        run_id = self.new_run()
        self.run_cli("add-feedback", "--run", run_id, stdin=block())
        fingerprint = json.loads(self.run_cli("atritos", "--json")[1])[0]["fingerprint"]
        code, out, _ = self.run_cli("mark-fixed", fingerprint, "--ref", "PR #3")
        self.assertEqual(code, 0)
        self.assertIn("1 atritos", out)
        conn = report.connect(self.path)
        try:
            row = conn.execute("SELECT status, fix_ref FROM harness_feedback").fetchone()
        finally:
            conn.close()
        self.assertEqual((row["status"], row["fix_ref"]), ("fixed", "PR #3"))
        self.assertEqual(self.run_cli("mark-fixed", fingerprint, "--ref", "PR #3")[0], 1)

    def test_mark_fixed_rejects_bad_fingerprint(self):
        code, _, err = self.run_cli("mark-fixed", "xyz", "--ref", "PR #3")
        self.assertEqual(code, 1)
        self.assertIn("fingerprint inválido", err)

    def test_list_runs(self):
        self.new_run(id="run-a", task="primeira tarefa")
        code, out, _ = self.run_cli("list-runs")
        self.assertEqual(code, 0)
        self.assertIn("run-a", out)
        self.assertIn("primeira tarefa", out)

    def test_feedback_never_changes_run_result(self):
        run_id = self.new_run(status="feito")
        self.run_cli("add-feedback", "--run", run_id, stdin=block(severidade="travou"))
        conn = report.connect(self.path)
        try:
            status = conn.execute("SELECT status FROM runs WHERE id = ?", (run_id,)).fetchone()[0]
        finally:
            conn.close()
        self.assertEqual(status, "feito")


if __name__ == "__main__":
    unittest.main()
