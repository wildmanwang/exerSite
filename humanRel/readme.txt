项目中文名：人情簿
项目英文名：Human Relations Management System
项目代码：humanRel

【问题】
人员修改，为什么User字段不能正确显示？
person reltype=0多个校验报错
礼簿完成字段循环

【技术点】
OK csrf校验
OK 用户验证：session
OK Form数据验证
OK 网页模板
OK 网页组件
?? 对于有参数的URL，jQuery中无法对参数动态赋值？如果参数以?arg=1形式，jQuery中可以赋值，而模板中如何反解？
?? select_related和prefetch_related
功能标准化：列表、新增、修改、删除
    https://github.com/howardandlili/AutoCMDB-master
    https://github.com/KC9226/AutoCmdb
    https://github.com/lingzhongxian/AutoCMDB
    https://github.com/P79N6A/AutoCmdb
    https://github.com/LamberMa/AutoCMDB
    https://github.com/dragon0486/AutoCMDB
中间件
信号
缓存
表格导出
单选按钮
反向解析地址
图片按钮
资料选择筐（数据分页）
输入提示下拉框

【业务优化】
礼簿录入时，方便维护家庭/人员
礼簿录入时，自动提示关系/称呼
好友系统：发送请柬、名片
家庭更换家长、拆分
OK “礼宴亲朋”新增修改时，“当事人”列只能选择当前家庭的成员
?? “八方随礼”新增修改时，当事人要根随家庭列变化而变化

【系统管理】
参数（parameters）
	代码
	名称
	取值
	分类（系统、资料、业务、报表、其他）
	备注
用户（user）
	用户名
	人员
	手机号码
	电子邮箱
	登录密码
	状态

【基础信息】
预测规则（eventPredictRule）
	结婚：未婚、男22女20
	生子：结婚后无子、50岁以前
	周岁：生子1.5年内未隆重宴请
	祝寿：36、60、70、80、90、100、110，男进女满
	考学：高中生
	乔迁：（无）
	身故：（无）
人物秘史
    日期
    性质（褒义、贬义、有趣、普通）
    详细描述
    图片
