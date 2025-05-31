import lightkurve as lk
from bokeh.io import output_notebook
output_notebook()


# 使用 search_targetpixelfile() 來搜尋 Kepler-10 的資料
tpf_search_result = lk.search_targetpixelfile('Kepler-10', mission='Kepler')
tpf = tpf_search_result[0].download()

# 使用切片以減少資料量，提高效能
with open("output.html", "w") as f:
    f.write(tpf[0:1000].interact().repr_html())
