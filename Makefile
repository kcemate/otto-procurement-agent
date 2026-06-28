PYTHON ?= python3
PORT ?= 8791

.PHONY: demo site serve verify package

demo:
	$(PYTHON) scripts/run_full_cycle.py

site: demo
	@echo "Site rendered to ./site"

serve:
	cd site && $(PYTHON) -m http.server $(PORT) --bind 127.0.0.1

verify:
	$(PYTHON) -m json.tool data/audit.json >/dev/null
	$(PYTHON) -m json.tool data/ledger.json >/dev/null
	$(PYTHON) -m json.tool data/evidence_pack.json >/dev/null
	$(PYTHON) -m json.tool site/data.json >/dev/null
	node --check site/app.js
	@echo "verify_ok"

package:
	rm -f submission/otto-procurement-submission-package.zip
	zip -r submission/otto-procurement-submission-package.zip README.md data scripts site docs .github Makefile submission/video_script.md submission/x_post.md submission/x_post_short.md submission/discord_submission.md submission/form_answers.md submission/otto-procurement-tenx-demo.mp4 submission/tenx-site-screenshot.png strategy/10x-gap-analysis.md strategy/council-10x.md -x '*/.herenow/*' '*/.herenow' >/tmp/otto_procurement_zip.log
	@echo "package_ok"
