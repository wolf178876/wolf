from pyecharts.charts import Bar, Pie, Line, Page, Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, ThemeType
import pymysql.cursors
conn = pymysql.Connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='178876',
                       db='gdsx',
                       charset='utf8')
def query1():
    cur = conn.cursor()
    sql = 'SELECT type, COUNT(*) as count FROM usedcar GROUP BY type ORDER BY count DESC LIMIT 5;'
    cur.execute(sql)
    data = [stu for stu in cur.fetchall()]
    # conn.commit()
    # conn.close()
    car_models = [item[0] for item in data]
    counts = [item[1] for item in data]
    bar = Bar()
    bar.add_xaxis(car_models)
    bar.add_yaxis('车辆数/辆', counts, color="purple")
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=5)),
        title_opts=opts.TitleOpts(title="车辆类型数量排名前5的车辆"),
    )
    return bar
def query2():
    cur = conn.cursor()
    sql = 'select loc,count(loc) as c from usedcar group by loc order by c desc limit 5'
    cur.execute(sql)
    data = [stu for stu in cur.fetchall()]
    # conn.commit()
    # conn.close()
    pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    pie.add('车辆数/辆', data)
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title='二手车数量前五的城市'),
        legend_opts=opts.LegendOpts(pos_right='30%'),
    )
    return pie
def query3():
    cur = conn.cursor()
    create_table_sql = """
        CREATE TEMPORARY TABLE all_intervals (interval_name VARCHAR(10));
    """
    cur.execute(create_table_sql)
    insert_data_sql = """
        INSERT INTO all_intervals (interval_name) VALUES ('5以下'), ('5-10'), ('10-15'), ('15-20'), ('20-25'), ('25-30'), ('30以上');
    """
    cur.execute(insert_data_sql)
    sql = """
        SELECT
            all_intervals.interval_name AS '区间',
            COUNT(usedcar.wgl) AS '数量'
        FROM
            all_intervals
        LEFT JOIN
            usedcar
        ON
            CASE
                WHEN all_intervals.interval_name = '5以下' AND usedcar.wgl <= 5 THEN 1
                WHEN all_intervals.interval_name = '5-10' AND usedcar.wgl > 5 AND usedcar.wgl <= 10 THEN 1
                WHEN all_intervals.interval_name = '10-15' AND usedcar.wgl > 10 AND usedcar.wgl <= 15 THEN 1
                WHEN all_intervals.interval_name = '15-20' AND usedcar.wgl > 15 AND usedcar.wgl <= 20 THEN 1
                WHEN all_intervals.interval_name = '20-25' AND usedcar.wgl > 20 AND usedcar.wgl <= 25 THEN 1
                WHEN all_intervals.interval_name = '25-30' AND usedcar.wgl > 25 AND usedcar.wgl <= 30 THEN 1
                WHEN all_intervals.interval_name = '30以上' AND usedcar.wgl > 30 THEN 1
                ELSE 0
            END = 1
        GROUP BY
            all_intervals.interval_name
        ORDER BY
            FIELD(all_intervals.interval_name, '5以下', '5-10', '10-15', '15-20', '20-25', '25-30', '30以上');
    """
    cur.execute(sql)
    data = [stu for stu in cur.fetchall()]
    drop_table_sql = """
        DROP TEMPORARY TABLE all_intervals;
    """
    cur.execute(drop_table_sql)
    # conn.commit()
    # conn.close()
    car_models = [item[0] for item in data]
    counts = [item[1] for item in data]
    bar = Bar()
    bar.add_xaxis(car_models)
    bar.add_yaxis('车辆数/辆', counts, color="black")
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=15)),
        title_opts=opts.TitleOpts(title="车辆已行驶公里数/万公里的区间"),
    )
    bar.reversal_axis()
    return bar
def query4():
    cur = conn.cursor()
    sql = 'SELECT loc, AVG(price) AS average_price FROM usedcar WHERE loc IN ("济南", "青岛", "北京", "重庆") GROUP BY loc;'
    cur.execute(sql)
    data = [stu for stu in cur.fetchall()]
    # conn.commit()
    # conn.close()
    # print((data))
    car_models = [item[0] for item in data]
    counts = [item[1] for item in data]
    bar = Bar()
    bar.add_xaxis(car_models)
    bar.add_yaxis('万元', counts, color="orange")
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=10)),
        title_opts=opts.TitleOpts(title="济南、青岛、北京、重庆的平均车辆价格"),
    )
    bar.reversal_axis()
    return bar
