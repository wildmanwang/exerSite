class Pages():
    def __init__(self, totalCnt, perCnt, baseUrl, curPage=1, funClick=""):
        self.totalCnt = totalCnt
        self.perCnt = perCnt
        self.funClick = funClick
        self.baseUrl = baseUrl
        self.curPage = int(curPage)

    @property
    def pageCnt(self):
        cnt, i = divmod(self.totalCnt, self.perCnt)
        if i:
            cnt += 1
        return cnt

    @property
    def startRec(self):
        return (self.curPage - 1) * self.perCnt

    @property
    def endRec(self):
        recEnd = self.curPage * self.perCnt
        if recEnd > self.totalCnt:
            recEnd = self.totalCnt
        return recEnd

    @property
    def pageStr(self):
        pagestr = '<div id="pageBanner" style="padding: 10px; overflow: hidden; "><select id="PAGE_reccnt_perpage_select" class="page right" style="width: 45px; color: rgb(127, 127, 127); margin: 0 2px 0 10px; "><option value="5">5</option><option value="10">10</option><option value="20">20</option><option value="50">50</option></select>'
        for page in range(self.pageCnt, 0, -1):
            if self.curPage == page:
                pagestr += '<span class="right" style="color: rgb(127, 127, 127); margin: 0 7px; ">{page}</span>'.format(page=page)
            else:
                if len(self.funClick) > 0:
                    pagestr += '<a class="right" href="javascript:void(0);" onclick="{funClick}(\'{baseUrl}\', {page})" style="display: inline-block; margin: 0 7px; ">{page}</a>'.format(funClick=self.funClick, baseUrl=self.baseUrl, page=page)
                else:
                    pagestr += '<a class="right" href="{baseUrl}{page}" style="display: inline-block; margin: 0 7px; ">{page}</a>'.format(baseUrl=self.baseUrl, page=page)
        pagestr += "</div>"
        return pagestr
