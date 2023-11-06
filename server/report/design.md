# Reporter plugin architecture

Proposals:

- one plugin for each report type
- decouple a report templates form report generators
- decouple styles from templates
- decouple textblocks from templates

This means that there need template plugins and report plugins and results in complete freedom when it comes to report generation.

I imagine the following flow.


1. Backend prepares the report context, which should contain **all** relevant data for the report generation.
2. User selects the template and generator plugin
3. Backend initialises the reporter plugin and the template plugin, passes a configuration and context to it.
4. the reporter plugin preprocesses the data
5. the template plugin prepares the template acroding to the users config and returns the template to the reporter plugin
6. the reporter plugin parses the context into the template
7. the reporter plugin postprecesses the template
8. and generates the report

The main reasons for this are:

#### dynamic templates

Lets say the base template provides the following sections:
- overview
- scope
- mgmt summary
- vulnerabilities
- port scans
- ...
then we could achieve, with a single pdf generator plugin the following report types:
- pentest report
- bugbounty report (only vulnerabilities)
- single vulnerability
- asset inventory
- port scan report
- ...
by simply configuring the context provided to the generator and the templates config.
These choices can be stored by the users into report settings to quickly generate a report of chosen type
(All sections von TemplateA and basic pdf reporter with the standart context and stye X is standard report for customer Z)
When then the text is seperated from the rest, we could just allow uses to write different textblock for the sections according to their needs and add it to the context in a step before




#### interchangable and extensible generators

When we want a different strategy for report generation, lets say to create different chars, it should be enough to create the following class:

```python
class PDFReporterWithCharts(BasePDFReporter):

    def _create_chart(self, data):
        # create your chart from input
        return chart

    def _preprocess(self):
        super()._preprocess()
        chart_data = context["key"] # gather data for chart
        chart = self._create_chart(chart_data)
        self.processed_context["key"] = chart # set the chart in the already prepared context
```


### Implementation

#### loader classes for template and reporter plugins

The loader class exposes 4 methods:

- get_available_plugins()
    - returns list of plugins
- get_plugin_options()
    - returns all options available to the user
- init_plugin()
    - returns an initialized instance of the plugin to the user
    - init_plugin for repoertes has the arguments (name, config, context, template) and for templates (name, config)
- generate
    - generate report / template
