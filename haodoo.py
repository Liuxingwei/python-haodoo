#!/usr/bin/env python3

import selenium.webdriver
import re
import os
import http.client


def parse_url(url):
    """
    解析url，获取其中的「协议」、「主机名」、「路径」、「查询串」信息
    :param url: url
    :return: component: map {'protocal': protocal, 'host': host, 'path': path, 'query': query}
    """
    pattern = re.compile('^((?P<protocal>http)://)?((?P<host>[^/]*)/?)?((?P<path>[^?^#]*)/?)?(?P<query>\?[^#]*)?')
    match = pattern.search(url)
    protocal = match.group('protocal')
    host = match.group('host')
    path = match.group('path')
    query = match.group('query')

    component = {
        'protocal': protocal or '',
        'host': host or '',
        'path': path or '',
        'query': query or ''
    }
    return component


def get_file_type(path):
    """
    获取文件类型
    :param path:
    :return:
    """
    pattern = re.compile('([^.]*$)')
    match = pattern.search(path)
    return match and match.group(1)


def process(url):
    """
    处理html文件
    :param url:
    :return:
    """
    urlComponent = parse_url(url)
    if urlComponent['host'] and urlComponent['host'] != 'haodoo.net' and urlComponent['host'] != '':
        return
    if urlComponent['path']:
        fileType = get_file_type(urlComponent['path'])
        if 'png' == fileType or 'jpg' == fileType or 'jpeg' == fileType or 'png' == fileType or 'js' == fileType or 'ico' == fileType:
            image_and_js_process(url)
        elif 'css' == fileType:
            css_process(url)
    elif urlComponent['query']:
        "此处处理是不完善的，仅适用于好读网站"
        bookPattern = re.compile('L=book$')
        if bookPattern.search(url):
            book_process(url)
        else:
            html_process(url)
    return


def book_process(url):
    content = save_file(url, 'html')
    pagesPattern = re.compile('var maxChapterID = (.*?);')
    pagesResult = pagesPattern.search(content)
    if pagesResult:
        pages = pagesResult.group(1)
        for page in range(1, int(pages) + 1):
            save_file(re.sub('\:0\&', ':' + str(page) + '&', url), 'html')
    return

def image_and_js_process(url):
    """
    处理图片和js文件
    :param url:
    :return:
    """
    save_file(url)
    return


def path_process(filePath):
    
    return


def save_file(url, filePath=""):
    try:
        body = get_remote_content(url)
        urlComponent = parse_url(url)
        if filePath != "":
            file = open(filePath, 'wb')
            file.write(body)
            file.close()
            return ""
        elif urlComponent['path'] != '':
            filePath = './pages/' + urlComponent['path']
            file = open(filePath, 'wb')
            file.write(body)
            file.close()
        elif urlComponent['query'] != '':
            filePath = './pages/' + urlComponent['query']
            try:
                content = body.decode('utf-8')
                file = open(filePath, 'w')
                file.write(content)
                file.close()
                return content
            except UnicodeDecodeError:
                return content.decode('big5')
                file = open(filePath, 'w')
                file.write(content)
                file.close()
                return content
            else:
                file = open(filePath, 'wb')
                file.write(body)
                file.close()
                return ""
    except RuntimeError:
        return ""


def get_remote_content(url):
    urlComponent= parse_url(url)
    conn = http.client.HTTPConnection(urlComponent['host'])
    conn.request('GET', url)
    response = conn.getresponse()
    content = response.read()
    return content


def css_process(url):
    """
    处理css文件
    :param url:
    :return:
    """
    save_file(url)
    return


def html_process(url):
    """
    处理html文件
    :param url:
    :return:
    """
    urlComponent = parse_url(url);

    content = save_file(url)

    imgs_process(content)
    scripts_process(content)
    icons = get_icons(content)
    icons_process(icons)
    styles_process(content)
    onlinereads_process(content)
    download_process(content)
    links_process(content)

    return


def download_process(content):

    bookPath = './books'
