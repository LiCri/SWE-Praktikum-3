echo "Compile markdown"
pandoc -f markdown -t html -o swe_p3_testdoc.0.pdf.html -s -N --number-offset=0 --template=.\pdf-Konvertierungsfiles\hdoc.tpl -H .\pdf-Konvertierungsfiles\hdoc_pdf.css.inc -H  .\pdf-Konvertierungsfiles\hdoc_syntax.css.inc --highlight-style pygments swe_p3_testdoc.0.md
echo "Compile pdf"
prince swe_p3_testdoc.0.pdf.html -o swe_p3_testdoc.0.pdf
pause