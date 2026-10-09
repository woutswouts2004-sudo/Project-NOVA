# Privacy for the public NOVA interface

The public website stores conversation messages in the visitor's own
browser storage when available. Messages are not shared with other
visitors or automatically committed to GitHub.

The public API implementation, if later deployed, sends a limited recent
history to the configured model provider. This may expose the content to
that provider and its retention policies. The current API does not store
conversations on the server, but infrastructure providers may collect
technical access logs.

Avoid sending confidential information. A visitor can export or erase
their own browser journal. Erasing local storage does not erase records
already sent to an external model provider.

NOVA's internal development journal must not be mixed with public visitor
messages. Owner credentials and API keys must remain server-side.
