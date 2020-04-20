(function(jq){
    // 资料列表组件
    // 通过自执行函数封装，避免函数重名
    var requestURL;
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

    function initTable(nid, stype) {
        $.ajax({
            url: requestURL,
            type: "GET",
            traditional: true,
            data: {"nid": nid, },
            dataType: "JSON",
            success: function (data, statusText, xmlRequest) {
                if(data.status) {
                    globalDict = data.data.global_dict;
                    createTable(data.data.table_config, data.data.data_detail, data.data.global_dict, stype);
                }else {
                    alert(data.message);
                }
            }
        })
    }

    function createTable(config, data, coldict, stype="detail") {
        var tagFrame = $("#data-free").first();
        var tagTable = document.createElement("table");
        tagFrame.append(tagTable);
        $.each(config, function (k1, confitem) {
            if (confitem.group.length > 0) {
                // 创建分组
                var tagGroup = document.createElement("td");
                tagGroup.innerHTML = confitem.group;
                $(tagGroup).addClass("groupTitle");
                $(tagGroup).attr("colspan", "3");

                var tagLineG = document.createElement("tr");
                $(tagLineG).append(tagGroup);
                $(tagTable).append(tagLineG);
            }
            if (confitem.display[stype]) {
                // 创建列
                var tagLineD = document.createElement("tr");

                var tagBox1 = document.createElement("td");
                tagBox1.innerHTML = confitem.caption;
                $(tagBox1).addClass("col1");
                $(tagLineD).append(tagBox1);

                var tagBox2 = document.createElement("td");
                if (stype === "new") {
                    if (confitem.edit.type === "select") {
                        var tagValue = document.createElement("select");
                        var optTag = document.createElement("option");
                        $(optTag).val("");
                        $(optTag).text("");
                        $(tagValue).append(optTag);
                        $.each(coldict[confitem.edit.dict], function (k2, val2) {
                            optTag = document.createElement("option");
                            $(optTag).val(k2);
                            $(optTag).text(val2);
                            $(tagValue).append(optTag);
                        });
                    } else {
                        var tagValue = document.createElement("input");
                        $(tagValue).attr("type", "text");
                    }
                    $(tagValue).attr("name", confitem.colname);
                    $(tagBox2).append(tagValue);
                } else {
                    var kwargs = {};
                    $.each(confitem.text.kwargs, function (k3, val3) {
                        if (val3.startsWith("@@")) {
                            var tmp = coldict[val3.substring(2, val3.length)][data[confitem.colname]];
                            if (tmp) {
                                kwargs[k3] = coldict[val3.substring(2, val3.length)][data[confitem.colname]];
                            } else {
                                kwargs[k3] = "";
                            }
                        } else if (val3.startsWith("@")) {
                            kwargs[k3] = data[val3.substring(1, val3.length)];
                        } else {
                            kwargs[k3] = val3;
                        }
                    });
                    tagBox2.innerHTML = confitem.text.content.format(kwargs);
                }
                $(tagBox2).addClass("col2");
                $(tagLineD).append(tagBox2);

                var tagBox3 = document.createElement("td");
                $(tagBox3).addClass("col4");
                var tagRemark1 = document.createElement("div");
                $(tagRemark1).addClass("subRemark");
                $(tagRemark1).text(confitem.text.remark[0]);
                $(tagBox3).append(tagRemark1);
                var tagRemark2 = document.createElement("div");
                $(tagRemark2).addClass("subRemark");
                $(tagRemark2).text(confitem.text.remark[1]);
                $(tagBox3).append(tagRemark2);
                $(tagLineD).append(tagBox3);

                $(tagTable).append(tagLineD);
            }
        });
    }

    // 暴露调用接口
    jq.extend({
        "initData": function (url, nid, stype) {
            requestURL = url;
            initTable(nid, stype);
        },
        "operSave": function () {
            $.ajax({
                url: requestURL,
                type: "POST",
                data: $("#data-form").serialize(),
                dataType: "JSON",
                success: function (data, statusText, xmlRequest) {
                    if(data.status) {
                        alert("数据保存成功！");
                    }else {
                        alert(data.message);
                    }
                }
            });
        },
    })
})(jQuery);