# Change NOVA files from an iPhone

This workflow does not need an always-on server or a language model.
It runs in GitHub Actions and creates a reviewable pull request.

1. Open [Owner File Change](https://github.com/woutswouts2004-sudo/Project-NOVA/actions/workflows/owner-file-change.yml).
2. Tap **Run workflow**.
3. Enter the repository-relative `target`, for example `docs/notes.md`.
4. Enter the complete replacement `content`.
5. Run the workflow. It syntax-checks Python, runs the repository unit
   tests, and opens a pull request if the change succeeds.
6. Open the pull request, review the diff, and merge it.

This is a **working owner-directed file-update mechanism** if GitHub Actions
has permission to create branches and pull requests. GitHub may require the
repository owner to enable **Settings → Actions → General → Allow GitHub
Actions to create and approve pull requests**. The workflow never merges
its own PR.

It can modify normal repository files without the model being online, but
does not interpret natural-language instructions. It requires replacement
file text. Protected security/workflow and credential paths remain excluded.

The public GitHub Pages chat still needs a separate HTTPS model backend
to respond intelligently. GitHub Pages cannot host Python or a model
server. Do not put provider tokens into website JavaScript.