#     content = '''
#
# <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
# <html>
# <head>
#    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
# <title>
# 好讀</title>
# <link rel="shortcut icon" href="image/favicon.ico">
# <script language="javascript" type="text/javascript" src="cookie.js"></script>
#
# <link rel=stylesheet href="styles.css" type="text/css">
#
# <script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.2.3.min.js" type="text/javascript"></script>
# <link href="https://ajax.aspnetcdn.com/ajax/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" />
# <script src="https://ajax.aspnetcdn.com/ajax/bootstrap/3.3.7/bootstrap.min.js"></script>
#
# <script language="javascript" type="text/javascript" src="d.js"></script>
#
# <script type="text/javascript">
# $(document).ready(function(){
# 	$("hr").css({
#        "margin-top": "6",
#        "margin-bottom": "6",
#        "color": "#CCCCCC",
#        "background-color": "#CCCCCC"
#        });
# 	$("a").hover(
#        function(){$(this).css("color", "#E88E00")},
#        function(){$(this).css("color", "#0078F0")}
#        );
# });
# </script>
#
# <script type="text/javascript">
#
#   var _gaq = _gaq || [];
#   _gaq.push(['_setAccount', 'UA-9086653-1']);
#   _gaq.push(['_trackPageview']);
#
#   (function() {
#     var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
#     ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
#     var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
#   })();
#
# </script>
# </head>
#
# <body style="background-color:#0088aa" text="#333333" link="#0078F0" vlink="#005AB4" alink="#FF6600" topmargin="0" leftmargin="0" marginwidth="0" marginheight="0">
# <table style="background-color:#FFFFFF" bgcolor="" border=0 cellspacing=0 cellpadding=0 align=center width="740">
# <tr valign=top>
# <td valign=top>
# <table border=0 cellspacing=0 cellpadding=0 width=560 class="a14">
# <tr>
# <td align=top>
# <table border=0 cellspacing=0 cellpadding=0>
# <tr>
# <td width=110><a href="?M=hd&P=welcome"><img SRC="image/logo-haodoo.png" align=left border="0" alt="好讀首頁"></a></td>
# <td class="a03">
# <a href="?M=hd&P=100">世紀百強</a>　|　<a href="?M=hd&P=wisdom">隨身智囊</a>　|　<a href="?M=hd&P=history">歷史煙雲</a>　|　<a href="?M=hd&P=martial">武俠小說</a>　|　<a href="?M=hd&P=mystery">懸疑小說</a><br>
# <a href="?M=hd&P=romance">言情小說</a>　|　<a href="?M=hd&P=scifi">奇幻小說</a>　|　<a href="?M=hd&P=fiction">小說園地</a>　|　<a href="?M=hd&P=audio">有聲書　</a>　|　<a href="?M=hd&P=letter">更新預告</a>
# </td></tr></table>
# </td></tr>
#
# <tr>
# <td align=top>
# <table border=0 cellspacing=0 cellpadding=0>
# <tr>
#
# <td width="20"></td>
# <td valign=top>
# <table border=0 cellspacing=0 cellpadding=0>
# <tr>
# <td valign=top>
# <span id=t>
# <table border=0 cellspacing=0 cellpadding=0 class="a03" background="images/bgfadegreen.gif" width="510">
# <tr>
# <td><img src="images/subject-mbook.gif" align=left></td>
# <td width=100><font color="CC0000"></font></td>
# </tr></table>
# </span>
# </td></tr>
# <tr><td height=10></td></tr>
# <tr>
# <!--------------------- START INCLUDE FILES --------------------->
# <td>
# <table border=0 cellspacing=0 cellpadding=0 width="530">
# <tr>
# <td>
# <script type="text/javascript">
# SetTitle("金庸【射鵰英雄傳】");
# $c1 = '';
# $c2 = '<a href="?M=hd&P=martial-1">武俠小說 書目</a>';
# $c3 = '<a href="?M=hd&P=100-2">世紀百強</a>';
# SetTopLinks($c1, $c2, $c3);
# </script>
#
# <table BORDER="0" CELLSPACING="0" CELLPADDING="2" WIDTH="100%">
# <tr><td>
# <font color="CC0000">金庸</font>《射鵰英雄傳一》<input type="button" value="線上閱讀" onClick = "ReadOnline('D55a', 'book')";> <a href="?M=hd&P=help-read" target=_blank>說明</a><br><br><input type="button" value="下載 updb 檔" onClick = "DownloadUpdb('D55a')";><font size=2> 2010/10/13 (473K) 2017/8/4</font><br><input type="button" value="下載 prc 檔" onClick = "DownloadPrc('D55a')";><font size=2> 2010/10/13 (503K) 2017/8/4</font><br><input type="button" value="下載直式 mobi 檔" onClick = "DownloadMobi('DV55a')";><font size=2> 2015/6/5 (1371K) 2017/8/4</font><br><input type="button" value="下載 epub 檔" onClick = "DownloadEpub('D55a')";><font size=2> 2010/10/13 (323K) 2017/8/4</font><br><input type="button" value="下載直式 epub 檔" onClick = "DownloadVEpub('DV55a')";><font size=2> 2013/5/10 (324K) 2017/8/4</font><br><br><font color="CC0000">金庸</font>《射鵰英雄傳二》<input type="button" value="線上閱讀" onClick = "ReadOnline('D55b', 'book')";><br><br><input type="button" value="下載 updb 檔" onClick = "DownloadUpdb('D55b')";><font size=2> 2010/8/6 (474K) 2017/8/4</font><br><input type="button" value="下載 prc 檔" onClick = "DownloadPrc('D55b')";><font size=2> 2010/10/13 (501K) 2017/8/4</font><br><input type="button" value="下載直式 mobi 檔" onClick = "DownloadMobi('DV55b')";><font size=2> 2015/6/5 (1364K) 2017/8/4</font><br><input type="button" value="下載 epub 檔" onClick = "DownloadEpub('D55b')";><font size=2> 2010/10/13 (320K) 2017/8/4</font><br><input type="button" value="下載直式 epub 檔" onClick = "DownloadVEpub('DV55b')";><font size=2> 2013/5/10 (321K) 2017/8/4</font><br><br><font color="CC0000">金庸</font>《射鵰英雄傳三》<input type="button" value="線上閱讀" onClick = "ReadOnline('D55c', 'book')";><br><br><input type="button" value="下載 updb 檔" onClick = "DownloadUpdb('D55c')";><font size=2> 2010/10/13 (468K) 2017/8/4</font><br><input type="button" value="下載 prc 檔" onClick = "DownloadPrc('D55c')";><font size=2> 2010/10/13 (499K) 2017/8/4</font><br><input type="button" value="下載直式 mobi 檔" onClick = "DownloadMobi('DV55c')";><font size=2> 2015/6/5 (1359K) 2017/8/4</font><br><input type="button" value="下載 epub 檔" onClick = "DownloadEpub('D55c')";><font size=2> 2010/10/13 (319K) 2017/8/4</font><br><input type="button" value="下載直式 epub 檔" onClick = "DownloadVEpub('DV55c')";><font size=2> 2013/5/10 (320K) 2017/8/4</font><br><br><font color="CC0000">金庸</font>《射鵰英雄傳四》<input type="button" value="線上閱讀" onClick = "ReadOnline('D55d', 'book')";><br><br><input type="button" value="下載 updb 檔" onClick = "DownloadUpdb('D55d')";><font size=2> 2010/8/6 (468K) 2017/8/4</font><br><input type="button" value="下載 prc 檔" onClick = "DownloadPrc('D55d')";><font size=2> 2010/10/13 (500K) 2017/8/4</font><br><input type="button" value="下載直式 mobi 檔" onClick = "DownloadMobi('DV55d')";><font size=2> 2015/6/5 (1367K) 2017/8/4</font><br><input type="button" value="下載 epub 檔" onClick = "DownloadEpub('D55d')";><font size=2> 2010/10/13 (325K) 2017/8/4</font><br><input type="button" value="下載直式 epub 檔" onClick = "DownloadVEpub('DV55d')";><font size=2> 2010/10/13 (325K) 2017/8/4</font><br><br><img src="covers/55.jpg" HSPACE=8 align=right>
# 好讀書櫃【典藏版】。2006年，美格騰參照原書再整理校正過。感謝Stephen Tsang、Anthony、Emil Lee、Jason勘誤。感謝tonyhsie再校正：「參考原書，校正錯字，別字，標點，段落，使其盡量符合原書原貌。」 (2010/12/24)。 感謝Fong、梁景堯勘誤。感謝周府之獬提供掃描檔。感謝敖先榮、章雪曼勘誤。感謝tiknuhc按掃描檔勘誤多處。<br>
# <br>
# 【射鵰英雄傳】名列<a href="?P=100"> 世紀百強 </a>第 29。<br>
# <br>
# 《射鵰英雄傳》是金庸中期武俠小說創作的代表作品，也是金庸擁有讀者最多的作品，它的發表確立了金庸「武林至尊」的地位。這部小說歷史背景突出，場景紛繁，氣勢宏偉，具有鮮明的「英雄史詩」風格；在人物創造與情節安排上，它打破了傳統武俠小說一味傳奇，將人物作為情節附庸的模式，堅持以創造個性化的人物形象為中心，堅持人物統帥故事，按照人物性格的發展需要及其內在可能性、必然性來設置情節，從而使這部說達到了事雖奇人卻真的妙境。本書最初連載於一九五七年─一九五九年的《香港商報》。<br>
# <br>
# 自幼家破人亡的郭靖，隨母流落蒙古大漠，這傻頭傻腦但有情有義的小伙子倒也是有福氣，他不但習得了江南六怪的絕藝、全真教馬鈺的內功、洪七公的降龍十八掌、雙手互博之術、九陰真經等蓋世武功，還讓古靈精怪的小美女黃蓉這輩子跟定了他。這部原名『大漠英雄傳』的小說是金庸小說中最廣為普羅大眾接受、傳頌的一部，其中出了許多有名又奇特的人物，東邪西毒南帝北丐中神通，還有武功靈光、腦袋不靈光的老頑童周伯通，他們有特立獨行的性格、作為和人生觀，讓人嘆為觀止。書中對歷史多有著墨，中原武林及蒙古大漠的生活情形隨著人物的生長環境變遷而有不同的敘述，異族統治之下的小老百姓心情寫來絲絲入扣，本書對情的感覺是很含蓄的，尤其是郭靖與拖雷、華箏無猜的童年之誼，他與江南六怪的師生之誼等等，還有全真七子中長春子丘處機的俠義行為及其與郭楊二人風雪中的一段情誼，也有很豪氣的敘述。神算子瑛姑及一燈大師和周伯通的一場孽戀，是最出乎人意料的一段，成人世界的戀情可比小兒女的青澀戀燕還複雜多了。郭靖以丑勝巧的人生經歷和「為國為民，俠之大者」的儒俠風範，也是書中最大要旨。距離這本書完成的時間已有四十年了，書中的單純誠樸的人物性格還深深的留在讀者心中，本書故事也多改編成電影、電視劇等，受歡迎程度可見一斑。<br>
# <br>
# <font size=2>
# <a href="?M=hd&P=pr">勘誤表</a>：<br>
# (射鵰英雄傳三 章雪曼 2015/10/2)<br>
# 靖蓉三人/靖蓉二人<br>
# 無可柰何/無可奈何<br>
# <br>
# (射鵰英雄傳二 mPDB 2015/6/5)<br>
# 掌法尚末完全/掌法尚未完全<br>
# 媒約之言/媒妁之言<br>
# 青蛇蜿蜓東去/青蛇蜿蜒東去<br>
# 幾上桌上/几上桌上<br>
# 笑顏逐開/笑逐顏開<br>
# 說到：﹁黃/說道：﹁黃<br>
# 憑你差遺/憑你差遣<br>
# <br>
# (射鵰英雄傳三 mPDB 2015/6/5)<br>
# 每顆樹/每棵樹<br>
# 傾刻間/頃刻間<br>
# 窒滯，，這兩/窒滯，這兩<br>
# 一包藥紛/一包藥粉<br>
# 空中矯矢飛至/空中矯夭飛至<br>
# 頂上蹤躍過去/頂上縱躍過去<br>
# 淵停嶽峙/淵渟嶽峙<br>
# <br>
# (射鵰英雄傳四 mPDB 2015/6/5)<br>
# 茅蘆三顧/茅廬三顧<br>
# 屍駭/屍骸<br>
# 軍中寂莫/軍中寂寞<br>
# 亞德裡亞/亞德里亞<br>
# 不裡/不里<br>
# 庫裡爾台/庫里爾台<br>
# <br>
# (射鵰英雄傳一 mPDB 2014/12/5)<br>
# 縮身在岸石之後/縮身在崖石之後<br>
# <br>
# (射鵰英雄傳一 敖先榮 2014/12/5)<br>
# 另有一般/另有一股 <font color=#0066CC>(依原書未改。一般：一番、一種。劉知遠諸宮調˙第一：「只有一般憑不得，南山依舊與雲齊。」)</font><br>
# 你推我擁/你推我擠 <font color=#0066CC>(依原書未改)</font><br>
# 骨都骨都/骨嘟骨嘟<br>
# 全金發部已/全金發都已<br>
# 一般好處/一股好處 <font color=#0066CC>(依原書未改)</font><br>
# 雅擅點穴/精擅點穴 <font color=#0066CC>(依原書未改。雅：表示程度很甚，相當於「很」、「極」。 )</font><br>
# 我在岸頂/我在崖頂 (閱文即知)<br>
# 望著岸頂/望著崖頂<br>
# <br>
# (射鵰英雄傳一 梁景堯 2014/1/3)<br>
# 白彫落單/白鵰落單<br>
# 雙額紅暈/雙頰紅暈<br>
# <br>
# (射鵰英雄傳二 梁景堯 2014/1/3)<br>
# 清展/清晨<br>
# 嬌痴無那/嬌痴無邪<br>
# <br>
# (射鵰英雄傳三 梁景堯 2014/1/3)<br>
# 發上插著/髮上插著<br>
# 戳死，了他/戳死了他<br>
# 我知道石盒/我只道石盒<br>
# 長春門下」。/長春門下。」<br>
# 媒約之言/媒妁之言<br>
# 腰里長劍/腰裏長劍<br>
# <br>
# (射鵰英雄傳四 梁景堯 2014/1/3)<br>
# 解明瞭第二道/解明了第二道<br>
# 漸漸頃側/漸漸傾側<br>
# 欄幹上一按/欄干上一按<br>
# 輕輕佻開/輕輕挑開<br>
# 梁唐晉漢週五代/梁唐晉漢周五代<br>
# 回身檢起/回身撿起<br>
# 諸後之中/諸后之中<br>
# 鹼海/鹹海<br>
# 朮赤的赤子/朮赤的次子<br>
# 國王享利二世/國王亨利二世<br>
# 範文虎/范文虎<br>
# 黃白朮/黃白術<br>
# 眉發儼然/眉髮儼然<br>
# <br>
# (射鵰英雄傳一 Fong 2013/5/10)<br>
# 修正參考：金庸作品集5，射鵰英雄傳一，遠流，三版十二刷<br>
# 那馬蹄到臨近/那馬踱到近<br>
# 勿予怪貴/勿予怪責<br>
# 得是了/便是了<br>
# 踢她下岸/踢她下崖<br>
# 考較比老哥/考較你老哥<br>
# 那個童/那小童<br>
# <br>
# (射鵰英雄傳二 Fong 2013/5/10)<br>
# 修正參考：金庸作品集6，射鵰英雄傳二，遠流，三版十二刷<br>
# 樑子翁/梁子翁 (有兩處)<br>
# 爹參/爹爹<br>
# 左拳鬥出/左拳斗出<br>
# 好人了了/好人了<br>
# 踢鬥/踢斗<br>
# 郭靖也得著尋找/郭靖也幫著尋找<br>
# 被頭鋪蓋/被頭舖蓋<br>
# 只所得/只聽得<br>
# 爭賠個不是/賠個不是<br>
# 一題心/一顆心<br>
# 因禁/囚禁<br>
# 老頑竟/老頑童<br>
# 就魚/鯊魚<br>
# 劃近去/划近去<br>
# <br>
# (射鵰英雄傳三 Fong 2013/5/10)<br>
# 修正參考：金庸作品集7，射鵰英雄傳三，遠流，三版十二刷<br>
# 截死/戳死<br>
# 室滯/窒滯<br>
# <br>
# (射鵰英雄傳四 Fong 2013/5/10)<br>
# 修正參考：金庸作品集8，射鵰英雄傳三，遠流，三版十二刷<br>
# 這在這/就在這<br>
# 彆扭我/別扭我<br>
# 農領/衣領<br>
# 斡兒朵的正後/斡兒朵的正后<br>
# 斡兒朵的次後/斡兒朵的次后<br>
# 斡兒朵的三後/斡兒朵的三后<br>
# 正後是金國的公主/正后是金國的公主<br>
# 卜佔/卜占<br>
# 偉之之上/偉人之上<br>
# 一仗就摧/一仗就摧毀了回教的大本營。<br>
# <br>
# (Ian Wang 2010/8/6)<br>
# 王(左吉右吉)/王&#21894;<br>
# (三個吉)/&#22174;<br>
# 金源(左王右壽)/金源&#29881;<br>
# 免肉/兔肉 (Jason 2010/8/6)<br>
# <br>
# (Emil Lee 2010/7/22)<br>
# 郭請與黃蓉/郭靖與黃蓉<br>
# <br>
# (Emil Lee 2010/6/16)<br>
# 鐵水真/鐵木真<br>
# <br>
# (Anthony 2010/4/30)<br>
# 原來來聰右手/原來朱聰右手<br>
# <br>
# (Stephen Tsang 2009/8/7)<br>
# 正是桃花島主東邪藥師/正是桃花島主東邪黃藥師<br>
# 功勢有如驚風駭浪/攻勢有如驚風駭浪<br>
# 黃藥師拿捏不住/黃蓉拿捏不住<br>
# 黃兒的婚事/蓉兒的婚事<br>
# 在青龍漢旁/在青龍灘旁<br>
# 喜興鐵槍廟/嘉興鐵槍廟<br>
# <br>
# (Stephen Tsang 2009/8/6)<br>
# 一等他峰/一等他下峰<br>
# 能愈諸患/能癒諸患<br>
# 郭靖才知別來餘/郭靖才知別來年餘<br>
# 將金兵打潰不成軍。/將金兵打得潰不成軍<br>
# 來頭夾腦/夾頭夾腦<br>
# 逐漸達去/逐漸遠去<br>
# 邊於天下/遍於天下<br>
# 當下將魯有腳靖到帳中/當下將魯有腳請到帳中<br>
# 忽吞忽口/忽吞忽吐<br>
# 常真沒/當真沒<br>
# 倘說是並無死意/倘說是並無惡意<br>
# 柯鎮惡不通 文黑/柯鎮惡不通文墨<br>
# 終能一殲滅/終能一舉殲滅<br>
# 路著咚咚咚咚/跟著咚咚咚咚<br>
# 只怕他難以腳身/只怕他難以脫身<br>
# 火星四錢/ 火星四濺<br>
# 得知真教要來/得知全真教要來<br>
# 丘處機掌真是/丘處機當真是<br>
# 那幾個丈道勸你/那幾個道長勸你<br>
# 全真五盡皆大驚/全真五子盡皆大驚<br>
# 兩造詳加詢問/兩邊詳加詢問<br>
# 半個﹃床﹄字加/半個﹃&#29248;﹄字加<br>
# 其是得意/甚是得意<br>
# 想來是老父爺/想來是老天爺<br>
# 相起一燈大師／想起一燈大師<br>
# 湖上幾尋/湖上幾年<br>
# 壯志不售/壯志不酬<br>
# 江水在三年身邊奔騰而過/江水在三人身邊奔騰而過<br>
# 買了三雙雞/買了三隻雞<br>
# 今身是八月初幾？/今兒是八月初幾？<br>
# 漢臉笑容/滿臉笑容<br>
# 此時功力進/此時功力猛進<br>
# <br>
# (Stephen Tsang 2009/7/25)<br>
# 只聽得敵車中/只聽得敵陣中<br>
# 晝停夜宿/晝行夜宿<br>
# 他連人帶，縱躍而至/他連人帶椅，縱躍而至<br>
# <br>
# (Stephen Tsang 2009/7/23)<br>
# 偷眼相顏烈瞧去/偷眼向顏烈瞧去<br>
# 喝道分出勝負/喝到分出勝負<br>
# 不由自由/不由自主<br>
# 柯惡鎮/柯鎮惡<br>
# <br>
# (Stephen Tsang 2009/7/21)<br>
# 另外一名武功腰間/另外一名武官腰間<br>
# 為義兄報全後代/為義兄保存後代<br>
# </font>
# </td></tr></table><br>
# </td>
# <td width="20"></td>
# </tr></table>
# </td></tr>
#
# <tr>
# <td>
# <table border=0 cellspacing=0 cellpadding=0 COLS=4 WIDTH="100%" background="images/d_background.gif">
# <tr class="a90" height=24>
# <td width="25%" align="center"><a href="?M=hd&P=welcome">好讀首頁</a></td>
# <td width="25%" align="center"><a href="?M=hd&P=about">有關好讀</a></td>
# <td width="25%" align="center"><a href="?M=hd&P=newcomer">讀友需知</a></td>
# <td width="25%" align="center"><a href="?M=mail&P=contact">聯絡好讀</a>
# </td></tr></table>
# <br>
# </td></tr></table>
# </td></tr></table>
# </td></tr></table>
# <td width=180 valign=top>
# <table border=0 cellspacing=0 cellpadding=0 WIDTH="160">
#
# <tr><td height=10></td></tr>
# <tr><td><font color="CC3300" size=2>搜尋好讀</font></td></tr>
# <!-- SiteSearch Google -->
# <form action="http://www.google.com/cse" id="cse-search-box" target="_blank">
# <tr><td>
# <input type="hidden" name="cx" value="partner-pub-4729470741573892:vcr86ky33h9" />
# <input type="hidden" name="ie" value="UTF-8" />
# <input type="text" name="q" size="10" />
# <input type="submit" name="sa" value="搜尋" />
# </td></tr></form>
# <!-- SiteSearch Google -->
#
# <tr>
# <td valign=top width="160">
# <table border=0 cellspacing=0 cellpadding=0 class="a03">
# <tr><td height=10></td></tr>
# <tr><td>
# <font color="CC0000">好讀第17年了</font>。<br>
# 有好讀真好，有你也真好。但不知遍及各地的你，究竟有多少。若你從未或很久沒贊助過好讀，<a href="?M=hd&P=donate">請按這裡</a>，贊助好讀美金或人民幣十元，讓我知道你存在。<br>
# <br>
# <font color="CC0000">11/25香港 Dennis C</font><br>
# 幾年前由朋友介紹得悉好讀，多年來在旅途中它都帶給我很多樂趣。香港地方狹小，不少書都因地方問題而送人或丟棄，好讀卻帶給了我很多閲讀的方便、亦節省了儲存的位置。衷心多謝各位工作仝人！<br>
# <br>
# <font color="CC0000">11/19 美國紐約 June</font><br>
# 發現好讀幾年了，但現在才發現這好讀留言板。抱歉呢，理應更早道謝。身在海外，要看一本中文書不是易事。書店售書種類少，價錢高；圖書館借書種類更少。幸好發現好讀網，可以一解書癮。衷心感謝所有有心人上載和校對。<br>
# <br>
# <font color="CC0000">11/17 大陸 Shirley</font><br>
# 偶然發現好讀網這塊寶地真的很驚訝，網絡上有這樣安靜舒適的地方可以閱讀電子書，對我這種資金短缺的學生真的很意外很開心！<br>
# <br>
# <font color="CC0000">11/16 香港 chair chun wai</font><br>
# 因為買了Kindle的緣故，所以才發現"好讀"這個地方。感謝"好讀"一直的更新和提供書本給大家。感謝感謝<br>
# <br>
# <font color="CC0000">11/15 香港 mike chan</font><br>
# 我認識好讀是因爲kindle。那時中學買了kindle，需要找找電子書，因此在網上發現了好讀。對於繁體字kindle用家，這是個大福音！<br>
# <br>
# <font color="CC0000">11/13 大陸 BerthaR</font><br>
# 今天因為Kindle的緣故找書，才發現好讀這個地方。感覺是一方淨土，公益地為書友們獲取知識省下了不少財力，節省了大家的時間：）目前我只是個高中生，提供的也只有十塊錢而已啦。十七年的好讀真是令人敬佩！希望你們知道我的感謝，還有知道更多人的感謝！<br>
# <br>
# <font color="CC0000">11/9 香港 MJ</font><br>
# 從小喜愛看書，看書人也許都知道要管理保存書本是不容易的（尤其香港的地方空間更有限）。今年開始嘗試電子書，看看能否接受。因為好讀網的海量書本，小弟所喜愛的黃易＋衛斯理，還有準備開始看的金庸也不用愁了。感謝好讀！<br>
# <br>
# >> <a href="?M=hd&P=letters">更多</a><br>
# <br>
# </td></tr></table>
# </td></tr></table>
# </td></tr></table>
# </body>
# </html>
#
# '''
    downloadLinkPattern = re.compile('(onClick\w*=\w*"Download)', re.IGNORECASE)
    downloadLinkMatch = downloadLinkPattern.search(content)
    if not downloadLinkMatch:
        return

    includeFilesPattern = re.compile('\<\!--------------------- START INCLUDE FILES ---------------------\>(.*?)\<\!-- SiteSearch Google --\>', re.DOTALL)
    includeFilesMatch = includeFilesPattern.findall(content)
    if not includeFilesMatch:
        return
    includeFileString = includeFilesMatch[0]

    categoryPattern = re.compile('\&lt;a\W*href="\?M=hd.*?"\&gt;(.*?)&lt;', re.IGNORECASE)
    categoryMatch = categoryPattern.findall(includeFileString)
    category = re.sub(' .*', '', categoryMatch[0])

    bookPath += '/' + category
    if not os.path.exists(bookPath):
        os.mkdir(bookPath)

    titlePattern = re.compile('SetTitle\("(.*?)"\)')
    titleMatch = titlePattern.findall(includeFileString)
    title = titleMatch[0]
    bookPath += '/' + title
    if not os.path.exists(bookPath):
        os.mkdir(bookPath)
    fileList = re.split('<font color="CC0000">', includeFileString, flags=re.DOTALL)
    for i in range(1, len(fileList)):
        fileString = fileList[i]
        fileTitlePattern = re.compile('^.*?</font>(.*?)<input')
        fileTitleMatch = fileTitlePattern.findall(fileString)
        fileTitle = fileTitleMatch[0]
        if len(fileList) > 1:
            filePath = bookPath + '/' + fileTitle
        else:
            filePath = bookPath
        if not os.path.exists(filePath):
            os.mkdir(filePath)
        downloadsPattern = re.compile('"(Download.*?)"', re.IGNORECASE)
        downloadsMatch = downloadsPattern.findall(fileString)
        for download in downloadsMatch:
            downloadInfoPattern = re.compile('Download(.*?)\(\'(.*)\'\)', re.IGNORECASE)
            downloadInfoMatch = downloadInfoPattern.search(download)
            downloadFileName = downloadInfoMatch.group(2) + '.' + downloadInfoMatch.group(1).lower()
            downloadLink = 'http://haodoo.net/?M=d&P=' + downloadFileName
            downloadFilePath = filePath + '/' + downloadFileName
            save_file(downloadLink, downloadFilePath)
        continue
    return


