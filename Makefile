PYTHON ?= python3
PORT ?= 8791

.PHONY: demo site serve verify nvidia-verify package

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
	$(PYTHON) -m json.tool data/nemotron_risk_review.json >/dev/null
	$(PYTHON) -m json.tool data/nemoclaw_safety_rack.json >/dev/null
	$(PYTHON) -m json.tool data/nvidia_integrations.json >/dev/null
	$(PYTHON) -m json.tool data/nvidia_skills_access.json >/dev/null
	$(PYTHON) -m json.tool site/data.json >/dev/null
	node --check site/app.js
	@echo "verify_ok"

nvidia-verify:
	$(PYTHON) nvidia/nemotron_client.py
	$(PYTHON) nvidia/safety_rack.py
	$(PYTHON) scripts/probe_nvidia_skills.py
	$(PYTHON) scripts/gpu_probe.py
	@echo "nvidia_verify_ok"

package:
	rm -f submission/otto-procurement-submission-package.zip
	zip -r submission/otto-procurement-submission-package.zip README.md data scripts nvidia site docs .github Makefile submission/video_script.md submission/x_post.md submission/x_post_short.md submission/x_reply_nvidia_proof.md submission/discord_submission.md submission/form_answers.md submission/otto-procurement-tenx-demo.mp4 submission/otto-procurement-cinematic-x-demo.mp4 submission/cinematic_video_notes.md submission/cinematic_voiceover.txt submission/cinematic_voiceover.ogg submission/cinematic_background.jpg submission/mobile-live-dashboard.png submission/cinematic-contact-sheet-final.jpg submission/tenx-site-screenshot.png submission/tenx-github-pages-screenshot.png strategy/10x-gap-analysis.md strategy/council-10x.md strategy/nvidia-nemotron-moa-rescue.md -x '*/.herenow/*' '*/.herenow' >/tmp/otto_procurement_zip.log
	@echo "package_ok"
