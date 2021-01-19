"""
This template produces Github-flavored markdown documents.

If you want to convert this markdown document to PDF,
the recommended way of doing it is using the `md-to-pdf` tool.

The documentation of the tool can be seen on
https://www.npmjs.com/package/md-to-pdf.

To install the tool, run the following command.

$ npm i -g md-to-pdf

Since the produced markdown document can be quite large
in width due to some tables, it is recommended to set
the output PDF margin to a lower value than the default setting.

It is recommended that the right and left margins should
be less than or equal to "10mm". One can use the following command
to generate the PDF output.

$ md-to-pdf documentation.md --pdf-options '{"margin": "10mm", "printBackground": true}'
"""

internal_services = {
    "MC",
}
