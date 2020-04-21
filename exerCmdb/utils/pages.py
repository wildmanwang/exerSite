class Pages():
    def __init__(self, totalCnt, perCnt, jsonUrl, newUrl, curPage=1, funClick=""):
        """
        分页控件
        :param totalCnt:    总记录条数
        :param perCnt:      每页记录条数
        :param jsonUrl:     当前页的基础地址
        :param newUrl:      当前页的新增地址
        :param curPage:     当前页码
        :param funClick:    点击跳转，默认空，即a标签跳转
        """
        self.totalCnt = totalCnt
        self.perCnt = perCnt
        self.jsonUrl = jsonUrl
        self.newUrl = newUrl
        self.curPage = int(curPage)
        self.funClick = funClick

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
                    pagestr += '<a class="right" href="javascript:void(0);" onclick="{funClick}(\'{jsonUrl}\', \'{newUrl}\', {page})" style="display: inline-block; margin: 0 7px; ">{page}</a>'.format(funClick=self.funClick, jsonUrl=self.jsonUrl, newUrl=self.newUrl, page=page)
                else:
                    pagestr += '<a class="right" href="{jsonUrl}{page}" style="display: inline-block; margin: 0 7px; ">{page}</a>'.format(jsonUrl=self.jsonUrl, page=page)
        pagestr += "</div>"
        return pagestr