def links_process(content):
    links = get_links(content)
    if links:
        for link in links:
            process(link.get_attribute('href'))


def onlinereads_process(content):
    onlinereads = get_onlinereads(content)
    if onlinereads:
        for onlineread in onlinereads:
            bookInfoPattern = re.compile("'(.*?)'")
            bookInfoString = onlineread.get_attribute('onClick')
            bookInfo = bookInfoPattern.findall(bookInfoString)
            onlinereadAddress = 'http://haodoo.net/?M=u&P=' + bookInfo[0] + ':0&L=' + bookInfo[1]
            process(onlinereadAddress)


def styles_process(content):
    styles = get_styles(content)
    if styles:
        for style in styles:
            process(style.get_attribute('href'))


def icons_process(icons):
    if icons:
        for icon in icons:
            process(icon.get_attribute('href'))


def scripts_process(content):
    scripts = get_scripts(content)
    if scripts:
        for script in scripts:
            process(script.get_attribute('src'))


def imgs_process(content):
    imgs = get_imgs(content)
    if imgs:
        for img in imgs:
            process(img.get_attribute('src'))


def get_links(content):
    return chrome.find_elements_by_xpath("//a[@href]")


def get_onlinereads(content):
    return chrome.find_elements_by_xpath("//input[@value='線上閱讀']")


def get_styles(content):
    return chrome.find_elements_by_xpath("//link[@rel='stylesheet']")


def get_icons(content):
    return chrome.find_elements_by_xpath("//link[@rel='shortcut icon']")


def get_scripts(content):
    return chrome.find_elements_by_xpath("//script[@src]")


def get_imgs(content):
    imgs = chrome.find_elements_by_css_selector('img')
    return imgs


def get_content(url):
    chrome.get(url)
    content = chrome.page_source
    return content


opts = selenium.webdriver.ChromeOptions()

# opts.headless = True

chrome = selenium.webdriver.Chrome(options = opts)

url = 'http://haodoo.net/?M=hd&P=welcome'

process(url)

chrome.close()
