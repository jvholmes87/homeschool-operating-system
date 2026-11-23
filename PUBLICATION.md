# Static site publication

`.github/security/publication-files.txt` lists every file in the site artifact. `site_release.py stage` builds a fresh directory from that list. The publication check verifies a signature over the sorted paths and SHA-256 digests of exactly those files. A changed or extra file requires a new privacy review and signature.

## Review an updated site

1. Review the candidate commit and preview its allowlisted artifact. Verify the rendered pages, coverage tool, document links, images, and the two intended sample PDFs. The scanner checks text and selected metadata. Review visual content in images and PDFs before signing.
2. Run the trusted privacy checker from the separate release workstation with the owner’s private rules. Sign the manifest for the exact reviewed Git tree only after the scan and preview pass. Keep the rules and signing key in the private store. Commit the detached signature under `.github/security/privacy.sig`.
3. Require the `Publishable site` check on the release PR, then get owner approval before merging or publishing. Changes to the workflow, public signing key, allowlist, or check implementation require a security review.

## Hosting setup and release

GitHub Pages must be switched from branch publishing to GitHub Actions after the preview is accepted. Keep the existing custom domain configuration. Set the owner-managed `HOMESCHOOL_PUBLICATION_KEY_SHA256` repository variable to the fingerprint of the approved PEM file. Restrict the `github-pages` environment to `main` and require owner approval. Dispatch the workflow from `main` for an approved release. The workflow verifies the artifact before uploading it and uses the protected environment for deployment.

Cloudflare Pages must stop publishing the repository root. Pause automatic production and preview builds after validating the replacement preview. Use the existing project to publish a verified static artifact via Wrangler with the intended branch name. Verify the signed artifact immediately before upload. Test the Cloudflare headers on the preview host before approving production and verify them again after release. GitHub Pages does not apply the Cloudflare `_headers` file.

## Generator dependencies

Use CPython 3.12 on x86-64 Windows or Linux. Install `requirements-generators.txt` in a virtual environment with `python -m pip install --require-hashes --only-binary=:all: -r requirements-generators.txt`. The lock includes the Python dependencies for `build_docs.py`, the sample PDF generators and the private artifact scanner. WeasyPrint also requires native Pango and HarfBuzz from the operating system. See [WeasyPrint installation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html). CI installs those libraries in the Ubuntu 24.04 runner and exercises an invented Markdown-to-PDF fixture.
