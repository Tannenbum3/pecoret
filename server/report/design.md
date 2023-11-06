# Reporter plugin architecture

Proposals:

- one plugin for each report type
- decouple a report templates form report generators
- decouple styles from templates

This means that there need template plugins and report plugins and results in complete freedom when it comes to report generation.

I imagine the following flow.


1. Backend prepares the report context, which should contain **all** relevant data for the report generation.
2. User selects the template and generator plugin
3. Backend initialises the reporter plugin and the template plugin, passes a configuration and context to it.
4. the reporter plugin preprocesses the data
5. the template plugin prepares the template acroding to the users config and returns the template to the reporter plugin
6. the reporter plugin parses the context into the template
7. the reporter plugin generates the templates
8. and postprocesses it



