# Release verification

A source commit is not a verified deployment. Before announcing a release:

1. Confirm GitHub Pages deployment completed successfully for the commit.
2. Open the live HTTPS website in Safari.
3. Check navigation, Send, local history, export, import and erase.
4. Confirm the demo mode is clearly labeled if no API is configured.
5. Check mobile viewport and accessibility labels.
6. Verify no credentials or private transcripts are in published files.
7. If a backend is connected, verify /health and a bounded chat request.
8. Confirm backend logs do not contain private conversation text.
9. Confirm owner kill switch, budget cap and rate limits.
10. Document what was and was not tested.

Never describe the public interface as a fully functioning independent
AI until a real model and independent runtime are deployed and tested.
