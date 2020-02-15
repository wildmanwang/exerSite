class Pages():
    def __init__(self, totalCnt, perCnt, baseUrl, curPage=1):
        self.totalCnt = totalCnt
        self.perCnt = perCnt
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
        pagestr = '<div><select id="PAGE_reccnt_perpage_select" class="page right" style="width: 45px; color: rgb(127, 127, 127); margin: 0 2px 0 10px; "><option value="5">5</option><option value="10">10</option><option value="20">20</option><option value="50">50</option></select></div>'
        for page in range(self.pageCnt, 0, -1):
            if self.curPage == page:
                pagestr += '<span class="right" style="display: inline-block; color: rgb(127, 127, 127); margin: 0 7px; ">{page}</span>'.format(baseUrl=self.baseUrl, page=page)
            else:
                pagestr += '<a class="right" href="{baseUrl}{page}" style="display: inline-block; margin: 0 7px; ">{page}</a>'.format(baseUrl=self.baseUrl, page=page)
        pagestr += "</div>"
        return pagestr
