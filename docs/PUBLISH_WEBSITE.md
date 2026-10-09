# Publish NOVA on GitHub Pages

The public website source is `docs/index.html` in this repository.

## Owner setup (GitHub Free)

GitHub Pages generally requires a **public repository** on GitHub Free.
The repository is currently private. Making it public exposes its source
code and commit history, but does not grant visitors permission to edit it.

1. Review the repository's code and commit history for secrets or personal
   information before making it public. Never publish API keys.
2. In the GitHub repository, open **Settings → General → Danger Zone →
   Change repository visibility → Public** and confirm.
3. Open **Settings → Pages**.
4. Under **Build and deployment**, select **Deploy from a branch**.
5. Choose **main** and **/docs**, then **Save**.
6. Wait for GitHub to finish publishing. The likely website address is
   `https://woutswouts2004-sudo.github.io/Project-NOVA/`, but do not
   assume it is live until GitHub Pages displays the published URL.

This project cannot change repository visibility or Pages settings through
the currently connected GitHub actions. The owner must perform those steps
in GitHub's web settings.

## Public chat security

The Pages interface is a static site. It can receive user input and keep
a local journal, but it does not run Python or host a model. The initial
website explicitly labels its responses as demos.

For a genuinely public AI chat service, deploy a separate API service
with the following controls:
- Keep model API keys on the server, never in browser JavaScript.
- Limit anonymous messages, request size, and model tokens.
- Implement per-user/IP rate limits and abuse handling.
- Set provider-side usage quotas and prevent surprise charges.
- Do not expose the private journal, development logs, or admin endpoints.
- Use separate owner authentication for any configuration changes.
- Make data retention and privacy terms clear before storing messages.
- Ensure public visitor messages do not become privileged instructions.

## Verification
On the published Pages URL, confirm the Conversation, Exploration, Memory,
and About tabs work. Send a test message and confirm the explicitly labeled
demo reply appears. Export and erase the local journal. Open About and run
the interface diagnostics. These tests confirm the website only; they do
not prove a real language model is connected.

## Important distinction
The public repository is editable only by authorized collaborators.
Public visitors can inspect or fork the code and submit suggestions,
but cannot push changes to the original repository without write access.
