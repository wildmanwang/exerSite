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
        pagestr = ""
        for page in range(1, self.pageCnt):
            if self.curPage == page:
                pagestr += '<span class="page active">{page}</span>'.format(baseUrl=self.baseUrl, page=page)
            else:
                pagestr += '<a href="{baseUrl}{page}" class="page">{page}</a>'.format(baseUrl=self.baseUrl, page=page)
        return pagestr
