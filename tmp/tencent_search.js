define("assets/js/app/page/search", ["../util/molo", "../util/jqueryPagination", "../common/animate", "../common/searchScrollAjaxLoadLitPage", "../util/doT", "../util/loadImage", "../common/AutoResizeImage", "../common/safeTipHover", "../common/searchAssociate", "../common/webBehaviour"], function (a) {
    a("../util/molo");
    a("../util/jqueryPagination");
    var b = a("../common/animate"),
        c = a("../common/searchScrollAjaxLoadLitPage"),
        d = a("../common/searchAssociate"),
        e = new c,
        f = a("../common/webBehaviour");
    $(document).ready(function () {
        var a = new f;
        a.init(), a.apkPostNew({});
        var c = new d;
        c.init();
        new b({
            rt: "#return",
            bottom: 60,
            time: 500
        });
        e.init()
    })
}), define("assets/js/app/util/molo", [], function (a, b, c) {
    function d(a) {
        g && alert(a)
    }
    $.ML = $.ML || {
            version: "v1.0.0"
        }, $.extend($.ML, {
            gConst: {
                urlPre: MOLO.urlPre,
                bodyMinWidth: 950,
                bodyMaxWidth: 1170,
                invalidImgSrcArr: ["10.148.144.180"]
            },
            gMsg: {},
            util: {
                CurentTime: function () {
                    var a = new Date,
                        b = a.getFullYear(),
                        c = a.getMonth() + 1,
                        d = a.getDate(),
                        e = a.getHours(),
                        f = a.getMinutes(),
                        g = b + "-";
                    return 10 > c && (g += "0"), g += c + "-", 10 > d && (g += "0"), g += d + " ", 10 > e && (g += "0"), g += e + ":", 10 > f && (g += "0"), g += f
                },
                isIE6: function () {
                    return window.ActiveXObject && !window.XMLHttpRequest ? !0 : !1
                },
                getSearchArray: function () {
                    var a = window.location.search.substring(1).split("&");
                    return a
                },
                getSearchByName: function (a) {
                    for (var b, c, d = $.ML.util.getSearchArray(), e = 0; e < d.length; e++) b = d[e].split("=")[0], b == a && (c = d[e].split("=")[1]);
                    return c
                },
                getCookie: function (a) {
                    for (var b = document.cookie.split("; "), c = 0, d = b.length; d > c; c++) {
                        var e = b[c].split("=");
                        if (e[0] == a) return decodeURIComponent(e[1])
                    }
                }
            }
        }),
        function () {
            try {
                var a = navigator.userAgent.toLowerCase(),
                    b = null,
                    c = 0;
                if (b = a.match(/msie ([\d.]+)/), c = b ? parseInt(b[1], 10) : 0, 6 == c) try {
                    document.execCommand("BackgroundImageCache", !1, !0)
                } catch (d) {}
            } catch (d) {}
        }();
    var e = function () {
            return window.addEventListener ? function (a, b, c, d) {
                a.addEventListener(b, c, d)
            } : function (a, b, c) {
                a.attachEvent("on" + b, c)
            }
        }(),
        f = function () {
            return window.addEventListener ? function (a, b, c, d) {
                a.removeEventListener(b, c, d)
            } : function (a, b, c) {
                a.detachEvent("on" + b, c)
            }
        }();
    window.printLog = function (a) {
        try {
            console.log(a)
        } catch (b) {}
    };
    var g = !0;
    $("#J_Log")[0] && $("#J_Log").on("click", function () {}), $(document).on("mouseover", "a", function () {
        $(this).attr("hidefocus", !0)
    }), c.exports = {
        addEvent: e,
        removeEvent: f,
        eTrace: d
    }
}), define("assets/js/app/util/jqueryPagination", [], function () {
    jQuery.fn.pagination = function (a, b) {
        return b = jQuery.extend({
            page_size: null,
            items_per_page: 10,
            num_display_entries: 10,
            current_page: 0,
            num_edge_entries: 0,
            link_to: "#",
            prev_text: "&lt;",
            next_text: "&gt;",
            ellipse_text: "...",
            prev_show_always: !0,
            next_show_always: !0,
            isJump: !1,
            callback_run: !0,
            islast_num_show: !0,
            callback: function () {
                return !1
            }
        }, b || {}), this.each(function () {
            function c() {
                return null !== b.page_size ? b.page_size : Math.ceil(a / b.items_per_page)
            }

            function d() {
                var a = Math.ceil(b.num_display_entries / 2),
                    d = c(),
                    e = d - b.num_display_entries,
                    f = g > a ? Math.max(Math.min(g - a, e), 0) : 0,
                    h = g > a ? Math.min(g + a, d) : Math.min(b.num_display_entries, d);
                return [f, h]
            }

            function e(a, c) {
                g = a, f();
                var d = b.callback(a, h);
                return d || (c.stopPropagation ? c.stopPropagation() : c.cancelBubble = !0), d
            }

            function f() {
                h.empty();
                var a = d(),
                    f = c(),
                    i = function (a) {
                        return function (c) {
                            return b.isJump ? void 0 : e(a, c)
                        }
                    },
                    j = function (a, c) {
                        if (a = 0 > a ? 0 : f > a ? a : f - 1, c = jQuery.extend({
                                text: a + 1,
                                classes: ""
                            }, c || {}), a == g) var d = jQuery("<span class='current'>" + c.text + "</span>");
                        else var d = jQuery("<a>" + c.text + "</a>").bind("click", i(a)).attr("href", b.link_to.replace(/__id__/, a));
                        c.classes && d.addClass(c.classes), h.append(d)
                    };
                if (b.prev_text && (g > 0 || b.prev_show_always) && j(g - 1, {
                        text: b.prev_text,
                        classes: "prev"
                    }), a[0] > 0 && b.num_edge_entries > 0) {
                    for (var k = Math.min(b.num_edge_entries, a[0]), l = 0; k > l; l++) j(l);
                    b.num_edge_entries < a[0] && b.ellipse_text && jQuery('<span class="ellipse">' + b.ellipse_text + "</span>").appendTo(h)
                }
                for (var l = a[0]; l < a[1]; l++) j(l);
                if (a[1] < f && b.num_edge_entries > 0)
                    if (b.islast_num_show) {
                        f - b.num_edge_entries > a[1] && b.ellipse_text && jQuery('<span class="ellipse" >' + b.ellipse_text + "</span>").appendTo(h);
                        for (var m = Math.max(f - b.num_edge_entries, a[1]), l = m; f > l; l++) j(l)
                    } else f > a[1] && b.ellipse_text && jQuery('<span class="ellipse" >' + b.ellipse_text + "</span>").appendTo(h);
                b.next_text && (f - 1 > g || b.next_show_always) && (j(g + 1, {
                    text: b.next_text,
                    classes: "next"
                }), h.parent().hasClass("page-box"))
            }
            var g = b.current_page;
            a = !a || 0 > a ? 1 : a, b.items_per_page = !b.items_per_page || b.items_per_page < 0 ? 1 : b.items_per_page;
            var h = jQuery(this);
            this.selectPage = function (a) {
                e(a)
            }, this.prevPage = function () {
                return g > 0 ? (e(g - 1), !0) : !1
            }, this.nextPage = function () {
                return g < c() - 1 ? (e(g + 1), !0) : !1
            }, f(), b.callback_run && b.callback(g, this), 1 == c() && jQuery(".pagin").css("display", "none"), c() > 1 && jQuery(".pagin").css("display", "")
        })
    }
}), define("assets/js/app/common/animate", [], function (a, b, c) {
    function d(a) {
        e = a.rt, f = a.bottom, g = a.time, $(e + " a").click(function () {
            return h ? !1 : (h = !0, $("html,body").animate({
                scrollTop: 0
            }, g, "easeOutExpo", function () {
                h = !1
            }), !1)
        });
        var b = $(window).height();
        $.browser.msie && "6.0" == $.browser.version && $(window).scroll(function () {
            var a = $(window).scrollTop();
            $(e).css({
                top: a + b - $(e).height() - f + "px"
            })
        }), $(window).scroll(function () {
            var a = $(window).scrollTop();
            $(e).css(a > 0 ? {
                display: "block"
            } : {
                display: "none"
            })
        })
    }
    jQuery.extend(jQuery.easing, {
        easeOutExpo: function (a, b, c, d, e) {
            return b == e ? c + d : d * (-Math.pow(2, -10 * b / e) + 1) + c
        }
    });
    var e, f, g, h = !1;
    c.exports = d
}), define("assets/js/app/common/searchScrollAjaxLoadLitPage", ["assets/js/app/util/molo", "assets/js/app/util/doT", "assets/js/app/util/loadImage", "assets/js/app/common/AutoResizeImage", "assets/js/app/common/safeTipHover"], function (a, b, c) {
    var d = (a("assets/js/app/util/molo"), a("assets/js/app/util/doT")),
        e = a("assets/js/app/util/loadImage"),
        f = a("assets/js/app/common/AutoResizeImage"),
        g = a("assets/js/app/common/safeTipHover"),
        h = new g,
        i = function () {
            this.opts = {}, this.conf = function () {
                var a = {
                        ajaxUrl: "searchAjax.htm",
                        listBox: "#J_SearchDefaultListBox",
                        searchNoneBox: ".search-none-img-box",
                        loadMoreBox: ".load-more",
                        containerBox: ".search-default-container"
                    },
                    b = $.extend(!0, a, this.opts);
                return b
            }
        };
    i.prototype.scrollSwitch = !0, i.prototype.nextPageKey = "", i.prototype.searchId = "", i.prototype.keyWord = $.ML.util.getSearchByName("kw"), i.prototype.loadCount = 0, i.prototype.loadAppList = function (a) {
        var b = this,
            c = b.conf();
        $(".load-more-btn").hide(), $.ajax({
            url: c.ajaxUrl + "?kw=" + b.keyWord + "&pns=" + b.nextPageKey + "&sid=" + b.searchId,
            type: "post",
            timeout: 8e3,
            cache: !1,
            dataType: "json",
            success: function (e) {
                var f = e.obj;
                if (null == f) return void(b.scrollSwitch = !0);
                if (a) {
                    if (f.appDetails && 0 == f.appDetails.length) return void a(!1);
                    a(!0)
                }
                b.loadCount++, b.searchId = f.searchId;
                var g = d.template($("#J_SearchAjaxListTmpl").html()),
                    i = g(f.appDetails);
                $(c.listBox).append(i), h.init(), l.init(), $(".load-more-btn").show(), $(".com-footer").show(), 1 == f.hasNext ? (b.scrollSwitch = !0, b.nextPageKey = f.pageNumberStack) : (b.scrollSwitch = !1, $(".load-more-btn").html("没有更多了"), $(".loading").hide(), $(".load-more-btn").unbind("click"))
            },
            error: function () {}
        })
    }, i.prototype.scrollLoad = function () {
        var a = this;
        if (a.scrollSwitch && a.loadCount < 5) {
            var b = $(".load-more-btn a").offset().top,
                c = $(window).scrollTop(),
                d = $(window).height();
            0 > b - c - d && ($(".com-footer").hide(), $(".load-more-btn").hide(), a.scrollSwitch = !1, a.loadAppList())
        }
    }, i.prototype.init = function () {
        var a = this,
            b = a.conf();
        a.loadAppList(function (c) {
            if ($(".load-more-btn").show(), c) $(b.containerBox).css("height", "auto");
            else if (a.scrollSwitch = !1, $(b.searchNoneBox).show(), $(b.loadMoreBox).hide(), $(".load-more-btn").html("没有更多了"), $(".loading").hide(), $(".load-more-btn").unbind("click"), $(b.containerBox).css("height", "500px"), $(".search-none-img-box").length > 0) {
                var d = 3,
                    e = setInterval(function () {
                        return d--, 0 == d ? (clearInterval(e), void(window.location.href = "../myapp/#")) : void $("#lastSec").html(d)
                    }, 1e3);
                return
            }
        }), setTimeout(function () {
            $(window).scroll(function () {
                a.scrollLoad()
            })
        }, 600), $(".load-more-btn").on("click", function () {
            a.loadAppList()
        })
    };
    var j = function () {
            this.options = {}, this.conf = function () {
                var a = this,
                    b = {
                        ImgsContainerClass: ".T_TurnImgBox",
                        ImgsHiddenBoxClass: ".T_TurnImgHiddenBox",
                        ImgsWidthBoxClass: ".T_TurnImgWidthBox",
                        ImgsTurnBtnBoxClass: ".T_TurnImgBtnBox",
                        ImgsTurnLeftBtnClass: ".T_TurnImgTurnLeft",
                        ImgsTurnRightBtnClass: ".T_TurnImgTurnRight",
                        HoverTipClass: "T_TipHoverBox",
                        pageSize: 2
                    },
                    c = $.extend(!0, b, a.options);
                return c
            }
        },
        k = !0;
    j.prototype.init = function () {
        var a = this,
            b = a.conf();
        $(b.ImgsContainerClass).on("mouseenter", function () {
            a.getTurnSwitch($(this)) && a.showTurnBtn($(this))
        }).on("mouseleave", function () {
            a.hideTurnBtn($(this))
        }).each(function (b, c) {
            "undefined" == typeof $(c).data("isload-img") && ($(c).data("isload-img", "1"), a.loadAppImg($(c), this))
        }), $(b.ImgsWidthBoxClass).data("pageindex", 0)
    }, j.prototype.showTurnBtn = function (a) {
        var b = this,
            c = b.conf(),
            d = a.find(c.ImgsTurnLeftBtnClass),
            e = a.find(c.ImgsTurnRightBtnClass);
        d.stop(!0, !0).animate({
            left: 0
        }), e.stop(!0, !0).animate({
            right: 0
        })
    }, j.prototype.hideTurnBtn = function (a) {
        var b = this,
            c = b.conf(),
            d = a.find(c.ImgsTurnLeftBtnClass),
            e = a.find(c.ImgsTurnRightBtnClass);
        d.stop(!0, !0).animate({
            left: 0 - d.width()
        }, "fast"), e.stop(!0, !0).animate({
            right: 0 - e.width()
        }, "fast")
    }, j.prototype.loadAppImg = function (a, b) {
        {
            var c = this,
                d = c.conf(),
                g = a.find(d.ImgsHiddenBoxClass),
                h = a.find(d.ImgsWidthBoxClass),
                i = a.find(".T_TurnImgAllLoading");
            h.find("li").length
        }
        $(b).find(d.ImgsTurnLeftBtnClass).on("click", function () {
            return k ? (k = !1, c.turnLeft(g, h), !1) : void 0
        }), $(b).find(d.ImgsTurnRightBtnClass).on("click", function () {
            return k ? (k = !1, c.turnRight(g, h), !1) : void 0
        }), $(b).find(".T_TurnImgCell:eq(0)").each(function () {
            var b = $(this);
            b.prepend("<img src='" + b.data("imgsrc") + "'/>");
            var d = $(this).find("img"),
                j = d.next(),
                k = d[0],
                l = d.closest("li");
            b.data("isload", "1"), e.detLoadImg(k.src, function () {
                if (1 == a.data("iscount")) j.css("display", "none");
                else {
                    var b, e, m = k.width,
                        n = k.height,
                        o = m > n;
                    if (a.find(".T_TurnImgEveryLoading:gt(0)").css("display", "block"), o ? (f(240, 200, k), b = d.width(), e = d.height(), h.find(".protect-img-box").css("margin-bottom", "5px"), g.width(b).height(2 * e + 5).find(".T_TurnImgCell").width(b).height(e), a.width(b).height(2 * e + 5), h.find("li").width(b + 5)) : (f(200, 300, k), b = d.width(), e = d.height(), g.width(2 * b + 5).height(e).find(".T_TurnImgCell").width(b).height(e), a.width(2 * b + 5).height(e), a.find("li").width(2 * b + 10).height(e)), c.getTurnSwitch(a) && 0 == a.data("iscount")) {
                        var p = h.find("li:first"),
                            q = h.find("li:last");
                        p.before(q), h.css("margin-left", 0 - q.width() + "px")
                    }
                    a.data("iscount", "1"), i.css("display", "none"), c.loadImage(l)
                }
            })
        })
    }, j.prototype.switchTurnBtn = function (a, b) {
        var c = this,
            d = c.conf(),
            e = b.data("imgsize"),
            f = Math.ceil(e / d.pageSize),
            g = b.data("pageindex");
        0 == g ? (a.parent().find(d.ImgsTurnLeftBtnClass)[0].style.display = "none", a.parent().find(d.ImgsTurnRightBtnClass)[0].style.display = "block") : g > 0 && f - 1 > g ? (a.parent().find(d.ImgsTurnLeftBtnClass)[0].style.display = "block", a.parent().find(d.ImgsTurnRightBtnClass)[0].style.display = "block") : g == f - 1 && (a.parent().find(d.ImgsTurnLeftBtnClass)[0].style.display = "block", a.parent().find(d.ImgsTurnRightBtnClass)[0].style.display = "none")
    }, j.prototype.turnLeft = function (a, b) {
        var c = this,
            d = (c.conf(), b.find("li:first")),
            e = b.find("li:last");
        d.before(e), b.css("margin-left", parseInt(b.css("margin-left")) - e.width() + "px");
        var f = parseInt(b.css("margin-left"));
        b.animate({
            marginLeft: f + parseInt(a.width()) + 5 + "px"
        }, function () {
            k = !0
        }), c.loadImage(b.find("li:eq(1)"));
        var g = b.data("pageindex");
        b.data("pageindex", g - 1), c.switchTurnBtn(a, b)
    }, j.prototype.turnRight = function (a, b) {
        var c = this,
            d = (c.conf(), b.find("li:first")),
            e = b.find("li:last");
        e.after(d), b.css("margin-left", "0px");
        var f = parseInt(b.css("margin-left"));
        b.animate({
            marginLeft: f - parseInt(a.width()) - 5 + "px"
        }, function () {
            k = !0
        }), c.loadImage(b.find("li:eq(1)"));
        var g = b.data("pageindex");
        b.data("pageindex", g + 1), c.switchTurnBtn(a, b)
    }, j.prototype.loadImage = function (a) {
        a.find(".T_TurnImgCell").each(function () {
            var a = $(this);
            if ("0" == $(this).data("isload")) {
                a.data("isload", "1"), a.prepend("<img src='" + a.data("imgsrc") + "'/>"); {
                    var b = $(this).find("img"),
                        c = b.next(),
                        d = b[0];
                    b.closest("li")
                }
                e.detLoadImg(d.src, function () {
                    b.css({
                        width: "100%",
                        height: "100%"
                    }), c.css("display", "none")
                })
            }
        })
    }, j.prototype.getTurnSwitch = function (a) {
        return a.find("li").length >= 2 ? !0 : !1
    };
    var l = new j;
    c.exports = i
}), define("assets/js/app/util/doT", [], function (a, b, c) {
    ! function () {
        "use strict";

        function a() {
            var a = {
                    "&": "&#38;",
                    "<": "&#60;",
                    ">": "&#62;",
                    '"': "&#34;",
                    "'": "&#39;",
                    "/": "&#47;"
                },
                b = /&(?!#?\w+;)|<|>|"|'|\//g;
            return function () {
                return this ? this.replace(b, function (b) {
                    return a[b] || b
                }) : this
            }
        }

        function b(a, c, d) {
            return ("string" == typeof c ? c : c.toString()).replace(a.define || g, function (b, c, e, f) {
                return 0 === c.indexOf("def.") && (c = c.substring(4)), c in d || (":" === e ? (a.defineParams && f.replace(a.defineParams, function (a, b, e) {
                    d[c] = {
                        arg: b,
                        text: e
                    }
                }), c in d || (d[c] = f)) : new Function("def", "def['" + c + "']=" + f)(d)), ""
            }).replace(a.use || g, function (c, e) {
                a.useParams && (e = e.replace(a.useParams, function (a, b, c, e) {
                    if (d[c] && d[c].arg && e) {
                        var f = (c + ":" + e).replace(/'|\\/g, "_");
                        return d.__exp = d.__exp || {}, d.__exp[f] = d[c].text.replace(new RegExp("(^|[^\\w$])" + d[c].arg + "([^\\w$])", "g"), "$1" + e + "$2"), b + "def.__exp['" + f + "']"
                    }
                }));
                var f = new Function("def", "return " + e)(d);
                return f ? b(a, f, d) : f
            })
        }

        function d(a) {
            return a.replace(/\\('|\\)/g, "$1").replace(/[\r\t\n]/g, " ")
        }
        var e = {
            version: "1.0.0",
            templateSettings: {
                evaluate: /\{\{([\s\S]+?\}?)\}\}/g,
                interpolate: /\{\{=([\s\S]+?)\}\}/g,
                encode: /\{\{!([\s\S]+?)\}\}/g,
                use: /\{\{#([\s\S]+?)\}\}/g,
                useParams: /(^|[^\w$])def(?:\.|\[[\'\"])([\w$\.]+)(?:[\'\"]\])?\s*\:\s*([\w$\.]+|\"[^\"]+\"|\'[^\']+\'|\{[^\}]+\})/g,
                define: /\{\{##\s*([\w\.$]+)\s*(\:|=)([\s\S]+?)#\}\}/g,
                defineParams: /^\s*([\w$]+):([\s\S]+)/,
                conditional: /\{\{\?(\?)?\s*([\s\S]*?)\s*\}\}/g,
                iterate: /\{\{~\s*(?:\}\}|([\s\S]+?)\s*\:\s*([\w$]+)\s*(?:\:\s*([\w$]+))?\s*\}\})/g,
                varname: "it",
                strip: !0,
                append: !0,
                selfcontained: !1
            },
            template: void 0,
            compile: void 0
        };
        "undefined" != typeof c && c.exports ? c.exports = e : "function" == typeof define && define.amd ? define(function () {
            return e
        }) : (function () {
            return this || (0, eval)("this")
        }()).doT = e, String.prototype.encodeHTML = a();
        var f = {
                append: {
                    start: "'+(",
                    end: ")+'",
                    endencode: "||'').toString().encodeHTML()+'"
                },
                split: {
                    start: "';out+=(",
                    end: ");out+='",
                    endencode: "||'').toString().encodeHTML();out+='"
                }
            },
            g = /$^/;
        e.template = function (c, h, i) {
            h = h || e.templateSettings;
            var j, k, l = h.append ? f.append : f.split,
                m = 0,
                n = h.use || h.define ? b(h, c, i || {}) : c;
            n = ("var out='" + (h.strip ? n.replace(/(^|\r|\n)\t* +| +\t*(\r|\n|$)/g, " ").replace(/\r|\n|\t|\/\*[\s\S]*?\*\//g, "") : n).replace(/'|\\/g, "\\$&").replace(h.interpolate || g, function (a, b) {
                return l.start + d(b) + l.end
            }).replace(h.encode || g, function (a, b) {
                return j = !0, l.start + d(b) + l.endencode
            }).replace(h.conditional || g, function (a, b, c) {
                return b ? c ? "';}else if(" + d(c) + "){out+='" : "';}else{out+='" : c ? "';if(" + d(c) + "){out+='" : "';}out+='"
            }).replace(h.iterate || g, function (a, b, c, e) {
                return b ? (m += 1, k = e || "i" + m, b = d(b), "';var arr" + m + "=" + b + ";if(arr" + m + "){var " + c + "," + k + "=-1,l" + m + "=arr" + m + ".length-1;while(" + k + "<l" + m + "){" + c + "=arr" + m + "[" + k + "+=1];out+='") : "';} } out+='"
            }).replace(h.evaluate || g, function (a, b) {
                return "';" + d(b) + "out+='"
            }) + "';return out;").replace(/\n/g, "\\n").replace(/\t/g, "\\t").replace(/\r/g, "\\r").replace(/(\s|;|\}|^|\{)out\+='';/g, "$1").replace(/\+''/g, "").replace(/(\s|;|\}|^|\{)out\+=''\+/g, "$1out+="), j && h.selfcontained && (n = "String.prototype.encodeHTML=(" + a.toString() + "());" + n);
            try {
                return new Function(h.varname, n)
            } catch (o) {
                throw "undefined" != typeof console && console.log("Could not create a template function: " + n), o
            }
        }, e.compile = function (a, b) {
            return e.template(a, null, b)
        }
    }()
}), define("assets/js/app/util/loadImage", [], function (a, b, c) {
    function d(a, b) {
        var c = new Image,
            d = !1;
        c.onload = function () {
            d = !0
        }, c.src = a, setTimeout(function () {
            d ? b && b.call(c) : setTimeout(arguments.callee, 100)
        }, 0)
    }

    function e(a, b) {
        a.complete || "loading" == a.readyState || "complete" == a.readyState ? b(a) : a.onload = function () {
            b(a)
        }
    }

    function f(a, b) {
        var c = new Image,
            d = !1;
        c.onload = function () {
            d = !0
        }, c.src = a, (c.complete || "loaded" == c.readyState || "complete" == c.readyState) && (d = !0), setTimeout(function () {
            d ? b(c) : setTimeout(arguments.callee, 10)
        }, 0)
    }
    c.exports = {
        imgLoadOver: e,
        loadImg: d,
        detLoadImg: f
    }
}), define("assets/js/app/common/AutoResizeImage", [], function (a, b, c) {
    function d(a, b, c) {
        var d, e, f = new Image,
            g = 1;
        f.src = c.src;
        var h = f.width,
            i = f.height;
        e = a / h, d = b / i, 0 == a && 0 == b ? g = 1 : 0 == a ? 1 > d && (g = d) : 0 == b ? 1 > e && (g = e) : (1 > e || 1 > d) && (g = d >= e ? e : d), 1 > g && (h *= g, i *= g), c.height = i, c.width = h
    }
    c.exports = d
}), define("assets/js/app/common/safeTipHover", [], function (a, b, c) {
    var d = function () {
        this.options = {}, this.conf = function () {
            var a = this,
                b = {
                    $HoverBtn: $(".T_HoverBtn"),
                    HoverTipClass: "T_TipHoverBox"
                },
                c = $.extend(!0, b, a.options);
            return c
        }
    };
    d.prototype.init = function () {
        var a, b, c = this,
            d = c.conf(),
            e = 300;
        d.$HoverBtn.on("mouseenter", function () {
            "undefined" != typeof b && b.css("display", "none"), clearTimeout(a), $(this).find("." + d.HoverTipClass).css("display", "block")
        }).on("mouseleave", function () {
            _this = this, b = $(_this).find("." + d.HoverTipClass), clearTimeout(a), a = setTimeout(function () {
                $(_this).find("." + d.HoverTipClass).css("display", "none")
            }, e)
        })
    }, c.exports = d
}), define("assets/js/app/common/searchAssociate", ["assets/js/app/util/molo"], function (a, b, c) {
    var d = (a("assets/js/app/util/molo"), function () {
        this.options = {
            $Search_Input: $("#J_MainInput"),
            $SearchAss_Box: $("#J_SearchAssociate"),
            $SearchHot_Box: $("#J_HotSearch"),
            $SearchAss_List: $("#J_AssociateList"),
            $SearchHot_List: $("#J_HotSearchList"),
            $Search_Btn: $("#J_SearchBtn"),
            $Search_Form: $("#J_SearchForm"),
            getAssDataCallBack: null,
            isShowDataList: !0,
            delayTime: 100,
            defaultText: "搜索应用或游戏..."
        }, this.conf = function () {
            var a = this,
                b = {
                    configUrl: {
                        hotWords: "/myapp/getSearchHotWords.htm",
                        associate: "/myapp/getSearchSuggest.htm"
                    }
                },
                c = $.extend(!0, b, a.options);
            return c
        }
    });
    d.prototype.isGetHotSearch = !1, d.prototype.searchKeyWords = "undefined" == decodeURIComponent($.ML.util.getSearchByName("kw")) ? "" : decodeURIComponent($.ML.util.getSearchByName("kw")), d.prototype.init = function () {
        var a = this,
            b = a.conf();
        d.prototype.searchKeyWords && a.setInputText(d.prototype.searchKeyWords), a.setNoneSelected(), $(document).on("click", ".T_HotWordsCtrl", function () {
            a.setInputText($(this).find("a").html()), a.inputSubmit()
        }), $(document).on("click", "#J_SearchBtn", function () {
            var c = b.$Search_Input.val();
            return c != b.defaultText && a.inputSubmit(), !1
        }), b.$SearchAss_List.on("mouseenter", "li", function () {
            $this = $(this), a.selectedByIndex($this.index())
        }).on("click", "li", function () {
            a.isSelected() && (b.$Search_Input.val($(this).find("a").html()), a.inputSubmit())
        }), b.$Search_Input.on("keyup", function (c) {
            var d = $(this).val(),
                e = c.keyCode;
            switch (e) {
            case 38:
                return a.keyUpSelected(), !1;
            case 40:
                return a.keyDownSelected(), !1;
            case 13:
                return a.isSelected() ? a.keyEnterSelected() : a.inputSubmit(), !1;
            case 27:
                return a.hideDataList(), !1
            }
            "" != d && null != $(this) ? (a.setSearchAssData(d), a.hideHotSearch(), a.showAssDataList()) : (b.$SearchAss_List.html(""), a.inputTextClear(), a.setNoneSelected(), a.hideAssDataList(), a.showHotSearch())
        }).on("keydown", function (b) {
            var c = ($(this).val(), b.keyCode);
            switch (c) {
            case 13:
                return a.isSelected() ? a.keyEnterSelected() : a.inputSubmit(), !1
            }
        }).on("blur", function () {
            var c = $(this).val();
            "" == c || c == b.defaultText ? (a.inputTextBack(), a.hideHotSearch()) : a.hideAssDataList()
        }).on("focus", function () {
            var c = $(this).val();
            c == b.defaultText ? (a.inputTextClear(), a.showHotSearch()) : d.prototype.searchKeyWords && d.prototype.searchKeyWords == c && (a.inputTextClear(), a.showHotSearch())
        })
    }, d.prototype.showHotSearch = function () {
        var a = this,
            b = a.conf();
        b.$SearchHot_Box.css("display", "block"), a.setHotSearch()
    }, d.prototype.hideHotSearch = function () {
        var a = this,
            b = a.conf();
        setTimeout(function () {
            b.$SearchHot_Box.css("display", "none")
        }, 200)
    }, d.prototype.setHotSearch = function () {
        if (!d.prototype.isGetHotSearch) {
            var a = this,
                b = a.conf();
            $.ajax({
                type: "get",
                url: b.configUrl.hotWords,
                dataType: "json",
                success: function (a) {
                    for (var c = a.obj, e = a.obj.length >= 10 ? 10 : a.obj.length, f = "", g = 0; e > g; g++) f += "<li class='T_HotWordsCtrl'>", f += "<a>", f += c[g], f += "</a>", f += "</li>";
                    b.$SearchHot_List.append(f), d.prototype.isGetHotSearch = !0
                },
                error: function () {}
            })
        }
    }, d.prototype.inputTextClear = function () {
        {
            var a = this;
            a.conf()
        }
        a.setInputText("")
    }, d.prototype.inputTextBack = function () {
        var a = this,
            b = a.conf();
        a.setInputText(b.defaultText)
    }, d.prototype.inputSubmit = function (a) {
        var b = this,
            c = b.conf(),
            a = a;
        a || (a = encodeURIComponent(c.$Search_Input.val())), window.location.href = "../myapp/search.htm?kw=" + a
    }, d.prototype.setInputText = function (a) {
        var b = this,
            c = b.conf();
        c.$Search_Input.val(a)
    }, d.prototype.setSearchAssData = function (a) {
        var b, c = this,
            d = c.conf(),
            e = c.getLastKeyWord();
        e == a ? c.showAssDataList() : (clearTimeout(b), b = setTimeout(function () {
            $.ajax({
                type: "get",
                url: d.configUrl.associate,
                data: "kw=" + a,
                dataType: "json",
                success: function (b) {
                    c.setLastKeyWord(a), c.setNoneSelected(), c.putSearchAssData(b), "function" == typeof d.getDataCallBack && d.getDataCallBack(b)
                },
                error: function () {}
            })
        }, d.delayTime))
    }, d.prototype.putSearchAssData = function (a) {
        {
            var b = this,
                c = b.conf(),
                d = "",
                e = a.obj.keywords,
                f = e.length;
            c.$Search_Input.val()
        }
        if (f > 0) {
            b.emptyAssData();
            for (var g = 0; f > g; g++) d += "<li>", d += "<a>", d += e[g], d += "</a>", d += "</li>";
            c.$SearchAss_List.append(d), b.showAssDataList()
        } else b.hideAssDataList()
    }, d.prototype.setLastKeyWord = function (a) {
        var b = this,
            c = b.conf();
        c.$SearchAss_List.data("seakeyword", a)
    }, d.prototype.getLastKeyWord = function () {
        var a = this,
            b = a.conf();
        return b.$SearchAss_List.data("seakeyword")
    }, d.prototype.emptyAssData = function () {
        var a = this,
            b = a.conf();
        b.$SearchAss_List.empty()
    }, d.prototype.showAssDataList = function () {
        var a = this,
            b = a.conf();
        b.$SearchAss_Box.css("display", "block")
    }, d.prototype.hideAssDataList = function () {
        var a = this,
            b = a.conf();
        setTimeout(function () {
            b.$SearchAss_Box.css("display", "none")
        }, 200)
    }, d.prototype.keyUpSelected = function () {
        var a = this,
            b = a.conf(),
            c = b.$SearchAss_List.find("li").length,
            d = a.getSelectedIndex() - 1 < 0 ? c - 1 : a.getSelectedIndex() - 1;
        a.selectedByIndex(a.isSelected() ? d : c - 1)
    }, d.prototype.keyDownSelected = function () {
        var a = this,
            b = a.conf(),
            c = b.$SearchAss_List.find("li").length,
            d = a.getSelectedIndex() + 1 > c - 1 ? 0 : a.getSelectedIndex() + 1;
        a.selectedByIndex(a.isSelected() ? d : 0)
    }, d.prototype.keyEnterSelected = function () {
        var a = this,
            b = a.conf();
        b.$SearchAss_List.find("li:eq(" + a.getSelectedIndex() + ")").trigger("click"), a.inputSubmit()
    }, d.prototype.getSelectedIndex = function () {
        var a = this,
            b = a.conf();
        return b.$SearchAss_List.data("selindex")
    }, d.prototype.selectedByIndex = function (a) {
        var b = this,
            c = b.conf();
        c.$SearchAss_List.find("li").removeClass("selected"), c.$SearchAss_List.find("li:eq(" + a + ")").addClass("selected"), b.setSelectedIndex(a)
    }, d.prototype.setSelectedIndex = function (a) {
        var b = this,
            c = b.conf();
        c.$SearchAss_List.data("selindex", a)
    }, d.prototype.setNoneSelected = function () {
        {
            var a = this;
            a.conf()
        }
        a.setSelectedIndex(-1)
    }, d.prototype.isSelected = function () {
        {
            var a = this;
            a.conf()
        }
        return -1 == a.getSelectedIndex() ? !1 : !0
    }, d.prototype.isEnterCanSubmit = function () {
        var a = this,
            b = a.conf();
        return b.$SearchAss_List.is(":visible") && a.isSelected()
    }, d.prototype.setInputPutinType = function () {
        var a = this,
            b = a.conf();
        b.$ComSearchBox.hasClass("com-search-box-putin") || b.$ComSearchBox.addClass("com-search-box-putin")
    }, d.prototype.setInputDefaultType = function () {
        var a = this,
            b = a.conf();
        b.$ComSearchBox.hasClass("com-search-box-putin") && b.$ComSearchBox.removeClass("com-search-box-putin")
    }, c.exports = d
}), define("assets/js/app/common/webBehaviour", ["assets/js/app/util/molo"], function (a, b, c) {
    var d = (a("assets/js/app/util/molo"), function () {
        this.opts = {}, this.conf = function () {
            var a = {
                    agentPreUrl: "http://agent.sj.qq.com/",
                    aid: "myappWebBehaviour",
                    sessionID: $.ML.util.getCookie("session_uuid"),
                    post: null,
                    classID: 1,
                    pageName: MOLO.pageKey
                },
                b = $.extend(!0, a, this.opts);
            return b
        }
    });
    d.prototype.pvuvPostInit = function () {
        var a = this,
            b = a.conf();
        a.reportItem({
            targetType: "show",
            targetObj: "pageShow",
            pageName: b.pageName
        })
    }, d.prototype.apkPostNew = function (a) {
        var b = this;
        $(document).on("click", ".com-install-btn,.com-install-lit-btn,.det-ins-btn,.installBtn", function () {
            var c = $(this),
                d = "btn_install",
                e = c.attr("apk"),
                f = c.attr("appname");
            defaultsParamJson = {
                targetType: d,
                targetObj: e,
                mark: f
            }, dataJson = $.extend(!0, {}, defaultsParamJson, a), b.reportItem(dataJson)
        })
    }, d.prototype.apkDownload = function (a) {
        var b = this;
        $(document).on("click", ".det-down-btn", function (c) {
            var d = $(this),
                e = "btn_download",
                f = d.attr("apk"),
                g = d.attr("appname");
            defaultsParamJson = {
                targetType: e,
                targetObj: f,
                mark: g,
                theEvent: c
            }, dataJson = $.extend(!0, {}, defaultsParamJson, a), b.reportItem(dataJson)
        })
    }, d.prototype.getPostParamJson = function (a) {
        var b = this,
            c = b.conf(),
            d = {
                post: {},
                show: {}
            };
        return d.post.sessionID = c.sessionID || "null", d.post.pageName = c.pageName || "null", d.post.modName = a.modName || "null", d.post.targetType = a.targetType || "null", d.post.targetObj = a.targetObj || "null", d.post.mark = a.mark || "null", d.show.sessionID = "（0）sessionID:" + d.post.sessionID, d.show.pageName = "（1）pageName:" + d.post.pageName, d.show.modName = "（2）modName:" + d.post.modName, d.show.targetType = "（3）targetType:" + d.post.targetType, d.show.targetObj = "（4）targetObj:" + d.post.targetObj, d.show.mark = "（5）mark:" + d.post.mark, d
    }, d.prototype.jointParam = function (a) {
        var b = this,
            c = (b.conf(), a),
            d = "";
        for (var e in c) d += "	" + c[e];
        return d
    }, d.prototype.reportItem = function (a) {
        var b = this,
            c = b.conf(),
            d = "",
            e = "",
            f = b.getPostParamJson(a),
            g = f.post,
            h = $.extend(!0, {}, g, a);
        switch (c.aid) {
        case "myappWebBehaviour":
            d = this.jointParam(f.post), e = this.jointParam(f.show)
        }
        printLog("webpost:" + e);
        var i = new Image;
        i.src = c.agentPreUrl + "behaviour.do?aid=" + c.aid + "&post=" + encodeURIComponent(d) + "&t=" + (new Date).getTime(), (h.callback || "function" == typeof h.callback) && h.callback(), "btn_download" == h.targetType
    }, d.prototype.init = function () {
        {
            var a = this;
            a.conf()
        }
        a.pvuvPostInit()
    }, c.exports = d
});