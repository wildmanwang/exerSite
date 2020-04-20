(function(jq){
    // 资料列表组件
    // 通过自执行函数封装，避免函数重名
    var requestURL;
    var newURL;
    var globalDict;

    // 为字符串增加格式化方法
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s,i) {
            return args[i];
        });
    };

    function csrfSafeMethod(method){
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/).test(method);
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $("#content input[name='csrfmiddlewaretoken']").val());
            }
        }
    });

    function initTable(pageNum) {
        var conStr;
        conStr = JSON.stringify(getCondition());
        $.ajax({
            url: requestURL,
            type: "GET",
            traditional: true,
            data: {"conditionDict": conStr, "pageNum": pageNum, },
            dataType: "JSON",
            success: function (data, statusText, xmlRequest) {
                if(data.status) {
                    globalDict = data.data.global_dict;
                    createFrame();
                    createCondition(data.data.condition_config, data.data.global_dict);
                    createToolbar();
                    createTableHead(data.data.table_config);
                    createTableBody(data.data.table_config, data.data.data_list, data.data.global_dict, data.data.page_info.startRec);
                    createDataPage(data.data.page_info);
                }else {
                    alert(data.message);
                }
            }
        })
    }

    function createFrame() {
        $("#data-grid").empty();

        var tagTable = document.createElement("table");
        $(tagTable).attr("style", "width: 100%; ");
        $("#data-grid").append(tagTable);

        var tagHead = document.createElement("thead");
        $(tagHead).attr("id", "thead");
        $(tagTable).append(tagHead);

        var tagBody = document.createElement("tbody");
        $(tagBody).attr("id", "tbody");
        $(tagTable).append(tagBody);

        var tagPage = document.createElement("div");
        $(tagPage).attr("id", "data-page");
        $(tagPage).attr("style", "text-align: right; overflow: hidden; ");
        $("#data-grid").append(tagPage);
    }

    function getCondition() {
        var conditionDict = {};
        $.each($("#condition-grid .query-condition"), function (k1, tagGroup) {
            var colname = $(tagGroup).find(".query-select option:selected").attr("name");
            if (colname.length > 0) {
                var colType = $(tagGroup).find(".query-select option:selected").attr("input-type");
                var colValue;
                if (colType === "select") {
                    colValue = $(tagGroup).find(".query-value option:selected").attr("value");
                } else {
                    colValue = $(tagGroup).find(".query-value").val();
                }
                if (colValue.length > 0) {
                    conditionDict[colname] = colValue;
                }
            }
        });
        return conditionDict;
    }

    function createCondition(config, coldict) {
        // {
        //     "name": "device_type",
        //     "caption": "设备类型",
        //     "input_type": "select",
        //     "select_dict": "device_type_list",
        // }
        // <div id="condition-grid" style="margin: 2px 5px 0 5px; border: #BBBBBB 1px solid; ">
        //     <div class="query-condition">
        //         <div class="left query-line btn-oper" name="btn-condition-add"><span class="btn-flag">+</span></div>
        //         <select class="left query-line query-select"></select>
        //         <div class="left query-line query-value"></div>
        //         <button class="left query-line query-btn" name="btn">查询</button>
        //     </div>
        // </div>
        if ($("#condition-grid").children().length > 0) return;

        var frameTag = document.createElement("div");
        $(frameTag).addClass("query-condition");

        var tag1 = document.createElement("div");
        $(tag1).addClass("left query-line btn-oper");
        var subTag = document.createElement("span");
        if (0 === 0) {
            $(subTag).text("+");
            $(tag1).attr("onclick", "$.conditionAdd(this)");
        } else {
            $(subTag).text("-");
            $(tag1).attr("onclick", "$.conditionRemove(this)");
        }
        $(subTag).addClass("btn-flag");
        $(tag1).append(subTag);
        $(frameTag).append(tag1);

        var tag2 = document.createElement("select");
        $(tag2).addClass("left query-line query-select");
        var optTag = document.createElement("option");
        $(optTag).attr("name", "");
        $(tag2).append(optTag);
        $.each(config, function (k1, col1) {
            var optTag = document.createElement("option");
            $(optTag).attr("name", col1.name);
            $(optTag).attr("input_type", col1.input_type);
            $(optTag).attr("select_dict", col1.select_dict);
            $(optTag).text(col1.caption);
            $(tag2).append(optTag);
        });
        $(tag2).attr("onchange", "$.conditionChange(this)");
        $(frameTag).append(tag2);

        var tag3 = document.createElement("div");
        $(tag3).addClass("left query-line query-value-border");
        $(frameTag).append(tag3);

        var tag4 = document.createElement("button");
        $(tag4).addClass("left query-line query-btn");
        $(tag4).attr("name", "btn");
        $(tag4).text("查询");
        $(tag4).attr("onclick", "$.initData(\"" + requestURL + "\", 1);");
        $(frameTag).append(tag4);

        $("#condition-grid").append(frameTag);
    }

    function createToolbar() {
        var tagFrame = $("#toolbar");
        if ($(tagFrame).children().length > 0) return;

        var configData = [
            {
                "name": "operSelectAll",
                "caption": "全选",
                "click-type": "click",
                "onclick": "$.operSelectAll(this)",
            },
            {
                "name": "operSelectCancel",
                "caption": "取消",
                "click-type": "click",
                "onclick": "$.operSelectCancel(this)",
            },
            {
                "name": "operSelectReverse",
                "caption": "反选",
                "click-type": "click",
                "onclick": "$.operSelectReverse(this)",
            },
            {
                "name": "operNew",
                "caption": "添加",
                "click-type": "click",
                "onclick": "$.operNew(this)",
            },
            {
                "name": "operDelete",
                "caption": "删除",
                "click-type": "click",
                "onclick": "$.operDelQuestion(this)",
            },
            {
                "name": "operEdit",
                "caption": "进入编辑模式",
                "click-type": "check",
                "onclick": "$.operEdit(this)",
            },
            {
                "name": "operSave",
                "caption": "保存",
                "click-type": "click",
                "onclick": "$.operSave(this)",
            },
            {
                "name": "operRefresh",
                "caption": "刷新",
                "click-type": "click",
                "onclick": "$.operRefresh(this)",
            },
        ];
        $.each(configData, function (k1, configItem) {
            var tBtn = document.createElement("span");
            $(tBtn).text(configItem.caption);
            $(tBtn).attr("name", configItem.name);
            $(tBtn).attr("click-type", configItem["click-type"]);
            if (configItem["click-type"] === "check") {
                $(tBtn).attr("state", "0");
            }
            $(tBtn).addClass("left toolBtn");
            $(tBtn).attr("onclick", configItem.onclick);
            $("#toolbar").append(tBtn);
        });
    }

    function createTableHead(config) {
        var tr = document.createElement("tr");
        var th = document.createElement("th");
        th.innerHTML = "选择";
        $(th).attr("style", "width: 50px; ");
        $(tr).append(th);
        th = document.createElement("th");
        th.innerHTML = "序号";
        $(th).attr("style", "width: 50px; ");
        $(tr).append(th);
        $.each(config, function (k, v) {
            if(v.display.grid){
                th = document.createElement("th");
                th.innerHTML = v.caption;
                $(tr).append(th);
            }
        });
        $("#thead").append(tr);
    }

    function createTableBody(config, data, coldict, startRec) {
        $.each(data, function (k1, row) {
            var tr = document.createElement("tr");
            $(tr).attr("rowid", row["id"]);
            var td = document.createElement("td");
            $(td).attr("style", "background-color: #f2f2f2; text-align: center; ");
            var tagCheckbox = document.createElement("input");
            tagCheckbox.type = "checkbox";
            $(td).append(tagCheckbox);
            $(tr).append(td);
            td = document.createElement("td");
            td.innerHTML = startRec + k1 + 1;
            $(td).attr("style", "background-color: #f2f2f2; text-align: center; ");
            $(tr).append(td);
            $.each(config, function (k2, confitem) {
                if (confitem.display.grid) {
                    td = document.createElement("td");
                    var strStyle = "background-color: #f2f2f2; padding: 5px; text-align: " + confitem.text.align + "; ";
                    var kwargs = {};
                    $.each(confitem.text.kwargs, function (k3, val3) {
                        if (val3.startsWith("@@")) {
                            var tmp = coldict[val3.substring(2, val3.length)][row[confitem.colname]];
                            if (tmp) {
                                kwargs[k3] = coldict[val3.substring(2, val3.length)][row[confitem.colname]];
                            } else {
                                kwargs[k3] = "";
                            }
                        } else if (val3.startsWith("@")) {
                            kwargs[k3] = row[val3.substring(1, val3.length)];
                        } else {
                            kwargs[k3] = val3;
                        }
                    });
                    td.innerHTML = confitem.text.content.format(kwargs);
                    if (confitem.edit.enable === 1) {
                        td.setAttribute("colname", confitem.colname);
                        td.setAttribute("editable", "1");
                        td.setAttribute("edittype", confitem.edit.type);
                        if (confitem.edit.type === "select") {
                            td.setAttribute("editdict", confitem.edit.dict);
                        }
                        td.setAttribute("origin", row[confitem["colname"]]);
                        td.setAttribute("current", row[confitem["colname"]]);
                    }
                    $.each(confitem.attr, function (k4, val4) {
                        if (val4.startsWith("@")){
                            td.setAttribute(k4, row[val4.substring(1, val4.length)]);
                        } else {
                            td.setAttribute(k4, val4);
                        }
                    });
                    $(td).attr("style", strStyle);
                    $(tr).append(td);
                }
            });
            $("#tbody").append(tr);
        })
    }

    function createDataPage(pageStr) {
        $("#data-page").empty().append(pageStr.page_str);
        $("#PAGE_reccnt_perpage_select").val($.cookie("reccnt_perpage"));
        $("#PAGE_reccnt_perpage_select").change(function () {
            $.cookie("reccnt_perpage", $(this).val(), {path: "/"});
            $.initData(requestURL);
        });
    }

    function getPageNum() {
        var pageNum = $("#pageBanner span").text();
        if (!pageNum) {
            pageNum = "1";
        }
        return pageNum;
    }

    function editIn() {
        $.each($("#tbody tr"), function (k1, row) {
            if ($(row).find("input[type='checkbox']").prop("checked")) {
                $(row).attr("editting", "1");
                $.each($(row).find("td[editable='1']"), function (k2, col) {
                    if ($(col).attr("edittype") === "select") {
                        var tagValue = document.createElement("select");
                        var optTag = document.createElement("option");
                        $(optTag).val("");
                        $(optTag).text("");
                        $(tagValue).append(optTag);
                        $.each(globalDict[$(col).attr("editdict")], function (k3, val3) {
                            optTag = document.createElement("option");
                            $(optTag).val(k3);
                            $(optTag).text(val3);
                            $(tagValue).append(optTag);
                        });
                        $(tagValue).val($(col).attr("current"));
                    } else {
                        var tagValue = document.createElement("input");
                        $(tagValue).val(col.innerHTML);
                    }
                    col.innerHTML = "";
                    $(tagValue).addClass("editBox");
                    $(col).append(tagValue);
                });
            }
        });
    }

    function editOut() {
        $.each($("#tbody tr[editting='1']"), function (k1, row) {
            $.each($(row).find("td[editable='1']"), function (k2, col) {
                if ($(col).attr("edittype") === "select") {
                    var sText = $(col).find("option:selected").text();
                    $(col).attr("current", $(col).find("option:selected").val());
                    $(col).find("select").remove();
                } else {
                    var sText = $(col).find("input").val();
                    $(col).attr("current", sText);
                    $(col).find("input").remove();
                }
                col.innerHTML = sText;
            });
            $(row).attr("editting", "0");
        });
    }

    function editOper(stype) {
        var operBtn = $("#toolbar span[name='operEdit']");
        var num = 0;
        $.each($("#tbody input[type='checkbox']"), function (k1, row) {
            if ($(row).prop("checked")) {
                num ++;
            }
        });
        if (stype === "editIn") {
            if (operBtn.attr("state") === "0") {
                if (num > 0) {
                    operBtn.attr("state", "1");
                    operBtn.addClass("check");
                    editIn();
                    operBtn.text("退出编辑模式");
                } else {
                    $("#dialogInfo span[name='title']").text("请选择要编辑的行。");
                    $("#dialogInfo").removeClass("hide");
                    $(".cover-layer").removeClass("hide");
                }
            }
        } else if (stype === "editOut") {
            if (operBtn.attr("state") === "1") {
                operBtn.attr("state", "0");
                operBtn.removeClass("check");
                editOut();
                operBtn.text("进入编辑模式");
            }
        } else {
            if (operBtn.attr("state") === "0") {
                if (num > 0) {
                    operBtn.attr("state", "1");
                    operBtn.addClass("check");
                    editIn();
                    operBtn.text("退出编辑模式");
                } else {
                    $("#dialogInfo span[name='title']").text("请选择要编辑的行。");
                    $("#dialogInfo").removeClass("hide");
                    $(".cover-layer").removeClass("hide");
                }
            } else {
                operBtn.attr("state", "0");
                operBtn.removeClass("check");
                editOut();
                operBtn.text("进入编辑模式");
            }
        }
    }

    // 暴露调用接口
    jq.extend({
        "initData": function (jsonUrl, newUrl, pageNum) {
            requestURL = jsonUrl;
            newURL = newUrl;
            if (!pageNum) pageNum = getPageNum();
            initTable(pageNum);
        },
        "conditionAdd": function () {
            var newTag = $("#condition-grid").children().first().clone();
            $(newTag).find(".query-value-border").empty();
            $("#condition-grid .query-btn").attr("style", "display: none;");
            $(newTag).find(".query-btn").removeAttr("style");
            $(newTag).find(".btn-flag").text("-");
            $(newTag).find(".btn-oper").removeAttr("onclick");
            $(newTag).find(".btn-oper").attr("onclick", "$.conditionRemove(this)");
            $("#condition-grid").append(newTag);
        },
        "conditionRemove": function (obj) {
            var tagParent = $(obj).parent().parent();
            $(obj).parent().remove();
            $(tagParent).find(".query-btn:last").removeAttr("style");
        },
        "conditionChange": function (obj) {
            var opt = $(obj).find("option:selected");
            var tagborder = $(obj).parent().find(".query-value-border");
            $(tagborder).empty();
            if (opt.attr("input_type") === "select") {
                var tagValue = document.createElement("select");
                var optTag = document.createElement("option");
                $(optTag).val("");
                $(optTag).text("");
                $(tagValue).append(optTag);
                $.each(globalDict[opt.attr("select_dict")], function (k1, v1) {
                    optTag = document.createElement("option");
                    $(optTag).val(k1);
                    $(optTag).text(v1);
                    $(tagValue).append(optTag);
                })
            } else {
                var tagValue = document.createElement("input");
            }
            $(tagValue).addClass("query-value");
            $(tagborder).append(tagValue);
        },
        "operSelectAll": function (obj) {
            $.each($("#tbody input[type='checkbox']"), function (k1, item) {
                $(item).prop("checked", true);
            });
        },
        "operSelectCancel": function (obj) {
            $.each($("#tbody input[type='checkbox']"), function (k1, item) {
                $(item).prop("checked", false);
            });
        },
        "operSelectReverse": function (obj) {
            $.each($("#tbody input[type='checkbox']"), function (k1, item) {
                if ($(item).prop("checked")) {
                    $(item).prop("checked", false);
                } else {
                    $(item).prop("checked", true);
                }
            });
        },
        "operNew": function (obj) {
            location.href = newURL;
        },
        "operDelQuestion": function (obj) {
            var num = 0;
            $.each($("#tbody input[type='checkbox']"), function (k1, row) {
                if ($(row).prop("checked")) {
                    num ++;
                }
            });
            if (num > 0) {
                $("#dialogDelete").removeClass("hide");
            } else {
                $("#dialogInfo span[name='title']").text("请选择要删除的行。");
                $("#dialogInfo").removeClass("hide");
            }
            $(".cover-layer").removeClass("hide");
        },
        "operDelete": function () {
            var deleteList = [];
            var num = 0;
            $.each($("#tbody input[type='checkbox']"), function (k1, item) {
                if ($(item).prop("checked")) {
                    deleteList.push($(item).parent().parent().attr("rowid"));
                    num ++;
                }
            });
            if (num > 0) {
                conStr = JSON.stringify(deleteList);
                $.ajax({
                    url: requestURL,
                    type: "DELETE",
                    traditional: true,
                    data: {"deleteList": conStr, "csrfmiddlewaretoken": $("#content input[name='csrfmiddlewaretoken']").val()},
                    dataType: "JSON",
                    success: function (data, statusText, xmlRequest) {
                        if(data.status) {
                            $("#dialogDelete").addClass("hide");
                            $(".cover-layer").addClass("hide");
                            alert("数据删除成功！");
                            $.each($("#tbody input[type='checkbox']"), function (k2, item) {
                                if ($(item).prop("checked")) {
                                    $(item).parent().parent().remove();
                                }
                            });
                        }else {
                            alert(data.message);
                        }
                    }
                });
            }
        },
        "operEdit": function (obj) {
            editOper("editToggle");
        },
        "operSave": function (obj) {
            editOper("editOut");
            var updateDict = {};
            var num;
            $.each($("#tbody tr"), function (k1, row) {
                updateDict[$(row).attr("rowid")] = {};
                num = 0;
                $.each($(row).find("td[editable='1']"), function (k2, col) {
                    if ($(col).attr("origin") !== $(col).attr("current")) {
                        updateDict[$(row).attr("rowid")][$(col).attr("colname")] = $(col).attr("current");
                        num += 1;
                    }
                });
                if (num === 0) {
                    delete updateDict[$(row).attr("rowid")];
                }
            });
            num = 0;
            for (var item in updateDict) {
                num ++;
            }
            if (num > 0) {
                conStr = JSON.stringify(updateDict);
                $.ajax({
                    url: requestURL,
                    type: "PUT",
                    traditional: true,
                    data: {"updateDict": conStr, "csrfmiddlewaretoken": $("#content input[name='csrfmiddlewaretoken']").val()},
                    dataType: "JSON",
                    success: function (data, statusText, xmlRequest) {
                        if(data.status) {
                            alert("数据保存成功！");
                        }else {
                            alert(data.message);
                        }
                    }
                });
            }
        },
        "operRefresh": function (obj) {
            editOper("editOut");
            $.initData(requestURL, 0);
        }
    })
})(jQuery);