def query5():
    cur = conn.cursor()
    create_table_sql = """
        CREATE TEMPORARY TABLE all_intervals (interval_name VARCHAR(10));
    """
    cur.execute(create_table_sql)
    insert_data_sql = """
        INSERT INTO all_intervals (interval_name) VALUES ('20以下'), ('20-50'), ('50-100'), ('100-150'), ('150-200'), ('200-300'), ('300-450'), ('450以上');;
    """
    cur.execute(insert_data_sql)
    sql = """
        SELECT
        all_intervals.interval_name AS '区间',
        COUNT(usedcar.price) AS '数量'
        FROM
            all_intervals
        LEFT JOIN
            usedcar
        ON
            CASE
                WHEN all_intervals.interval_name = '20以下' AND usedcar.price <= 20 THEN 1
                WHEN all_intervals.interval_name = '20-50' AND usedcar.price > 20 AND usedcar.price <= 50 THEN 1
                WHEN all_intervals.interval_name = '50-100' AND usedcar.price > 50 AND usedcar.price <= 100 THEN 1
                WHEN all_intervals.interval_name = '100-150' AND usedcar.price > 100 AND usedcar.price <= 150 THEN 1
                WHEN all_intervals.interval_name = '150-200' AND usedcar.price > 150 AND usedcar.price <= 200 THEN 1
                WHEN all_intervals.interval_name = '200-300' AND usedcar.price > 200 AND usedcar.price <= 300 THEN 1
                WHEN all_intervals.interval_name = '300-450' AND usedcar.price > 300 AND usedcar.price <= 450 THEN 1
                        WHEN all_intervals.interval_name = '450以上' AND usedcar.price > 450 THEN 1
                ELSE 0
            END = 1
        GROUP BY
            all_intervals.interval_name
        ORDER BY
            FIELD(all_intervals.interval_name, '20以下', '20-50', '50-100', '100-150', '150-200', '200-300', '300-450','450以上');
    """
    cur.execute(sql)
    data = [stu for stu in cur.fetchall()]
    drop_table_sql = """
        DROP TEMPORARY TABLE all_intervals;
    """
    cur.execute(drop_table_sql)
    # conn.commit()
    # conn.close()
    car_models = [item[0] for item in data]
    counts = [item[1] for item in data]
    bar = Bar()
    bar.add_xaxis(car_models)
    bar.add_yaxis('车辆数', counts, color="green")
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=15)),
        title_opts=opts.TitleOpts(title="各价格区间车辆数"),
    )
    return bar
def query6():
    cur = conn.cursor()
    sql = 'select date ,count(type) from usedcar  where date between "2010/1/1" and "2023/9/8" group by date order by date'
    cur.execute(sql)
    data = [stu for stu in cur.fetchall()]
    car_models = [str(item[0]) for item in data]
    counts = [item[1] for item in data]
    l = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    l.add_xaxis(car_models)
    l.add_yaxis('车辆数', counts)
    l.set_series_opts(label_opts=opts.LabelOpts(rotate=-9))
    l.set_global_opts(
        title_opts=opts.TitleOpts(title='2010-2023卖车趋势'),
        legend_opts=opts.LegendOpts(pos_right='50%'),
    )
    return l
def query7():
    cur = conn.cursor()
    sql = 'SELECT SUBSTRING_INDEX(vip, "年", -1) AS membership_type, COUNT(*) AS count FROM usedcar GROUP BY membership_type;'
    cur.execute(sql)
    data = [stu for stu in cur.fetchall()]
    pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    pie.add('信息', data)
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title='会员类型占比'),
        legend_opts=opts.LegendOpts(pos_right='30%'),
    )
    return pie
def query8():
    cur = conn.cursor()
    sql = 'SELECT loc, COUNT(*) as count FROM usedcar GROUP BY loc;'
    cur.execute(sql)
    data = []
    for row in cur.fetchall():
        loc, count = row
        data.append([loc, count])
    # conn.commit()
    # conn.close()
    g = Geo()
    g.add_schema(maptype='china')
    g.add('车辆数/辆', data,
         type_=ChartType.EFFECT_SCATTER)
    g.set_series_opts(
        legend_opts=opts.LabelOpts(is_show=True)
    )
    g.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(),
        title_opts=opts.TitleOpts(title='二手车在全国城市中的分布')
    )
    return g

# page = Page(layout=Page.DraggablePageLayout)
# page.add(
#     query1(),
#     query2(),
#     query3(),
#     query4(),
#     query5(),
#     query6(),
#     query7(),
#     query8()
# )
# page.render('显示.html')

conn.commit()
conn.close()

Page.save_resize_html(
    '显示.html',
    cfg_file='chart_config.json',
    dest='surprise.html'
)
