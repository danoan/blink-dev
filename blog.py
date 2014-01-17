#coding:utf-8

def main(request,lang,page):
    if page is None:
        page = "app"

    page = "%s_%s.html" % (page,lang)

    return render_template(page,**paths_dict)	