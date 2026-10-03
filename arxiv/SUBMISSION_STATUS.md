# Submission handoff

State: **NOT SUBMITTED — login required**. No submission ID or public arXiv ID exists for this manuscript.

The current in-app tab was rechecked through read-only DOM inspection: its path is `/login`, it displays “Log in to arXiv.org”, and neither the login identifier nor password is filled. It was marked for handoff again. Native accessibility reads timed out, but the documented browser DOM API works. Chrome connector access remains unavailable and an attempted ordinary Chrome launch was blocked by policy. Credentials were neither output nor copied. A visibility request did not make the browser visible while this chat was in the background; the preserved page is available when the chat is opened.

Everything before authenticated submission is prepared: `arxiv_submission.tar.gz`, independently compiled `submission_preview.pdf`, hash/build report, and complete title/author/abstract/category/license fields in `metadata.json`. The chosen primary category is cs.PL because the contribution concerns semantics and exact program analysis. No additional cross-list is necessary. The intended perpetual, non-exclusive arXiv license matches the author's previously verified choice.

After the author signs in, the remaining workflow is to upload the source archive, verify the arXiv compiler/top-level main.tex, inspect the server-generated PDF, enter/check metadata, and finish the ordinary submission. A new endorsement, CAPTCHA, OTP, or explicitly personal legal declaration must be completed by the author. No category change will be used to evade endorsement.

Current official requirements checked on 2026-10-03: [TeX submission](https://info.arxiv.org/help/submit_tex.html), [endorsement](https://info.arxiv.org/help/endorsement.html), [licenses](https://info.arxiv.org/help/license/index.html), and [category taxonomy](https://arxiv.org/category_taxonomy).
